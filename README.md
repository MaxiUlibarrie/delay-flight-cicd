# Delay Flight CI/CD
This project is to create a CI/CD environment for a model to predict delay flights probabilities.

This diagram shows the pipeline to update the new model adn deploy it into Heroku. 

![Alt text](/assets/flow.jpg)

The pipeline is based on two principals processes: train and backend (both managed by Dockerfile.train and Dockerfile.backend respectively)

# common folder
Located in `common/`. Used for config file where we can find all the constants and important information for all modules in the project.

## config.yml
It has constant information for all modules (for training and backend)

## config_handler 
It takes the config.yml and create a Singleton module to easy access the information.

## log_handler 
Singleton module to log all information to the console.

## credential_decode
Prepare important information to be used for DVC and retrieve dataset and model from Firebase bucket.

# Pipeline 'train' (pipeline/train)
It has all the important modules for prepare the training data and train the model depending on config file.

In the config file (section 'base') the model expert can configure the features for the model.

Note: In the case the model only has categoric features but if in the future the model expert determine to add numeric features, this can be easily added in `base.features.numeric` and add the proper treatment on `prepare.py` script.

## main.py
Run all the modules to prepare the training data and train the model.

## prepare.py
Prepare the `train.csv` data for training using models from `models.py` as DataPreparer and DataTrasnformer.

## models.py 
Define DataPreparer and DataTransformer to organize the needed transformations to produce training data.

* **DataTransformer:** abstract class to define one step in the transformation of the data in order to generate the train data.
* **DataPreparer:** class to orchestrate the steps (or data transformations) to produce the training data.

## train.py
Train the model with the training data.

## report.py
Defines reports used in train process.

## update_model.sh
Upload the new model to the Firebase bucket with DVC.

# Pipeline 'backend' (pipeline/backend)
It has all the modules to deploy the new model to Heroku.

## models.py
Defines the models for the FastAPI API REST.

* **DelayFlightRequest:** it takes the features from the config.yml (`backend.request_features`) to create dynamically the request model. In this case we can add new fearures depending on the decisions of the model expert.
* **DelayFlightResponse:** model response with the prediction.
* **DelayFlightModel:** retrieve the current model from the Firebase bucket using DVC and it use it to make predictions.

## main.py
Instantiates the models to get the FastAPI service up.
