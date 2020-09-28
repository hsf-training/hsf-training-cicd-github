---
title: "YAML and CI"
teaching: 5
exercises: 0
objectives:
  - Learn where to find more details about everything for the GitLab CI.
  - Understand the structure of the GitLab CI YAML file.
questions:
  - What is the GitHub CI specification?
hidden: false
keypoints:
  - You should bookmark the GitHub reference on CI/CD. You'll visit that page often.
  - A job is defined by a name and a script, at minimum.
  - Other than job names, reserved keywords are the top-level parameters defined in a YAML file.
---
<iframe width="420" height="263" src="https://www.youtube.com/embed/1Kz3VrzYHb0?list=PLKZ9c4ONm-VmmTObyNWpz4hB3Hgx8ZWSb" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
# GitHub CI YAML

The GitHub CI configurations are specified using a YAML file called `main.yml` stored in the`.github/workflows/` directory. Here is an example:

~~~
name: example

on: push

jobs:
  job_1:
    runs-on: ubuntu-latest
	steps:
	  - name: My first step
	    run: |
			echo This is the first step of my first job.
~~~
{: .language-yaml}


> ## `name`
> **Optional**. GitHub displays the names of your workflows on your repository's actions page. If you omit name, GitHub sets it to the YAML file.

> ## `on`
> **Required**. Specify the event that automatically triggers pipelines. This example uses the push event, so that the jobs run every time someone pushes a change to the repository.

> ## `jobs`
> Specify the job(s) to be run. Each job runs in an environment specified by `runs-on`. Jobs run in parallel by default. To run jobs sequentially, you have to define dependencies on other jobs. We'll cover this in a later section.
{: .callout}

> ## Steps
> A step is an individual task that can run commands (known as actions). Each step in a job executes on the same runner, allowing the actions in that job to share data with each other.

## Take note

 Sometimes, commands that contain a colon (`:`) need to be wrapped in quotes so that the YAML parser knows to interpret the whole thing as a string rather than a “key: value” pair. Be careful when using special characters: `:`, `{`, `}`, `[`, `]`, `,`, `&`, `*`, `#`, `?`, `|`, `-`, `<`, `>`, `=`, `!`, `%`, `@`, `\``.
{: .callout}

## Overall Structure

Every single parameter we consider for all configurations are keys under jobs. The YAML is structured using job names. For example, we can define three jobs that run in parallel (more on parallel/serial later) with different sets of parameters.

~~~
jobs:
  job1:
    param1: null
    param2: null

  job2:
    param1: null
    param3: null

  job3:
    param2: null
    param4: null
    param5: null
~~~
{: .language-yaml}


## Reference

The reference guide for all GitLab CI/CD pipeline configurations is found at [workflow-syntax-for-github-actions](https://docs.github.com/en/free-pro-team@latest/actions/reference/workflow-syntax-for-github-actions). This contains all the different parameters you can assign to a job.
{: .checklist}

{% include links.md %}
