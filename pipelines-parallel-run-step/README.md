# Exercise Instructions

Open [`parallel_run_step_pipeline.ipynb`](parallel_run_step_pipeline.ipynb) and follow the instructions in the notebook.

# Knowledge Check

:question: **Question:** How can we change where `ParallelRunStep` should write its output to?
<details>
  <summary>:white_check_mark: See solution!</summary>
  
We can use the `OutputFileDatasetConfig` class. There, we can define the `destination`, which points to a folder on a datastore:

```python
# Direct path
output_dataset = OutputFileDatasetConfig(name='batch_results', destination=(datastore, 'batch-scoring-results/'))

# run-id is replaced with the run's id
output_dataset = OutputFileDatasetConfig(name='batch_results', destination=(datastore, 'batch-scoring-results/{run-id}/'))

# output-name is replaced with the name, in this case batch_results
output_dataset = OutputFileDatasetConfig(name='batch_results', destination=(datastore, 'batch-scoring-results/{output-name}/'))

# Lastly, we can automatically register it as a Dataset in the workspace
output_dataset = OutputFileDatasetConfig(name='batch_results', destination=(datastore, 'batch-scoring-results/')).register_on_complete(name='batch-scoring-results')
``` 
</details>

:question: **Question:** How does `ParallelRunStep` know that the minibatch has been successfully processed?
<details>
  <summary>:white_check_mark: See solution!</summary>
  
The method `def run(file_list)` in your `score_parallel.py` is expected to return an array or Dataframe with the same number of elements/rows as `len(file_list)`.
</details>