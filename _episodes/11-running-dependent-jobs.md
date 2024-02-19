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
  - We can specify dependencies between jobs running in a series using the needs value.
---
<iframe width="560" height="315" src="https://www.youtube.com/embed/1pnxBc33oyo" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
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
   container: rootproject/root:{% raw %}${{ matrix.version }}{% endraw %}
   strategy:
     matrix:
       version: [6.26.10-conda, latest]
   steps:
     - name: checkout repository
       uses: actions/checkout@v4

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
> >   container: rootproject/root:{% raw %}${{ matrix.version }}{% endraw %}
> >   strategy:
> >     matrix:
> >       version: [6.26.10-conda, latest]
> >   steps:
> >     - name: checkout repository
> >       uses: actions/checkout@v4
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


Let's go ahead and add those changes and look at GitHub.
```bash
git add .github/workflows/main.yml
git commit -m "add dependent jobs"
git push -u origin feature/add-actions
```

![CI/CD Pipeline Two Stages]({{site.baseurl}}/fig/actions_multi_jobs.png)


{% include links.md %}
