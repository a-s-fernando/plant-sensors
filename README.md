# Plant-Sensors 🌱🌸🌼

Repository for the SigmaLabsXYZ LMNH plant sensors project. This repository allows users to build a database pipeline to store plant data from the Liverpool Natural History Museum's Plant API.

🌿[LMNH Plant API](https://data-eng-plants-api.herokuapp.com/)🌵
<span style="opacity: 0.5">_Use the endpoint **/plants/{plant_id}** to find a plant by it's **plant_id**._</span>

## Table of Contents

- [Files](#files) 🌾
- [Installation](#installation) 🌱
- [Usage](#usage) 🪴
- [The Data](#the-data) 🌿
- [The Architecture](#the-architecture) 🌲
- [Our Dashboards](#our-dashboards) 🌳
- [License](#license) 🍂

<br>

🌱🌿🍃🌵🌿🍃🌵🌱🌿🍃🌵🌿🍃🌵🌱🌿🍃🌵🌿🍃🌵🌱🌿🍃🌵🌿🍃🌵

## Files

WORK IN PROGRESS

🌱🌿🍃🌵🌿🍃🌵🌱🌿🍃🌵🌿🍃🌵🌱🌿🍃🌵🌿🍃🌵🌱🌿🍃🌵🌿🍃🌵

## Installation

WORK IN PROGRESS

To run this project, you will need to perform the following steps:

1. Create an Amazon Elastic Container Registry (ECR) repository to store your Docker images. This can be done through the AWS Management Console or using the AWS CLI.

2. Go into the load and transfer directories and build the Docker images of these scripts for your project, using the Dockerfile provided in this repository. Then, push the image to your ECR repository using the following commands:

   `docker build -t _ECR REPOSITORY NAME_ . --platform "linux/amd64"`

   `docker images`

   Copy the image ID of your latest repository and tag it then push it to AWS ECR using:

   `docker tag <IMAGE ID> <ECR REPOSITORY URI>`

   `docker push <ECR REPOSITORY URI>`

3. Create a `terraform.tfvars` file in the `terraform` directory with the following contents:

   `aws_access_key = "<YOUR AWS ACCESS KEY>"`

   `aws_secret_key = "<YOUR AWS SECRET KEY>"`

   `db_user = "<YOUR DATABASE USERNAME>"`

   `db_password = "<YOUR DATABASE PASSWORD>"`

   Replace the values in angle brackets with your own AWS access key, AWS secret key, database username, and database password.

4. Run Terraform to create your infrastructure resources, using the following commands:

   `terraform init`

   `terraform plan -var-file=terraform.tfvars`

   `terraform apply -var-file=terraform.tfvars`

   This will create an RDS database and other necessary resources in your AWS account.

   Once you have completed these steps, your project should be up and running on your AWS account. You can access the project by navigating to the URL provided by the API endpoint in your web browser.

![planting](https://64.media.tumblr.com/32090cdc70e0098abde641e7176fab8e/tumblr_ojecf2O8FT1w0423ro1_500.gifv)

🌱🌿🍃🌵🌿🍃🌵🌱🌿🍃🌵🌿🍃🌵🌱🌿🍃🌵🌿🍃🌵🌱🌿🍃🌵🌿🍃🌵

## Usage

WORK IN PROGRESS

<br>

🌱🌿🍃🌵🌿🍃🌵🌱🌿🍃🌵🌿🍃🌵🌱🌿🍃🌵🌿🍃🌵🌱🌿🍃🌵🌿🍃🌵

## The Data

This project pulls data from the Plants API hosted on Heroku, and processes it into a structured format for storage and analysis. The data includes the following measurements, which are collected every minute:

- Plant origin continent
- Plant origin country
- Sunlight requirements for the plant
- Plant name
- Plant cycle
- Recording time
- Last watered time
- Soil moisture level
- Temperature
- Botanist first and last names
- Botanist email

The raw data is processed through a data pipeline, which cleans and transforms it into a structured format suitable for storage in a database. The structured data is then inserted into a schema for further analysis and visualization.

By collecting data on the plants' origin, sunlight requirements, and other environmental factors, this project can help to optimize plant care and management and inform future research and development efforts in the field of botany.

![seeds sprouting](https://media.tenor.com/_hcJywXeOmoAAAAC/cartoon-planting.gif)

<br>

🌱🌿🍃🌵🌿🍃🌵🌱🌿🍃🌵🌿🍃🌵🌱🌿🍃🌵🌿🍃🌵🌱🌿🍃🌵🌿🍃🌵

## The Architecture

WORK IN PROGRESS

<br>

🌱🌿🍃🌵🌿🍃🌵🌱🌿🍃🌵🌿🍃🌵🌱🌿🍃🌵🌿🍃🌵🌱🌿🍃🌵🌿🍃🌵

## OUR Dashboards

WORK IN PROGRESS

<br>

🌱🌿🍃🌵🌿🍃🌵🌱🌿🍃🌵🌿🍃🌵🌱🌿🍃🌵🌿🍃🌵🌱🌿🍃🌵🌿🍃🌵

## Licenses

This project uses the following third-party software and tools, each with its own licensing terms:

- AWS services and tools: AWS offers a variety of services and tools, each with its own licensing terms. You can find more information about AWS licenses on their [website](https://aws.amazon.com/legal/).
- Docker: Docker is released under the Apache 2.0 license. See [here](https://www.apache.org/licenses/LICENSE-2.0) for more information about the Apache 2.0 license.
- Terraform: Terraform is released under the Apache 2.0 license. See [here](https://www.apache.org/licenses/LICENSE-2.0) for more information about the Apache 2.0 license.
