import os
import glob
import json
import argparse
import numpy as np
import pandas as pd
import joblib

from azureml.core.model import Model
from azureml.core import Run

current_run = None
model = None

def init():
    print("Started batch scoring by running init()")

    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', type=str, help='Model to use for batch scoring')
    args, _ = parser.parse_known_args()

    global current_run
    current_run = Run.get_context()

    print(f'Arguments: {args}')
    print(f'Model name: {args.model_name}')
  
    global model
    model_path = Model.get_model_path(args.model_name)
    model = joblib.load(model_path)

def run(file_list):
    try:
        output_df = pd.DataFrame(columns=["Sno", "ProbaGoodCredit", "ProbaBadCredit"])
        for filename in file_list:
            df = pd.read_csv(filename)

            sno = df["Sno"]
            df = df.drop("Sno", axis=1)

            proba = model.predict_proba(df)
            proba = pd.DataFrame(data=proba, columns=["ProbaGoodCredit", "ProbaBadCredit"])
            result = pd.concat([sno, proba], axis=1)
            output_df = output_df.append(result)

            print(f'Batch scored: {filename}')

        return output_df
    except Exception as e:
        error = str(e)
        return error

if __name__ == "__main__":
    test()