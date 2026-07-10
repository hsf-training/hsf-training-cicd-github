+++
exercises = 0
hidden = false
keypoints = ["You should bookmark the GitHub Actions reference. You'll visit that page often.", 'Actions are standalone commands that are combined into steps to create a job.', 'Workflows are made up of one or more jobs and can be scheduled or triggered.']
objectives = ['Learn where to find more details about everything for the GitHub Actions.', 'Understand the components of GitHub Actions YAML file.']
questions = ['What is the GitHub Actions specification?']
teaching = 5
title = 'YAML and GitHub Actions'
weight = 50
+++
<!--
{{< youtube PwVUVkvcM5A >}}
-->

{{< youtube rPOigpUpLRI >}}

## GitHub Actions YAML

The GitHub Actions configurations are specified using YAML files stored in the`.github/workflows/` directory. Here is an example of a YAML file:

```yaml
name: example

on: push

jobs:
  job_1:
    runs-on: ubuntu-latest
    steps:
      - name: My first step
        run: echo This is the first step of my first job.
```


`name`: GitHub displays the names of your workflows on your repository's actions page. If you omit name, GitHub sets it to the YAML file name.

`on`: **Required**. Specify the event that automatically triggers a workflow run. This example uses the push event, so that the jobs run every time someone pushes a change to the repository.<br/>
For more details, check [this link](https://docs.github.com/en/free-pro-team@latest/actions/reference/workflow-syntax-for-github-actions#on).

{{< callout type="note" title="`jobs`" >}}
Specify the job(s) to be run. Jobs run in parallel by default. To run jobs sequentially, you have to define dependencies on other jobs. We'll cover this in a later section.

`<job_id>`: Each job must have an id to associate with the job, job_1 in the above example. The key job_id is a string that is unique to the jobs object. It must start with a letter or _ and contain only alphanumeric characters, -, or _. Its value is a map of the job's configuration data.

- `runs-on`: **Required**. Each job runs in a particular type of machine (called a "runner") that we choose with this key. There are options for the major operating systems (Linux, Windows, and macOS) and different versions of them. The available options can be found [here](https://docs.github.com/en/free-pro-team@latest/actions/reference/workflow-syntax-for-github-actions#jobsjob_idruns-on).

- `steps`: Specify sequence of tasks. A step is an individual task that can run commands (known as actions). Each step in a job executes on the same runner, allowing the actions in that job to share data with each other. If you do not provide a `name`, the step name will default to the text specified in the `run` command.

[Further reading on jobs](https://docs.github.com/en/free-pro-team@latest/actions/reference/workflow-syntax-for-github-actions#jobs).
{{< /callout >}}

{{< callout type="note" title="`run` commands" >}}
Sometimes, the commands in a `run` step will need to be wrapped in single or double quotes. For example, commands that contain a colon (`:`) need to be wrapped in quotes so that the YAML parser knows to interpret the whole thing as a string rather than a "key: value" pair. Be careful when using special characters: `:`, `{`, `}`, `[`, `]`, `,`, `&`, `*`, `#`, `?`, `|`, `-`, `<`, `>`, `=`, `!`, `%`, `@`, `` ` ``.
{{< /callout >}}

### Overall Structure

Every single parameter we consider for all configurations are keys under jobs. The YAML is structured using job names. For example, we can define two jobs that run in parallel (more on parallel/serial later) with different sets of parameters.

```yaml
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
```


{{< callout type="checklist" title="Reference" >}}
The reference guide for all GitHub Actions pipeline configurations is found at [workflow-syntax-for-github-actions](https://docs.github.com/en/free-pro-team@latest/actions/reference/workflow-syntax-for-github-actions). This contains all the different parameters you can assign to a job.
{{< /callout >}}