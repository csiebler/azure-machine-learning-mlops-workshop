# Exercise Instructions

This exercise shows how to train and register a R model using the `az ml` CLI. I'd recommend to run these commands in the Jupyter or JupyterLab's Terminal. When using your own laptop, make sure you have the [CLI extension for Azure Machine Learning](https://docs.microsoft.com/en-us/azure/machine-learning/reference-azure-machine-learning-cli) installed.

### Attach to folder for authentication

Let's first set the default workspace and resource group for the folder we are in. This will also include subfolders and later allows us to not always having to specify the workspace and resource group in each call.

```console
cd azure-machine-learning-mlops-workshop/
az ml folder attach -g <your resource group> -w <your workspace name>
cd cli-with-r/
```

## Training a model from the CLI

### Local training (no AML)

If you want, you can run the example fully locally in R. In this case, make sure you have the required libraries installed:

```console
R train.R --data-path data/
```

This won't log to AML at all, as we run in so called "offline-mode". The statement `run <- get_current_run()` is just skipped and `log_metric_to_run("Accuracy", accuracy, run=run)` just logs to `STDOUT`. This is useful if you want to develop your code locally and write it against a small dataset.

### Training on AML Compute Cluster

Since we are already happy with our training script, we can now run it in AML on a Compute Cluster. Typically you'd probably already have data in Azure Blob or Data Lake, but here we need to simulate it and then registering a Dataset from it. Typically, I'd recommend registering Dataset in the Studio UI:

```console
# Upload data
az ml datastore upload -n workspaceblobstore --src-path data/ --target-path cli-with-r-tutorial/

# Register data as Dataset in AML
az ml dataset register -f dataset.json --skip-validation
```

Next, we can create a Compute Cluster:

```console
az ml computetarget create amlcompute -n cpu-cluster --max-nodes 1 -s STANDARD_D3_V2 --idle-seconds-before-scaledown 1800
```

Now, since R takes a while to build, it makes sense to pre-built a Docker image with our required libraries. See the provided [`Dockerfile`](./Dockerfile) as an example and feel free to add more dependencies

```console
az acr build --registry amlsharedclemens --image r-tutorial:v1 .
```

Once the build has finished (this might take quite a while), note down the image name (in this example `xxxxxxxxx.azurecr.io/r-tutorial:v1`):

```console
...
2021/02/01 17:37:25 Successfully pushed image: xxxxxxxxx.azurecr.io/r-tutorial:v1
2021/02/01 17:37:25 Step ID: build marked as successful (elapsed time in seconds: 1671.289653)
...
```

Now, we need to update our [`config/train-aml.runconfig`](config/train-aml.runconfig) to use this new image:

```yaml
  docker:
    enabled: true
    baseImage: axxxxxxxxx.azurecr.io/r-tutorial:v1 # replace with your image
    sharedVolumes: true
```

Finally, we can run the training on a Compute Cluster:

```console
az ml run submit-script -c config/train-aml -e cli-r-tutorial -t run.json
```

This will do exactly the same as locally, but everything will happen in Azure. The command options are the following:

* The `-c` option specifies the runconfig and points to [`config/train-aml.runconfig`](config/train-aml.runconfig) (the extension `.runconfig` does not need to be specified). 
* The `-e` optino refers to the experiment name, under which the run should be logged
* The `-t` option outputs a reference to the experiment run (optionnal), which can be used to directly register the model from it. 

Let's have a look at the runconfig in detail:

```yaml
script: train.R # Defines the script we want to run for training
arguments: [--data_path, /data] # Defines the arguments for our training script
target: cpu-cluster # The target Compute Cluster in AML
framework: R
environment:
  environmentVariables:
    EXAMPLE_ENV_VAR: EXAMPLE_VALUE
  python:
    userManagedDependencies: true # Set to true, as we will rely on our pre-built Docker image
  docker:
    enabled: true
    baseImage: xxxxx.azurecr.io/r-tutorial:v1 # our Docker image with all R dependencies
    sharedVolumes: true
data:
  training_dataset: # Just a placeholder name, that is shown in the Studio UI
    dataLocation:
      dataset:
        name: cli-with-r-tutorial # Reference the Dataset name
        version: 1 # Pick the version
    mechanism: download # Select 'mount' or 'download' (use download if data fits in the cluster)
    pathOnCompute: /data # Mountpath for the data, passed into arguments (see above)
    environmentVariableName: training_dataset
    createOutputDirectories: false
    overwrite: false
```

## Registering a model from the CLI

You can register the model within the run through the following command:

```console
az ml model register --name r-model --asset-path outputs/model.rds --run-metadata-file run.json
```

## Cleanup

If you want, you can delete the model via:

```console
az ml model delete --model-id r-model:1
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