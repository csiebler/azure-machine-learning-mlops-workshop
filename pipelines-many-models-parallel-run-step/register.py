import os
import argparse
from azureml.core import Run

parser = argparse.ArgumentParser()
parser.add_argument('--model_name', type=str, help='Name under which the models will be registered')
parser.add_argument('--model_path', type=str, help='Model directory')
args, _ = parser.parse_known_args()

print(f'Arguments: {args}')
model_name = args.model_name
model_path = args.model_path

# current run is the registration step
current_run = Run.get_context()

# parent run is the overall pipeline
parent_run = current_run.parent
print(f'Parent run id: {parent_run.id}')

# Upload models to pipeline artifacst and register a model from them
parent_run.upload_folder(name='models', path=model_path)
parent_run.register_model(model_path='models', model_name=model_name)