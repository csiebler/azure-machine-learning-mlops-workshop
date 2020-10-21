# Exercise Instructions

Open [`pipeline.ipynb`](pipeline.ipynb) and follow the instructions in the notebook.

# Knowledge Check

**Question:** How can we make our pipeline accept parameters like Datasets, numbers, or strings?
<details>
  <summary>See solution!</summary>
  
  :white_check_mark: We can use the `PipelineParameter` class. In this case, we always have to specify a default value, for the case that the caller does not specify a value. Here is a shot example:

  ```python
default_training_dataset = Dataset.get_by_name(ws, "my_dataset")
training_dataset_parameter = PipelineParameter(name="training_dataset", default_value=default_training_dataset)
  ``` 
</details>

**Question:** What are some pros and cons for separating a pipeline into multiple steps?
<details>
  <summary>See solution!</summary>
  
  :white_check_mark: It depends on the use case, but here are some ideas:

  Pros for having multiple steps:
  * Step results can be chached via `allow_reuse=True`
  * Better modularity of code possible
  * Easier to troubleshoot individual steps

  Cons against having multiple steps:
  * More overhead to pass data between steps
  * Long pipelines with many steps might complicated

</details>