# Exercise Instructions

## Prerequisites

Before starting with the exercises, make sure that you have the following in place:

* An Azure Machine Learning workspace
   * Follow this [tutorial](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-manage-workspace#create-a-workspace), no need to configure the networking section!
* A Compute Instance, running in your workspace (`Standard_D2_v2` is sufficient)
  * Goto [AML Studio (https://ml.azure.com)](https://ml.azure.com), sign-in, then select `Compute`, then `Compute instance` and click `Create`
  * Give it any name, select `Standard_D2_v2` as size and hit create - done!

## Running this on a Compute Instance (recommended)

We recommend to run these exercises on a Compute Instance on Azure Machine Learning. To get started, open Jupyter or JupyterLab on the Compute Instance, select `New --> Terminal` (upper right corner) and clone this repo:

```console
git clone https://github.com/csiebler/azure-machine-learning-mlops-workshop.git
cd azure-machine-learning-mlops-workshop/
```

Then navigate to the cloned folder in Jupyter, and open [`single_step_pipeline.ipynb`](single_step_pipeline.ipynb) from this exercise. In case you're asked for a kernel, please use the `Python 3.6 - AzureML` kernel that comes with the Compute Instance.

## Running this on your own machine

1. Provision an Azure Machine Learning Workspace in Azure
1. Install the [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
1. Login to your Azure subscription via `az login`
1. Make sure you are in the correct subscription (the one of your workspace):
    * `az account list` lists all your subscriptions
    * `az account set -s '<SUBSCRIPTION_ID or NAME>'` sets the default one that the CLI should use
1. Install the Azure Machine Learning CLI extensive via `az extension add -n azure-cli-ml`
1. Clone this repo via `git clone https://github.com/csiebler/azure-machine-learning-mlops-workshop.git`
1. Navigate into the repo `cd azure-machine-learning-mlops-workshop/`
1. Attach the whole repo to your workspace via `az ml folder attach -w <YOUR WORKSPACE NAME> -g <YOUR RESOURCE GROUP>`
1. Fire up your favorite notebook experience and get started!

# Knowledge Check

:question: **Question:** From where does `train_step = PythonScriptStep(name="train-step", ...)` know which Python dependencies to use?
<details>
  <summary>:white_check_mark: See solution!</summary>

It uses the AML environment `workshop-env` which we created in the first step. This environment was created using the `conda.yml`. We could have defined all this in Python, but having the conda enviroment in a separate file, allows us to easier test this locally, e.g., by using:

```
conda env create -f conda.yml
python train.py --data-path ../data-training
``` 
</details>

:question: **Question:** How can we make a compute cluster scale down quicker/slower?
<details>
  <summary>:white_check_mark: See solution!</summary>

We can adapt `idle_seconds_before_scaledown=3600`, which defines the idle time until the cluster scales down to 0 nodes.
</details>

:question: **Question:** From where does `ws = Workspace.from_config()` how to which workspace it needs to connect?
<details>
  <summary>:white_check_mark: See solution!</summary>

The call `Workspace.from_config()` has the following behaviour:
* Inside a Compute Instance, it resolves to the workspace of the current instance
* If a `config.json` file is present, it loads the workspace reference from there (you can download this file from the Studio UI, by clicking the book icon on the upper right):

```json
{
    "subscription_id": "*****",
    "resource_group": "aml-mlops-workshop",
    "workspace_name": "aml-mlops-workshop"
}
```
* Use the az CLI to connect to the workspace and use the workspace attached to via `az ml folder attach -g <resource group> -w <workspace name>`
</details>

:question: **Question:** What is the difference between `PublishedPipeline` and `PipelineEndpoint`?
<details>
  <summary>:white_check_mark: See solution!</summary>

* [`PublishedPipeline`](https://docs.microsoft.com/en-us/python/api/azureml-pipeline-core/azureml.pipeline.core.graph.publishedpipeline?view=azure-ml-py) allows to publish a pipeline as a RESTful API endpoint, from which it can be invoked. Each `PublishedPipeline` will have a new URL endpoint.
* [`PipelineEndpoint`](https://docs.microsoft.com/en-us/python/api/azureml-pipeline-core/azureml.pipeline.core.pipelineendpoint?view=azure-ml-py) allows to "hide" multiple `PublishedPipeline`s behind a single URL and routes the request to a specific default version. This enables to continously update the `PipelineEndpoint` with new `PublishedPipeline`s while the URL stays the same. Hence, the consumer will not notice that the pipeline got "swapped out", "replaced" or "changed". This is very helpful when we want to test pipelines before we release or hand them over to the pipeline consumer.
</details>
