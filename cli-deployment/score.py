import os
import json
import numpy as np
import pandas as pd
import joblib

def init():
    global model

    model_filename = 'model.pkl'

    # AZUREML_MODEL_DIR is injected by AML
    model_dir = os.getenv('AZUREML_MODEL_DIR')
    model = joblib.load(os.path.join(model_dir, model_filename))

def run(raw_data):
    try:
        data = json.loads(raw_data)['data']
        input_df = pd.DataFrame.from_dict(data)
        proba = model.predict_proba(input_df)
        result = {"predict_proba": proba.tolist()}
        return result
    except Exception as e:
        error = str(e)
        return error