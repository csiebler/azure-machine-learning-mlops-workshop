# Exercise Instructions

## Running this on a Compute Instance (recommended)

We recommend to run these exercises on a Compute Instance on Azure Machine Learning. To get started, open Jupyter or JupyterLab on the Compute Instance, select `New --> Terminal` (upper right corner) and clone this repo:

```cli
git clone https://github.com/csiebler/azure-machine-learning-mlops-workshop.git
cd azure-machine-learning-mlops-workshop/
```

Then navigate to the cloned folder in Jupyter, and open [`pipeline.ipynb`](pipeline.ipynb) from this exercise. In case you're asked for a kernel, please use the `Python 3.6 - AzureML` kernel that comes with the Compute Instance.

## Running this on your own machine

1. Install the [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
1. Login to your Azure subscription via `az login`
1. Install the Azure Machine Learning CLI extensive via `az extension add -n azure-cli-ml`
1. Clone this repo via `git clone https://github.com/csiebler/azure-machine-learning-mlops-workshop.git`
1. Navigate into the repo `cd azure-machine-learning-mlops-workshop/`
1. Attach the whole repo to your workspace via `az ml folder attach -w <YOUR WORKSPACE NAME> -g <YOUR RESOURCE GROUP>`
1. Fire up your favorite notebook experience and get started!

# Knowledge Check

**Question:** From where does `train_step = PythonScriptStep(name="train-step", ...)` know which Python dependencies to use?
<details>
  <summary>See solution!</summary>

  :white_check_mark: It uses the file `runconfig.yml`, which further defines the step's configuration. The runconfig points to `condaDependenciesFile: conda.yml`, which defines the conda enviroment, in which this step is executed in. We could have defined all this in Python, but having the conda enviroment in a separate file, allows us to easier test this locally, e.g., by using:

  ```
  conda env create -f conda.yml
  python train.py --data-path ../data-training
  ``` 
</details>

**Question:** How can we make a compute cluster scale down quicker/slower?
<details>
  <summary>See solution!</summary>

  :white_check_mark: We can adapt <code>idle_seconds_before_scaledown=3600</code>, which defines the idle time until the cluster scales down to 0 nodes.
</details>

**Question:** From where does `ws = Workspace.from_config()` how to which workspace it needs to connect??
<details>
  <summary>See solution!</summary>

  :white_check_mark: The call <code>Workspace.from_config()</code> has the following behaviour:
  * Inside a Compute Instance, it resolves to the workspace of the current instance
  * If a <code>config.json</code> file is present, it loads the workspace reference from there (you can download this file from the Studio UI, by clicking the book icon on the upper right):

```json
    {
        "subscription_id": "*****",
        "resource_group": "aml-mlops-workshop",
        "workspace_name": "aml-mlops-workshop"
    }
```
  * Use the az CLI to connect to the workspace and use the workspace attached to via <code>az ml folder attach -g <resource group> -w <workspace name></code>
</details>