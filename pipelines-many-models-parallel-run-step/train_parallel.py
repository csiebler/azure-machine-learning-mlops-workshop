import os
import glob
import json
import argparse
import numpy as np
import pandas as pd

from azureml.core import Run
from train import train_model

current_run = None
model_output_path = None

def init():
    print("Started many model training by running init()")

    parser = argparse.ArgumentParser()
    parser.add_argument('--model_output_path', type=str, help='Model output directory')
    args, _ = parser.parse_known_args()
    
    global model_output_path
    model_output_path = args.model_output_path

    global current_run
    current_run = Run.get_context()


def run(file_list):
    
    results = []
    try:
        print(f"Training model on the following files: {file_list}")

        # Only use first file for model training in this example
        train_file = file_list[0]
        path = os.path.dirname(train_file)
        model_name = os.path.basename(path)      
        model_filename = model_name + '.pkl'
        
        print(f"Training model {model_name} using file {train_file}")
        test_accuracy = train_model(train_file, os.path.join(model_output_path, model_filename))
        
        # append success, as AzureML uses this to check if our batch was successful
        results.append(f"{model_name}, {model_filename}, {train_file}, {test_accuracy}")

    except Exception as e:
        error = str(e)
        return error
    return results

if __name__ == "__main__":
    print("I need to be written")