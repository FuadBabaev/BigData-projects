# Homework 5: Model Training and Prediction using MLflow

## Overview

Train a model using `sklearn`, log the parameters, metrics (log_loss), and the model itself using MLflow version 2.10.2. This task should be executed on the login node only, without using the cluster.

## Task

- Use your model and `train.py` from Homework 1.
- Add code to log parameters, metrics (log_loss), and the model using MLflow.
- Ensure at least one model parameter is passed to `train.py`.

## Project Structure

Create a directory `projects/5mla` in your private repository `ai-masters-bigdata`. The directory should contain the following files:

1. **MLProject** - Entry point `main` should have at least two parameters: 
   - `train_path`: Path to the training dataset.
   - `model_param1`: Any parameter of your model with a default value.

2. **conda.yaml** - File to create a virtual Python environment with required packages.

3. **train.py** - Should accept at least two arguments:
   - `train_path`
   - `model_param1`

You can either define the model in `model.py` as in Homework 1 or within `train.py`.

## Checking Your Work

### Preparation

1. Commit your code to the repository and sync with GitHub.
2. Add the following lines to `.gitignore` to ensure MLflow data is not included in your repo:
   ```
   mlruns
   *.sqlite
   ```

### Execution

1. If you developed on your laptop/desktop, clone your repo on the server.
2. Activate the `dsenv` environment using `conda activate dsenv` which includes MLflow.
3. In one terminal window, navigate to your home directory and start the tracking server using SQLite as the backend store and `./mlruns` as the artifact store. The port should be `5000 + your user ID` obtained from `id -u`. If the connection is lost, kill any running `gunicorn` processes before restarting the server.
4. In another terminal window, activate `dsenv` again and set the `MLFLOW_TRACKING_URI` environment variable to `http://localhost:port` (use the port number as described above). Navigate to the `projects/5mla` folder.
5. Train the model using:
   ```sh
   mlflow run . -P train_path=/home/users/datasets/criteo/train1000.txt --env-manager=local
   ```
   The `--env-manager=local` option prevents the creation of a new environment and ensures execution within the activated `dsenv`.

6. Verify that the backend recorded a successful run with the run ID, model parameters including `model_param1`, log_loss metric, and the model in artifacts using `mlflow ui` or `mlflow runs`.

7. Start the model inference service:
   ```sh
   mlflow models serve -m models:/your_model_name/1 -p 6000 + id -u --env-manager=local
   ```

## Notes

- The task should be completed on the login node only.
- Ensure all MLflow-related data is excluded from the repository by updating `.gitignore`.

For further assistance, refer to the [MLflow documentation](https://mlflow.org/docs/latest/index.html).
