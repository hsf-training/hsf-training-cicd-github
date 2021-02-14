---
title: "Dependent Jobs"
teaching: 5
exercises: 5
objectives:
  - Run some jobs in serial.
questions:
  - How do you make some jobs run after other jobs?
hidden: false
keypoints:
  - needs allows to specify dependencies between jobs in order to run them in serial.
---
<!-- 
<iframe width="420" height="263" src="https://www.youtube.com/embed/PBkO3TsdDUA?list=PLKZ9c4ONm-VmmTObyNWpz4hB3Hgx8ZWSb" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
-->
# Defining dependencies

From the last session, we're starting with

~~~
jobs:
  greeting:
   runs-on: ubuntu-latest
   steps:
     - run: echo hello world

 build_skim:
   runs-on: ubuntu-latest
   container: rootproject/root-conda:{% raw %}${{ matrix.version }}{% endraw %}
   strategy:
     matrix:
       version: [6.18.04, latest]
   steps:
     - name: checkout repository
       uses: actions/checkout@v2

     - name: build
       run: |
        COMPILER=$(root-config --cxx)
        FLAGS=$(root-config --cflags --libs)
        $COMPILER -g -O3 -Wall -Wextra -Wpedantic -o skim skim.cxx $FLAGS
~~~
{: .language-yaml}

We're going to talk about another useful parameter `needs`.  

> ## Specify dependencies between jobs
>
> The key-value `needs: jobs or list of jobs` allows you to specify dependencies between jobs in the order you define.
> <br/>Example:
> ~~~
> job2:
>   needs: job1
> ~~~
> {: .language-yaml}
> job2 waits until job1 completes successfully. [Further reading](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#jobsjob_idneeds).
{: .callout}

> ## Dependent jobs
> How to make `build_skim` job to run after `greeting`?
>
> > ## Solution
> >
> > ~~~
> > jobs:
> >  greeting:
> >    runs-on: ubuntu-latest
> >    steps:
> >      - run: echo hello world
> >
> > build_skim:
> >   needs: greeting
> >   runs-on: ubuntu-latest
> >   container: rootproject/root-conda:{% raw %}${{ matrix.version }}{% endraw %}
> >   strategy:
> >     matrix:
> >       version: [6.18.04, latest]
> >   steps:
> >     - name: checkout repository
> >       uses: actions/checkout@v2
> >
> >     - name: build
> >       run: |
> >         COMPILER=$(root-config --cxx)
> >         FLAGS=$(root-config --cflags --libs)
> >         $COMPILER -g -O3 -Wall -Wextra -Wpedantic -o skim skim.cxx $FLAGS
> > ~~~
> > {: .language-yaml}
> {: .solution}
{: .challenge}


If you do it correctly, you should see

![CI/CD Pipeline Two Stages]({{site.baseurl}}/fig/actions_multi_jobs.png)


{% include links.md %}
