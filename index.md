---
layout: lesson
title: Introduction
root: .  # Is the only page that doesn't follow the pattern /:path/index.html
permalink: index.html  # Is the only page that doesn't follow the pattern /:path/index.html
---
{% include gh_variables.html %}

GitHub is a version control distributed git platform used for code hosting and collaboration. Yet it can be used to automatically run the hosted code on Github's servers via GitHub Actions. Actions are workflow automation scripts. We'll learn how to develop on to make our code robust to errors, preserved, and reproducible.

The aim of this module is to:
- explore what it means to build a CI/CD workflow
- guide you through building a CI/CD workflow

> ## Prerequisites
>
> This assumes that you have some basic background with your command line, for example:
> - How to execute custom shell scripts
> - How to run python scripts
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
