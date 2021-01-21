import json
import os
import ast
import argparse
import azureml.core
from azureml.core import Run
from azureml.pipeline.steps.hyper_drive_step import HyperDriveStepRun

def get_runtime_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', type=str)
    args = parser.parse_args()
    return args

def main():
    args = get_runtime_args()
    model_name = args.model_name
    
    # current run is the registration step
    current_run = Run.get_context()

    # parent run is the overall pipeline
    parent_run = current_run.parent

    # Get the HyperDriveStep of the pipeline by name (make sure only 1 exists)
    hd_step_run = HyperDriveStepRun(step_run=parent_run.find_step_run('hyperparameter-tuning')[0])

    # Get RunID for best run
    best_run = hd_step_run.get_best_run_by_primary_metric()
    best_run_id = best_run.id

    # Get the best run's metrics and hyperparameters
    hyperparameters = ast.literal_eval(hd_step_run.get_hyperparameters()[best_run_id].replace('--', ''))
    metrics = hd_step_run.get_metrics()[best_run_id]

    best_run.register_model(model_path='outputs/model.pkl',
                            model_name=model_name,
                            properties={**metrics, **hyperparameters})

if __name__ == "__main__":
    main()