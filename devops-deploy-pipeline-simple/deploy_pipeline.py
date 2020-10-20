import os
import azureml.core
from azureml.core import Workspace, Experiment, Dataset, RunConfiguration
from azureml.pipeline.core import Pipeline, PipelineData, PipelineParameter
from azureml.pipeline.steps import PythonScriptStep
from azureml.data.dataset_consumption_config import DatasetConsumptionConfig

# AML Pipeline defaults (hardcoded for the sake of the workshop)
source_directory = "pipelines-single-training-step/"
default_training_dataset = Dataset.get_by_name(ws, "german-credit-train-tutorial")

print("Azure ML SDK version:", azureml.core.VERSION)

# Connect to the workspace
ws = Workspace.from_config()
print(f'WS name: {ws.name}')
print(f'Region: {ws.location}')
print(f'Subscription id: {ws.subscription_id}')
print(f'Resource group: {ws.resource_group}')

# Parametrize dataset input to the pipeline
training_dataset_parameter = PipelineParameter(name="training_dataset", default_value=default_training_dataset)
training_dataset_consumption = DatasetConsumptionConfig("training_dataset", training_dataset_parameter).as_download()

# Load runconfig from earlier exercise and create pipeline
runconfig = RunConfiguration.load(os.path.join(source_directory, "runconfig.yml"))

train_step = PythonScriptStep(name="train-step",
                        source_directory=source_directory,
                        script_name="train.py",
                        arguments=['--data-path', training_dataset_consumption],
                        inputs=[training_dataset_consumption],
                        runconfig=runconfig,
                        allow_reuse=False)

steps = [train_step]

pipeline = Pipeline(workspace=ws, steps=steps)
pipeline.validate()
published_pipeline = pipeline.publish('training-pipeline')

# Printing the pipeline's id this way will make it available in Azure DevOps for the subsequent tasks
print(f'##vso[task.setvariable variable=pipeline_id]{published_pipeline.id}')
