---
title: "Hello CI World"
teaching: 5
exercises: 10
objectives:
  - Add CI/CD to your project.
questions:
  - How do I run a simple GitHub CI job?
hidden: false
keypoints:
  - Creating `.github/workflows/main.yml` is the first step to salvation.
  - Pipelines are made of jobs with steps.
  - CI Linters are especially useful to check syntax before pushing changes.
---
<iframe width="420" height="263" src="https://www.youtube.com/embed/LqeJzIYJCwc?list=PLKZ9c4ONm-VmmTObyNWpz4hB3Hgx8ZWSb" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
# Adding CI/CD to a project

We've been working on the analysis code which has a lot of work done, but we should be good physicists (and people) by adding tests and CI/CD. The first thing we'll do is create a `.github/workflows/main.yml` file in the project.

Firstly, let's run a GitHub CI job locally
```
cd virtual-pipelines-eventselection/
mkdir -p .github/workflows
```
Open `.github/workflows/main.yml` with your favorite editor and add the following
~~~
name: example
on: push
jobs:
	hello_word:
		runs-on: ubuntu-latest
		steps:
			-name: my first ci/cd
			  run: |
				  echo hello world
~~~
{: .source}

Run locally:
```
act -l
```

What happened??? We can see that this failed because the YAML was invalid... (Error: yaml: line 8: mapping values are not allowed in this context)

We should fix this accondingly to the Error message.

Let's rerun:
```
act -l
```
This should print out the job name, *i.e* hello_word.

To run hello word

```
act -j job_1
```

Now, let's run on GitHub virual machines
```
cd virtual-pipelines-eventselection/
git checkout -b feature/add-ci
git add .github/workflows/main.yml
git commit -m "my first ci/cd"
git push -u origin feature/add-ci
```
{: .source}

> ## Feature Branches
>
> Since we're adding a new feature (CI/CD) to our project, we'll work in a feature branch. This is just a human-friendly named branch to indicate that it's adding a new feature.
{: .callout}

Now, if you navigate to the GitHub webpage for that project and hit Actions button, you will find details of your job (status, output,...).


Lastly, we'll open up a pull request for this branch, since we plan to merge this back into master when we're happy with the first iteration of the CI/CD.

> ## Work In Progress?
>
> If you expect to be working on a branch for a bit of time while you have a merge request open, it's good etiquette to mark it as a Work-In-Progress (WIP).
> ![Work In Progress]({{site.baseurl}}/fig/work-in-progress.png)
{: .callout}



And that's it! You've successfully run your CI/CD job and you can view the output.


{% include links.md %}
