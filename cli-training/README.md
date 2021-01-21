# Exercise Instructions

This exercise shows how to train and register a model using the `az ml` CLI. We'll cover using `azureml` and `mlflow` for metrics logging. I'd recommend to run these commands in the Jupyter or JupyterLab's Terminal. When using your own laptop, make sure you have the [CLI extension for Azure Machine Learning](https://docs.microsoft.com/en-us/azure/machine-learning/reference-azure-machine-learning-cli) installed.

### Attach to folder for authentication

Let's first set the default workspace and resource group for the folder we are in. This will also include subfolders and later allows us to not always having to specify the workspace and resource group in each call.

```console
cd azure-machine-learning-mlops-workshop/
az ml folder attach -g <your resource group> -w <your workspace name>
cd cli-training/
```

## Training a model from the CLI

### Local training (no AML)

If you want, you can run the example fully locally in Python. In this case, if you do not have the necessary libraries installed, you can create a new conda environment:

```console
conda create env -f config/conda.yml
conda activate workshop-env
```

Next, you can run the training script with the data from this repo:

```console
python train.py --data-path ../data-training/
```

This won't log to AML at all, as we run in so called "offline-mode". The statement `run = Run.get_context()` is just skipped and `run.log('Train accuracy', train_acc)` just logs to `STDOUT`. This is useful if you want to develop your code locally and write it against a small dataset.

### Training on AML Compute Cluster

Since we are already happy with our training script, we can now run it in AML on a Compute Cluster. Typically you'd probably already have data in Azure Blob or Data Lake, but here we need to simulate it and then registering a Dataset from it. Typically, I'd recommend registering Dataset in the Studio UI:

```console
# Upload data
az ml datastore upload -n workspaceblobstore --src-path ../data-training/ --target-path cli-training-tutorial/

# Register data as Dataset in AML
az ml dataset register -f dataset.json --skip-validation
```

Next, we can create a Compute Cluster:

```console
az ml computetarget create amlcompute -n cpu-cluster --max-nodes 1 -s STANDARD_D3_V2 --idle-seconds-before-scaledown 1800
```

Finally, we can run the training on a Compute Cluster:

```console
az ml run submit-script -c config/train-aml -e german-credit-train-amlcompute -t run.json
```

This will do exactly the same as locally, but everything will happen in Azure. The command options are the following:

* The `-c` option specifies the runconfig and points to [`config/train-aml.runconfig`](config/train-aml.runconfig) (the extension `.runconfig` does not need to be specified). 
* The `-e` optino refers to the experiment name, under which the run should be logged
* The `-t` option outputs a reference to the experiment run (optionnal), which can be used to directly register the model from it. 

Let's have a look at the runconfig in detail:

```yaml
script: train.py # Defines the script we want to run for training
arguments: [--data-path, /data] # Defines the arguments for our training script
target: cpu-cluster # The target Compute Cluster in AML
framework: Python
environment:
  environmentVariables:
    EXAMPLE_ENV_VAR: EXAMPLE_VALUE
  python:
    userManagedDependencies: false
    interpreterPath: python
    condaDependenciesFile: config/conda.yml # Points to our conda environment definition, used by our script
  docker:
    enabled: true
    baseImage: mcr.microsoft.com/azureml/base:intelmpi2018.3-ubuntu16.04
    sharedVolumes: true
data:
  training_dataset: # Just a placeholder name, that is shown in the Studio UI
    dataLocation:
      dataset:
        name: cli-training-tutorial # Reference the Dataset name
        version: 1 # Pick the version
    mechanism: download # Select 'mount' or 'download' (use download if data fits in the cluster)
    pathOnCompute: /data # Mountpath for the data, passed into arguments (see above)
    environmentVariableName: training_dataset
    createOutputDirectories: false
    overwrite: false
```

### Training on AML Compute Cluster with mlflow

Let's say you want to use mlflow for metric tracking within your code - this means, you code will stay free of `import azureml.*`. In this case, we'll use the mlflow-native imports in your `train-mlflow.py`

```python
import mlflow
import mlflow.sklearn

...
mlflow.sklearn.autolog()
mlflow.log_metric('Train accuracy', train_acc)
...
```

We can then run the training via:

```console
az ml run submit-script -c config/train-aml-mlflow -e german-credit-train-amlcompute
```

In this case, have a look at Conda environment [`config/conda-mlflow.yml`](config/conda-mlflow.yml).

### Summary

So in summary, to train a model on AML Compute Cluster, you'll need:

* Your training code
* An AML Compute Cluster
* An AML Dataset with the training data
* A `runconfig` file (job definition)
* A conda environment yaml

This will allow you to quickly offload model training to AML.

## Registering a model from the CLI

```console
az ml model register --name test-model --asset-path outputs/model.pkl --run-metadata-file run.json
```

## Cleanup

```console
az ml model delete --model-id test-model:1
```

# Knowledge Check

:question: **Question:** How does the Compute Cluster from where it should the training data?
<details>
  <summary>:white_check_mark: See solution!</summary>

This is defined in [`config/train-aml.runconfig`](config/train-aml.runconfig), in the `data` and `arguments` section:

```yaml
data:
  training_dataset:
    dataLocation:
      dataset:
        name: cli-training-tutorial # Dataset reference
        version: 1 # Pick the version
    mechanism: download # Select 'mount' or 'download' (use download if data fits in the cluster)
    pathOnCompute: /data # Mountpath for the data, passed into arguments
```

Then in the `arguments` section, we point the script to load the data from `/data`:

```yaml
arguments: [--data-path, /data] # Defines the arguments for our training script
```

Obviously, this require that our script is able to load the data from a folder and knows how to deal with what's in this folder.
</details>