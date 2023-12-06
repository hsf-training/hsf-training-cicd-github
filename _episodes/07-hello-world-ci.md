---
title: "Hello CI World"
teaching: 5
exercises: 10
objectives:
  - Add CI/CD to your project.
questions:
  - How do I run a simple GitHub Actions job?
hidden: false
keypoints:
  - Creating `.github/workflows/main.yml` is the first step to salvation.
  - Pipelines are made of jobs with steps.
  - ACT is especially useful to check and run GitHub Actions jobs (locally) before pushing changes.
---
<iframe width="560" height="315" src="https://www.youtube.com/embed/iAOMjGiksUc" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Adding CI/CD to a project

The first thing we'll do is create a `.github/workflows/main.yml` file in the project.
```bash
cd virtual-pipelines-eventselection/
mkdir -p .github/workflows
```

Open `.github/workflows/main.yml` with your favorite editor and add the following
~~~
name: example
on: push
jobs:
  greeting:
    runs-on: ubuntu-latest
    steps:
      -run: echo hello world
~~~
{: .language-yaml}

## Run GitHub Actions

Now, let's see it in action!

### Run on your computer

It is always nice to first test that everything works well locally before
pushing to the git remote. For this, we need the [nektos/act](https://github.com/nektos/act) tool.

> ## If you cannot install `act`
> `act` requires docker to work. If you have trouble with the installation
> (for example because you are working from a cluster where `docker` is not
> available), simply go to the GitHub section below.
{:.callout}

You can run
```bash
act -l  # -l stands for list (list workflows)
```

What happened??? We can see that this failed because the YAML was invalid... (Error: yaml: line ...)

We should fix this accondingly to the Error message. **Note** that `act` is not a YAML Validator but can help. Some YAML Validators: [https://yamllint.readthedocs.io](https://yamllint.readthedocs.io/en/stable/), [https://codebeautify.org/yaml-validator](https://codebeautify.org/yaml-validator), [http://www.yamllint.com/](http://www.yamllint.com/), ...

Let's rerun:
```bash
act -l
```
This should print out the job name, *i.e* greeting:
<!--![Hello world list]({{site.baseurl}}/fig/act_list_greeting.png)-->

```
ID          Stage  Name
greeting    0      greeting
```
{: .output}

To run `greeting` do

```bash
act -j greeting  # -j stands for job (run job)
```

<!--![greeting job]({{site.baseurl}}/fig/act_run_greeting.png)-->
```
[example/greeting] 🚀  Start image=catthehacker/ubuntu:act-latest
[example/greeting]   🐳  docker run image=catthehacker/ubuntu:act-latest entrypoint=["/usr/bin/tail" "-f" "/dev/null"] cmd=[]
[example/greeting] ⭐  Run echo hello world
| hello world
[example/greeting]   ✅  Success - echo hello world
```
{: .output}

### Run on GitHub

We've created the `.github/workflows/main.yml` file but it's not yet on GitHub. Next step we'll push these changes to GitHub so that it can run our job.
Since we're adding a new feature (Actions) to our project, we'll work in a feature branch. This is just a human-friendly named branch to indicate that it's adding a new feature.

```bash
cd virtual-pipelines-eventselection/
git checkout -b feature/add-actions
git add .github/workflows/main.yml
git commit -m "my first actions"
git push -u origin feature/add-actions
```

And that's it! You've successfully run your CI/CD job and you can view the output. You just have to navigate to the GitHub webpage for the `virtual-pipelines-eventselection` project and hit Actions button, you will find details of your job (status, output,...).

![GitHub Actions Page]({{site.baseurl}}/fig/actions_commits_page.png)

From this page, click through until you can find the output for the successful job run which should look like the following
![CI/CD Hello World Success Output]({{site.baseurl}}/fig/actions_first_ci-cd_success.png)


## Pull Request

Lastly, we'll open up a pull request for this branch, since we plan to merge this back into main when we're happy with the first iteration of the Actions.

### Draft Pull Requests

If you expect to be working on a branch for a bit of time while you have a pull request open, it's good etiquette to mark it as a "draft pull request." This makes clear to everyone that you will continue to add new commits and that it may not yet be the right time to review the pull request. Once you are ready with the work, you can mark the pull request as "ready for review."

{% include links.md %}
