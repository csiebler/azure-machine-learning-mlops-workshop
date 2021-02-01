# azure-machine-learning-mlops-workshop

A workshop for doing MLOps on Azure Machine Learning.

## Theoretical Part

**Goal:**
* Understand basics around MLOps
* Understand how Azure Machine Learning can help you to build MLOps pipelines
* Experience hands-on for the key concepts (AML pipelines, AZ ML CLI, etc.) to further deepen the understanding
* Understand what is important to a good folder/project layout, what should be in your git repo, how to deal with notebooks, do versioning, etc.

**Furthermore this workshop covers:**
* Overview of when to use one model and when to use many models
* Deployment of models for real-time scoring vs. batch scoring

## Hands-On Parts

:pushpin: Please follow the hands-on exercise in the proposed order, as they build on each other.

* AML Pipelines
  * :weight_lifting: Exercise - Single-step pipeline - [`pipelines-single-training-step`](pipelines-single-training-step/)
  * :weight_lifting: Exercise - Multi-step pipeline with parameters - [`pipelines-multi-step-pipeline`](pipelines-multi-step-pipeline/)
  * :weight_lifting: Exercise - ParallelRunStep pipeline for batch scoring - [`pipelines-parallel-run-step`](pipelines-parallel-run-step/)
  * :weight_lifting: Exercise - Hyperparametertuning pipeline - [`pipelines-hyperdrive-step`](pipelines-hyperdrive-step/)
* MLOps on Azure DevOps
  * :weight_lifting_woman: Exercise - Deploy AML pipeline as Published Endpoint - [`devops-deploy-simple-pipeline`](devops-deploy-simple-pipeline/)
  * :weight_lifting_woman: Exercise - Deploy AML pipeline as Published Endpoint, automatically test it and then add it to a Pipeline Endpoint - [`devops-deploy-pipeline-with-tests`](devops-deploy-pipeline-with-tests/)
* Model Training & Deployment using CLI
  * :weight_lifting_woman: Exercise - Train a model using the AML CLI (mlflow option included) - [`cli-training`](cli-training/)
  * :weight_lifting_woman: Exercise - Deploy a model to ACI and AKS using the AML CLI - [`cli-deployment`](cli-deployment/)
  * :weight_lifting_woman: Exercise - Train a R model using the AML CLI - [`cli-with-r`](cli-with-r/)

**Words of caution:**
The hands-on exercises do not fully embrace concepts like DRY (don't repeat yourself) or other best pratices when it comes to coding standards. Feel free to use them for understanding the concepts, but don't blindly copy and paste them to production.
