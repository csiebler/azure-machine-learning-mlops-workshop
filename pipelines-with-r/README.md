# Exercise Instructions

On your laptop or Compute Instance, build the Docker base image for R. Since R environments take a while to build, it makes sense to pre-built a Docker image with our required libraries. See the provided [`Dockerfile`](./Dockerfile) as an example and feel free to add more dependencies. Locate the name of the Azure Container Registry you want to use (preferably the one of the AML workspace) and run:

```console
cd pipelines-with-r
az login
az acr build --registry <your registry name> --image r-tutorial:v1 .
```

Once done, open [`r_pipeline.ipynb`](r_pipeline.ipynb) and follow the instructions in the notebook.

