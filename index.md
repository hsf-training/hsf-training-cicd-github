---
layout: lesson
title: Introduction
root: .  # Is the only page that doesn't follow the pattern /:path/index.html
permalink: index.html  # Is the only page that doesn't follow the pattern /:path/index.html
---
{% include gh_variables.html %}

> ## Prerequisites
>
> This assumes that you'll have some basic background with your command line, for example:
>
> 1. How to execute custom shell scripts
> 2. How to run python scripts
>
> as well as having gone through all previous sessions in this workshop.
{: .prereq}

Introduction
------------

GitHub is a version control distributed git platform used for code hosting and collaboration. Yet it can be used to automatically run the hosted code on Github's servers via GitHub Actions. Actions are workflow automation scripts. We'll learn how to develop on to make our code robust to errors, preserved, and reproducible.

The aim of this module is to:
- explore what it means to build a CI/CD workflow
- guide you through building a CI/CD workflow

> ## The skills we'll focus on:
>
> 1.  Making scripts exit correctly
> 2.  Building a CI/CD workflow of unlimited potential
> 3.  Understanding how job runners work (and get access to your clones)
> 4.  The GitHub permissions model
> 5.  Protecting secret information while allowing jobs to run
{: .checklist}

{% include links.md %}
