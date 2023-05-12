# Plant-Sensors 🌱🌸🌼

Repository for the SigmaLabsXYZ LMNH plant sensors project. This repository allows users to build a database pipeline to store plant data from the Liverpool Natural History Museum's Plant API.

🌿[LMNH Plant API](https://data-eng-plants-api.herokuapp.com/)🌵
_Use the endpoint **/plants/{plant_id}** to find a plant by it's **plant_id**._

## Table of Contents

- [Files](#files) 🌾
- [Installation](#installation) 🌱
- [Usage](#usage) 🪴
- [The Data](#the-data) 🌿
- [The Architecture](#the-architecture) 🌲
- [License](#licenses) 🍂

<br>

🌱🌿🍃🌵🌿🍃🌵🌱🌿🍃🌵🌿🍃🌵🌱🌿🍃🌵🌿🍃🌵🌱🌿🍃🌵🌿🍃🌵

## Files

### Dashboard

### This directory contains files related to the dashboard interface of our data pipeline.

- main.py: This file contains code for running our Dash application through app.py.
- combine_data.py: This file contains code for combining csvs into a single table to aid data visualisation.
- app.py: This file contains code for setting up and running the functionality of our dashboard.
- setup.py: This file contains code for S3 connections and file retrieval.
- requirements.txt: This file lists the required Python packages for our application.
- **Pages**: This directory contains files related to the user interface of our data pipeline.

### Load

### This directory contains files related to the data extraction and loading functionality of our pipeline.

- .dockerignore: This file specifies which files and directories should be ignored by Docker when building the image for our load container.
- database_connection.py: This file contains code for connecting to our database.
- Dockerfile: This file is used for building the Docker image for our load functionality.
- extract.py: This file contains code for extracting and transforming data from the API.
- load.py: This file contains code for cleaning and transforming data, and loading it into our database.
- requirements.txt: This file lists the required Python packages for our load functionality.

### Transfer

### This directory contains files related to data transfer functionality of our pipeline.

- .dockerignore: This file specifies which files and directories should be ignored by Docker when building the image for our transfer functionality.
- Dockerfile: This file is used for building the Docker image for our transfer functionality.
- requirements.txt: This file lists the required Python packages for our transfer functionality.
- transfer.py: This file contains code for transferring data from the RDS to an S3 as .csv files.

**.gitignore**: This file specifies which files and directories should be ignored by Git when committing changes.

**README.md**: This file contains information about our data pipeline project and instructions for getting started.

**main.tf**: This file is a Terraform configuration file for deploying AWS resources.

**schema.sql**: This file contains SQL code for creating the schema of our database.

<br>
🌱🌿🍃🌵🌿🍃🌵🌱🌿🍃🌵🌿🍃🌵🌱🌿🍃🌵🌿🍃🌵🌱🌿🍃🌵🌿🍃🌵

## Installation

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

5. Connect to the RDS using an PostgreSQL client and run the **'schema.sql'** file to build the database schema for this project. The schema follows the following entity-relationship diagram:

![ERD](https://i.ibb.co/TYJX9H1/image-1.png)

Once you have completed these steps, your project should be up and running on your AWS account. You can access the project by navigating to the URL provided by the API endpoint in your web browser.

![planting](https://64.media.tumblr.com/32090cdc70e0098abde641e7176fab8e/tumblr_ojecf2O8FT1w0423ro1_500.gifv)

🌱🌿🍃🌵🌿🍃🌵🌱🌿🍃🌵🌿🍃🌵🌱🌿🍃🌵🌿🍃🌵🌱🌿🍃🌵🌿🍃🌵

## Usage

### Tableau Dashboard

To view the live data collected each day in a visual format, use the Tableau dashboard. To access the dashboard, follow these steps:

1. Log in to the Tableau server.
2. Navigate to the dashboard for the desired data set.
3. Use the interactive filters and charts to explore the data.

![tableau](https://i.ibb.co/MPCWsc7/Dashboard-1-1.png)

### Plotly Dashboards

To view the archived data in a web-based dashboard, use the Plotly dashboards. To access the dashboards, follow these steps:

1. Install the required dependencies listed in the **dashboard/requirements.txt** file.
2. Run the main.py script to start the dashboard server.
3. Open a web browser and navigate to the URL provided by the dashboard server.
4. Use the interactive widgets and charts to explore the data.

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

Our data architecture diagram utilizes several AWS services to collect, store, and manage data. The architecture consists of an API, AWS Lambda functions, Amazon RDS, and Amazon S3.

![DAD](https://i.ibb.co/BnXPnmy/image.png)

### API

We use an external API, https://data-eng-plants-api.herokuapp.com/, to retrieve data about various plant species. The API returns information about plant origin, sunlight requirements, plant cycles, and other relevant data points.

### AWS Lambda

We have two AWS Lambda functions. The first function, minutely, retrieves the data from the external API and stores it into the RDS database every minute. The second function, daily, retrieves the data from the RDS database once a days, transforms it into CSV format, and uploads it to Amazon S3.

### Amazon RDS

We use Amazon RDS as our relational database to store and manage the data collected from the external API.

### Amazon S3

The transformed data is then stored in Amazon S3, where it can be accessed by downstream applications. This provides us with a centralized location for storing and sharing data with other applications.

![tree](https://i.pinimg.com/originals/eb/54/d4/eb54d4191a91f9ff3c2f9a198471136b.gif)
<br>

🌱🌿🍃🌵🌿🍃🌵🌱🌿🍃🌵🌿🍃🌵🌱🌿🍃🌵🌿🍃🌵🌱🌿🍃🌵🌿🍃🌵

## Licenses

This project uses the following third-party software and tools, each with its own licensing terms:

- AWS services and tools: AWS offers a variety of services and tools, each with its own licensing terms. You can find more information about AWS licenses on their [website](https://aws.amazon.com/legal/).
- Docker: Docker is released under the Apache 2.0 license. See [here](https://www.apache.org/licenses/LICENSE-2.0) for more information about the Apache 2.0 license.
- Terraform: Terraform is released under the Apache 2.0 license. See [here](https://www.apache.org/licenses/LICENSE-2.0) for more information about the Apache 2.0 license.
