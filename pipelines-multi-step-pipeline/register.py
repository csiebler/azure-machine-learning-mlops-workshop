import os
import argparse
from azureml.core import Run, Dataset
from azureml.pipeline.core import PipelineRun

parser = argparse.ArgumentParser()
parser.add_argument('--model_name', type=str, help='Name under which model will be registered')
parser.add_argument('--model_path', type=str, help='Model directory')
args, _ = parser.parse_known_args()

print(f'Arguments: {args}')

# current run is the registration step
current_run = Run.get_context()
ws = current_run.experiment.workspace

# parent run is the overall pipeline
parent_run = current_run.parent
print(f'Parent run id: {parent_run.id}')

pipeline_run = PipelineRun(parent_run.experiment, parent_run.id)

training_run = pipeline_run.find_step_run('train-step')[0]
print(f'Training run: {training_run}')

prepare_run = pipeline_run.find_step_run('prepare-step')[0]
print(f'Prepare run: {prepare_run}')

# Retrieve input training datasets
datasets = []
details = prepare_run.get_details()
for d in details['inputDatasets']:
    print(f'Dataset info: {d}')
    name = d['consumptionDetails']['inputName']
    dataset = d['dataset']
    datasets.append([name, dataset])

# Register model
model = training_run.register_model(model_name=args.model_name,
                                    model_path=args.model_path,
                                    datasets=datasets)