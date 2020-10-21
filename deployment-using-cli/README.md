# Exercise Instructions

This exercise shows how to register and deploy a model using the `az ml` CLI. I'd recommend to run these commands in the Jupyter or JupyterLab's Terminal.

### Attach to folder for authentication

Let's first set the default workspace and resource group for the folder we are in. This will also include subfolders and later allows us to not always having to specify the workspace and resource group in each call.

```cli
cd azure-machine-learning-mlops-workshop/
az ml folder attach -g <your resource group> -w <your workspace name>
cd deployment-using-cli/
```

## Using the CLI for model registration

Let's first register the model using the CLI:

```cli
az ml model register --name credit-model --model-path model.pkl
```

The model should now show up in the Studio UI under `Models`.

## Using the CLI for model deployment to Azure Container Instances

Now, we can deploy our model to Azure. We'll start with deployment to Azure Container Instances (ACI):

```cli
az ml model deploy -n credit-model-aci -m credit-model:1 --inference-config-file config/inference-config.yml --deploy-config-file config/deployment-config-aci-qa.yml --overwrite
```

* `-n` refers to the deployment name
* `-m` refers to the registered model and its version
* `--inference-config-file` defines the runtime environment for our model
* `--deploy-config-file` defines on what infrastructure the deployment should happen

We can test the ACI endpoint using the following request (make sure to replace the URL with your container's URL). You can find the same code also in [`test_webservice.ipynb`](test_webservice.ipynb):

```python
import requests

url = 'http://xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx.xxxxxx.azurecontainer.io/score'

test_data = {
  'data': [{
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
}

headers = {'Content-Type': 'application/json'}
response = requests.post(url, json=test_data, headers=headers)

print("Prediction (good, bad):", response.text)
```

## Using the CLI for model deployment to Azure Kubernetes Service

Before we can deploy to Azure Kubernetes Service (AKS), we first need to create a small cluster (we use `DevTest` for a single node cluster):

```cli
az ml computetarget create aks --name aks-cluster --cluster-purpose DevTest
```

Now, we can deploy to it - only difference is that we use a differnet deployment config and are required to specify to which cluster we want to deploy:

```cli
az ml model deploy -n credit-model-aks -m credit-model:1 --compute-target aks-cluster --inference-config-file config/inference-config.yml --deploy-config-file config/deployment-config-aks-prod.yml --overwrite
```

* `--compute-target` defines the target AKS cluster where we want to deploy too
* Rest of the parameters are the same as for ACI

Finally, we can retrieve the API key through the CLI or reveal it in the Studio UI:

```cli
az ml endpoint realtime get-keys -n credit-model-aks
```

We can test the AKS endpoint with the sample code in [`test_webservice.ipynb`](test_webservice.ipynb):

## Cleanup

We can remove the model deployments via:

```cli
az ml service delete --name credit-model-aci
az ml service delete --name credit-model-aks
```

And our AKS cluster via:

```cli
az ml computetarget delete -n aks-cluster
```

# Knowledge Check

:question: **Question:** How does AML know which script and what conda dependencies it should deploy?
<details>
  <summary>:white_check_mark: See solution!</summary>

This is defined in [`config/inference-config.yml`](config/inference-config.yml), which points towards our scoring script `score.py` and our `conda.yml`:

```
entryScript: score.py
condaFile: config/conda.yml
```
</details>

:question: **Question:** How can we configure the deployment itself?
<details>
  <summary>:white_check_mark: See solution!</summary>

This is defined in  [`config/deployment-config-aci-qa.yml`](config/deployment-config-aci-qa.yml) and [`config/deployment-config-aks-prod.yml`](config/deployment-config-aks-prod.yml). The file slightly differ, but a few sections are the same:

```yaml
containerResourceRequirements:
  cpu: 1
  memoryInGB: 0.5

# Only one can be True
authEnabled: True
tokenAuthEnabled: False

appInsightsEnabled: True
sslEnabled: False
```

The config for AKS is more granular, as it allows for auto-scaling and replication of the running container(s). Full details for the AKS config can be found [here](https://docs.microsoft.com/en-us/azure/machine-learning/reference-azure-machine-learning-cli#azure-kubernetes-service-deployment-configuration-schema).
Full details for the config of ACI can be found [here](https://docs.microsoft.com/en-us/azure/machine-learning/reference-azure-machine-learning-cli#azure-container-instance-deployment-configuration-schema).
</details>