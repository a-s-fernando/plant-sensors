terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
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
data "aws_subnet" "c7-subnet-public1-eu-west-2a" {
  id = "subnet-0bd43551b596597e1"
}

# Create a RDS database
resource "aws_db_instance" "postgres_db" {
  engine         = "postgres"
  engine_version = "15.0"
  instance_class = ""

  name     = ""
  username = ""
  password = ""

  db_subnet_group_name = "default"
  subnet_id            = [data.aws_subnet.c7-subnet-public1-eu-west-2a]

}

