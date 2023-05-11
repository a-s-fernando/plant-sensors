terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }
  required_version = ">= 1.2.0"
}
# Initalise environment variables 
variable "access_key" {
  type = string
}
variable "secret_key" {
  type = string
}
variable "username" {
  type = string
}
variable "password" {
  type = string
}

# Configure AWS provider
provider "aws" {
  access_key = var.access_key
  secret_key = var.secret_key
  region     = "eu-west-2"
}

# Use existing VPC
data "aws_vpc" "c7-vpc" {
  id = "vpc-010fd888c94cf5102"
}

# Use existing subnet
data "aws_db_subnet_group" "c7-subnets" {
  name = "c7-db-subnet-group"
}

# Use existing security group
data "aws_security_group" "c7-remote-access" {
  name   = "c7-remote-access"
  vpc_id = data.aws_vpc.c7-vpc.id
  id     = "sg-01745c9fa38b8ed68"

}

# Create a RDS database
resource "aws_db_instance" "aaa-plant-db" {
  identifier        = "c7-aaa-plant-db"
  engine            = "postgres"
  engine_version    = "14.1"
  instance_class    = "db.t3.micro"
  allocated_storage = 20
  username          = var.username
  password          = var.password
  # Ensures the RDS database can be accessed.
  publicly_accessible    = true
  db_subnet_group_name   = data.aws_db_subnet_group.c7-subnets.name
  vpc_security_group_ids = [data.aws_security_group.c7-remote-access.id]
  skip_final_snapshot    = true
}

# Create S3 bucket
resource "aws_s3_bucket" "c7-aaa-s3-bucket" {
  bucket = "c7-aaa-s3-bucket"
}

# Creata lambda IAM policy
data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

# Creata lambda IAM role
resource "aws_iam_role" "lambda-role" {
  name_prefix = "iam-aaa-for-lambda"
  #  = "iam-aaa-for-lambda"
  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [{
      "Action" : "sts:AssumeRole",
      "Principal" : {
        "Service" : "lambda.amazonaws.com"
      },
      "Effect" : "Allow"
    }]
  })
}

# Create minutely lambda function
resource "aws_lambda_function" "c7-aaa-lambda-minutely" {
  function_name = "c7-aaa-lambda-minutely"
  role          = aws_iam_role.lambda-role.arn
  memory_size   = 3010
  timeout       = 120
  image_uri     = "605126261673.dkr.ecr.eu-west-2.amazonaws.com/c7-aaa-ecr-minutely:latest"
  package_type  = "Image"
  architectures = ["x86_64"]

  environment {
    variables = {
      DB_USER     = var.username
      DB_PASSWORD = var.password
      DB_HOST     = aws_db_instance.aaa-plant-db.address
      DB_PORT     = aws_db_instance.aaa-plant-db.port

    }
  }

}

# Create daily lambda function
resource "aws_lambda_function" "c7-aaa-lambda-daily" {
  function_name = "c7-aaa-lambda-daily"
  role          = aws_iam_role.lambda-role.arn
  memory_size   = 3010
  timeout       = 120
  image_uri     = "605126261673.dkr.ecr.eu-west-2.amazonaws.com/c7-aaa-ecr-daily:latest"
  package_type  = "Image"
  architectures = ["x86_64"]

  environment {
    variables = {
      ACCESS_KEY  = var.access_key
      SECRET_KEY  = var.secret_key
      DB_USER     = var.username
      DB_NAME     = var.username
      DB_PASSWORD = var.password
      DB_HOST     = aws_db_instance.aaa-plant-db.address
      DB_PORT     = aws_db_instance.aaa-plant-db.port

    }
  }
}

# Create minutely schedule for lambda function 
resource "aws_cloudwatch_event_rule" "c7-schedule-lambda-minutely" {
  name                = "c7-schedule-lambda-minutely"
  schedule_expression = "rate(1 minute)"

}
# Create minutely schedule target for lambda function 
resource "aws_cloudwatch_event_target" "c7-schedule-target-minutely" {
  rule = aws_cloudwatch_event_rule.c7-schedule-lambda-minutely.name
  arn  = aws_lambda_function.c7-aaa-lambda-minutely.arn
}

# Create minutely trigger prevention
resource "aws_lambda_permission" "allow_minutely_event_trigger" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.c7-aaa-lambda-minutely.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.c7-schedule-lambda-minutely.arn
}



# Create daily schedule for lambda function 
resource "aws_cloudwatch_event_rule" "c7-schedule-lambda-daily" {
  name                = "c7-schedule-lambda-daily"
  schedule_expression = "rate(1 day)"

}

# Create daily schedule target for lambda function 
resource "aws_cloudwatch_event_target" "c7-schedule-target-daily" {
  rule = aws_cloudwatch_event_rule.c7-schedule-lambda-daily.name
  arn  = aws_lambda_function.c7-aaa-lambda-daily.arn
}

# Create daily trigger prevention
resource "aws_lambda_permission" "allow_daily_event_trigger" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.c7-aaa-lambda-daily.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.c7-schedule-lambda-daily.arn
}
