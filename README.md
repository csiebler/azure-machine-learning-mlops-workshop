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

* AML Pipelines
  * :weight_lifting: Exercise - Single-step pipeline - [`pipelines-single-training-step`](pipelines-single-training-step/)
  * :weight_lifting: Exercise - Multi-step pipeline with parameters - [`pipelines-multi-step-pipeline`](pipelines-multi-step-pipeline/)
  * :weight_lifting: Exercise - ParallelRunStep pipeline for batch scoring - [`pipelines-parallel-run-step`](pipelines-parallel-run-step/)
* MLOps on Azure DevOps
  * :weight_lifting_woman: Exercise - Deploy AML pipeline as endpoint - [`devops-deploy-pipeline-simple`](devops-deploy-pipeline-simple/)
  * :weight_lifting_woman: Exercise - Deploy AML pipeline as endpoint (with basic tests) - [`devops-deploy-pipeline-with-tests`](devops-deploy-pipeline-with-tests/)