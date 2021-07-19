import json
import os
import numpy as np
import pandas as pd
import joblib
from inference_schema.schema_decorators import input_schema, output_schema
from inference_schema.parameter_types.standard_py_parameter_type import StandardPythonParameterType
from azureml.monitoring import ModelDataCollector

# Automatically generate the swagger interface by providing an data example
input_sample = [{
    "Age": 20,
    "Sex": "male",
    "Job": 0,
    "Housing": "own",
    "Saving accounts": "little",
    "Checking account": "little",
    "Credit amount": 100,
    "Duration": 48,
    "Purpose": "radio/TV"
  }]
output_sample = [[0.7, 0.3]]

def init():
    global model

    model_filename = 'model.pkl'

    # AZUREML_MODEL_DIR is injected by AML
    model_dir = os.getenv('AZUREML_MODEL_DIR')
    model = joblib.load(os.path.join(model_dir, model_filename))
    
    # Setup Data Collection
    global inputs_dc
    global predictions_dc
    inputs_dc = ModelDataCollector("best_model", designation="inputs", feature_names=["Age", "Sex", "Job", "Housing", "Saving accounts", "Checking account", "Credit amount", "Duration", "Purpose"])
    predictions_dc = ModelDataCollector("best_model", designation="predictions", feature_names=["good", "bad"])

@input_schema('data', StandardPythonParameterType(input_sample))
@output_schema(StandardPythonParameterType(output_sample))
def run(data):
    try:
        # Predict
        df = pd.DataFrame(data)
        proba = model.predict_proba(df)
        result = {"predict_proba": proba.tolist()}

        # Collect data
        correlations = inputs_dc.collect(df)
        predictions_data = predictions_dc.add_correlations(proba, correlations)
        predictions_dc.collect(predictions_data)

        return result
    except Exception as e:
        error = str(e)
        return error