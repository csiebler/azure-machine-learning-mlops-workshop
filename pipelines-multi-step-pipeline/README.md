# Exercise Instructions

Open [`multi_step_pipeline.ipynb`](multi_step_pipeline.ipynb) and follow the instructions in the notebook.

# Knowledge Check

:question: **Question:** How can we make our pipeline accept parameters like Datasets, numbers, or strings?
<details>
  <summary>:white_check_mark: See solution!</summary>
  
We can use the `PipelineParameter` class. In this case, we always have to specify a default value, for the case that the caller does not specify a value. Here is a shot example:

```python
default_training_dataset = Dataset.get_by_name(ws, "my_dataset")
training_dataset_parameter = PipelineParameter(name="training_dataset", default_value=default_training_dataset)
``` 
</details>

:question: **Question:** What are some pros and cons for separating a pipeline into multiple steps?
<details>
  <summary>:white_check_mark: See solution!</summary>
  
It depends on the use case, but here are some ideas:

Pros for having multiple steps:
* Step results can be chached via `allow_reuse=True`
* Better modularity of code possible
* Easier to troubleshoot individual steps

Cons against having multiple steps:
* More overhead to pass data between steps
* Long pipelines with many steps might complicated
</details>

:question: **Question:** When should you use Datasets vs Datapaths?
<details>
  <summary>:white_check_mark: See solution!</summary>
  
It depends on the use case, but roughly speaking:

Use `Datasets` when:
* Your data assets are register in AzureML
* When you prefer direct data lineage within AzureML (click through from data to experiment to model to deployment)

Use `DataPaths` when:
* You want to call the pipeline from a different tool and there is no need to register the input data as a dataset
* A typical examples would be e.g., a batch scoring pipeline, called via Azure Data Factory
</details>