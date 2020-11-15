---
title: "YAML and GitHub Actions"
teaching: 5
exercises: 0
objectives:
  - Learn where to find more details about everything for the GitHub Actions.
  - Understand the components of GitHub Actions YAML file.
questions:
  - What is the GitHub Actions specification?
hidden: false
keypoints:
  - You should bookmark the GitHub Actions reference. You'll visit that page often.
  - Actions are standalone commands that are combined into steps to create a job.
  - Workflows are made up of one or more jobs and can be scheduled or triggered.
---
<!--
<iframe width="420" height="263" src="https://www.youtube.com/embed/1Kz3VrzYHb0?list=PLKZ9c4ONm-VmmTObyNWpz4hB3Hgx8ZWSb" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
-->

# GitHub Actions YAML

The GitHub Actions configurations are specified using YAML files stored in the`.github/workflows/` directory. Here is an example of a YAML file:

~~~
name: example

on: push

jobs:
  job_1:
    runs-on: ubuntu-latest
    steps:
      - name: My first step
        run: echo This is the first step of my first job.
~~~
{: .language-yaml}


`name`: GitHub displays the names of your workflows on your repository's actions page. If you omit name, GitHub sets it to the YAML file name.

`on`: **Required**. Specify the event that automatically triggers a workflow run. This example uses the push event, so that the jobs run every time someone pushes a change to the repository. For more details, check [this link](https://docs.github.com/en/free-pro-team@latest/actions/reference/workflow-syntax-for-github-actions#on).

> ## `jobs`
> Specify the job(s) to be run. Jobs run in parallel by default. To run jobs sequentially, you have to define dependencies on other jobs. We'll cover this in a later section. 
>
> `<job_id>`: Each job must have an id to associate with the job, job_1 in the above example. The key job_id is a string that is unique to the jobs object. It must start with a letter or _ and contain only alphanumeric characters, -, or _. Its value is a map of the job's configuration data.
>
> - `runs-on`: **Required**. Each job runs in an virtual environment (runner) specified by the key runs-on. Available environments can be found [here](https://docs.github.com/en/free-pro-team@latest/actions/reference/workflow-syntax-for-github-actions#jobsjob_idruns-on).
>
> - `steps`: Specify sequence of tasks. A step is an individual task that can run commands (known as actions). Each step in a job executes on the same runner, allowing the actions in that job to share data with each other. If you do not provide a `name`, the step name will default to the text specified in the `run` command.
>
> [Further reading on jobs](https://docs.github.com/en/free-pro-team@latest/actions/reference/workflow-syntax-for-github-actions#jobs).
{: .callout}

## Overall Structure

Every single parameter we consider for all configurations are keys under jobs. The YAML is structured using job names. For example, we can define three jobs that run in parallel (more on parallel/serial later) with different sets of parameters.

~~~
name: <name of your workflow>

on: <event or list of events>

jobs:
  job_1:
    name: <name of the first job>
    runs-on: <type of machine to run the job on>
    steps:
      - name: <step 1>
        run: |
          <commands>
      - name: <step 2>
        run: |
          <commands>
  job_2:
    name: <name of the second job>
    runs-on: <type of machine to run the job on>
    steps:
      - name: <step 1>
        run: |
          <commands>
      - name: <step 2>
        run: |
          <commands>
~~~
{: .language-yaml}


## Reference

The reference guide for all GitHub Actions pipeline configurations is found at [workflow-syntax-for-github-actions](https://docs.github.com/en/free-pro-team@latest/actions/reference/workflow-syntax-for-github-actions). This contains all the different parameters you can assign to a job.
{: .checklist}

{% include links.md %}
