import os
import azureml.core
from azureml.core import Workspace
from azureml.pipeline.core import Pipeline, PublishedPipeline, PipelineEndpoint

print(f'Azure ML SDK version: {azureml.core.VERSION}')

endpoint_name = "training-pipeline-endpoint"
pipeline_id = os.getenv('PIPELINE_ID')

# Connect to the workspace
ws = Workspace.from_config()
print(f'WS name: {ws.name}')
print(f'Region: {ws.location}')
print(f'Subscription id: {ws.subscription_id}')
print(f'Resource group: {ws.resource_group}')

print(f'Pipeline ID: {pipeline_id}')
published_pipeline = PublishedPipeline.get(workspace=ws, id=pipeline_id)
print(f'Published Pipeline: {published_pipeline}')

# Check if PipelineEndpoint already exists
if any(pe.name == endpoint_name for pe in PipelineEndpoint.list(ws)):
    print(f'Pipeline Endpoint with name {endpoint_name} already exists, will add pipeline to it')
    pipeline_endpoint = PipelineEndpoint.get(workspace=ws, name=endpoint_name)
    pipeline_endpoint.add(published_pipeline)
    # Set it to default, as we already tested it beforehand!
    pipeline_endpoint.set_default(published_pipeline)
else:
    print(f'Will create Pipeline Endpoint with name {endpoint_name}')
    pipeline_endpoint = PipelineEndpoint.publish(workspace=ws,
                                                name=endpoint_name,
                                                pipeline=published_pipeline,
                                                description="New Training Pipeline Endpoint")