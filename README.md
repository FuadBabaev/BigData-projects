# Big Data Projects Repository

This repository contains a collection of projects focused on big data processing, machine learning model training, and deployment using various tools and frameworks such as Hadoop, Spark, and MLflow. Each project demonstrates the application of these technologies to solve specific data-driven problems.

## Projects

### Project 1: Hadoop Streaming for Click Prediction

In this project, we implemented a solution to predict the probability of a click on an ad banner using the Criteo Dataset. The training occurs on a local machine, while filtering and prediction are performed in a distributed manner using Hadoop Streaming. The solution includes:
- Model training script
- Prediction script using Hadoop Streaming
- Filtering and combined filtering-prediction scripts

### Project 2: Spark ML for Product Rating Prediction

This project involves predicting the rating of a product based on its text review using Spark ML. The dataset consists of reviews from Amazon. The solution includes:
- Model pipeline definition using Spark ML
- Training script that processes the input data, trains the model, and saves it
- Prediction script that loads the trained model and makes predictions on new data

### Project 3: Shortest Path in a Graph with Spark

In this project, we implemented an algorithm to find the shortest path between two vertices in a graph using the Breadth-First Search (BFS) algorithm. The dataset is a snapshot of the Twitter social network graph. The solution includes:
- Spark script to find the shortest paths
- Handling of cycles in the graph
- Saving the shortest paths in HDFS

### Project 4: Hive for Distributed Query Processing

This project demonstrates the use of Hive for processing large datasets. We used Hive to perform predictions and filtering on a large-scale dataset, similar to previous projects but using Hive queries for distributed processing.

### Project 5: Model Training and Deployment with MLflow

In this project, we trained a machine learning model using `sklearn` and logged the parameters, metrics (log_loss), and the model itself using MLflow. The project includes:
- Definition of the model pipeline
- Training script that logs information to MLflow
- Prediction script that uses the trained model for inference
- Setting up and using MLflow tracking server and model serving

## Technologies Used

- **Hadoop Streaming**: For distributed data processing and predictions.
- **Apache Spark**: For scalable machine learning model training and graph processing.
- **Apache Hive**: For distributed query processing on large datasets.
- **MLflow**: For model tracking, logging, and deployment.

## Getting Started

To get started with any of the projects, navigate to the respective project directory and follow the instructions provided in the README file within that directory. Ensure that you have the required dependencies and configurations set up as mentioned in the project-specific documentation.

