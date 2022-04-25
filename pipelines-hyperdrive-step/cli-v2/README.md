# Running a Sweep Job via CLI (v2)

For running this example with Azure Machine Learning CLI v2, we can use a sweep job:

```
az configure --defaults group=<YOUR WORKSPACE NAME> workspace=<YOUR WORKSPACE NAME>
az ml data create -f dataset.yml
az ml job create -f sweep.yml --stream
```

Notes:
* Make sure to adapt [`dataset.yml`](dataset.yml) to point to your data
* This examples an AzureML Dataset that was created using the CLI v2 - it does not work with datasets created in the UI/old SDK

## References

* [Dataset YAML examples](https://docs.microsoft.com/en-us/azure/machine-learning/reference-yaml-data)
* [Sweep Job YAML examples](https://docs.microsoft.com/en-us/azure/machine-learning/reference-yaml-job-sweep)