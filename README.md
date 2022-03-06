# Run Batch Jobs on Kubernetes with Bodywork

![bodywork](https://bodywork-media.s3.eu-west-2.amazonaws.com/batch_job_qs.png)

This repository contains a Bodywork project that demonstrates how to run a batch workload (or job) on Kubernetes, with Bodywork. For information on this demo, take a look [here](https://bodywork.readthedocs.io/en/latest/quickstart_batch_job/). To run this project, follow the steps below. If you are new to Kubernetes, then take a look at our [Kubernetes Quickstart Guide](https://bodywork.readthedocs.io/en/latest/kubernetes/#quickstart).

## Install Bodywork

Bodywork is distributed as a Python package that can be installed using Pip,

```shell
$ pip install bodywork
```
## Run the Job

To execute the workload defined in this repository run,

```shell
$ bodywork create deployment https://github.com/bodywork-ml/bodywork-batch-job-project
```

Logs will be streamed to your terminal until the job has been successfully completed.

## Running the Job on a Schedule

If you're happy with the result, you can schedule the workflow-controller to operate remotely on the cluster on a pre-defined schedule. For example, to setup the the workflow to run every hour, use the following command,

```shell
$ bodywork create cronjob https://github.com/bodywork-ml/bodywork-batch-job-project \
    --name=hourly-job \
    --schedule="0 * * * *"
```

Each scheduled workflow will attempt to re-run the batch-job, as defined by the state of this repository's `master` branch at the time of execution.

## Make this Project Your Own

This repository is a [GitHub template repository](https://docs.github.com/en/free-pro-team@latest/github/creating-cloning-and-archiving-repositories/creating-a-repository-from-a-template) that can be automatically copied into your own GitHub account by clicking the `Use this template` button above.

After you've cloned the template project, use official [Bodywork documentation](https://bodywork.readthedocs.io/en/latest/) to help modify the project to meet your own requirements.
