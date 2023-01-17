---
layout: lesson
root: .  # Is the only page that doesn't follow the pattern /:path/index.html
permalink: index.html  # Is the only page that doesn't follow the pattern /:path/index.html
---
{% include gh_variables.html %}

GitHub is a distributed git platform used for code hosting and collaboration. It can also be used to automatically run the hosted code on Github's servers via GitHub Actions. Actions are workflow automation scripts. We'll learn how to develop on to make our code robust to errors, preserved, and reproducible.

The aim of this module is to:
- explore what it means to build a CI/CD workflow
- guide you through building a CI/CD workflow

> ## Prerequisites
>
> This assumes that you'll have some basic background with your command line, for example:
>
> 1. How to execute custom shell scripts (if you are not familiar with the shell, click [here](https://swcarpentry.github.io/shell-novice/))
> 2. How to run python scripts (if you are not familiar with python, click [here](https://swcarpentry.github.io/python-novice-inflammation/))
> 3. How to interact with remotes in git (if you are not familiar with git, click [here](https://swcarpentry.github.io/git-novice/); for simplified authentication with the `gh` command line interface, see [this version of the git training](https://mambelli.github.io/git-novice/07-github/index.html))
{: .prereq}

> ## The skills we'll focus on:
>
> 1.  Making scripts exit correctly
> 2.  Building a CI/CD workflow of unlimited potential
> 3.  Understanding how job runners work (and get access to your clones)
> 4.  Protecting secret information while allowing jobs to run
{: .checklist}

{% include curriculum.html %}

{% include links.md %}
