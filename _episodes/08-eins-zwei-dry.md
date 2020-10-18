---
title: "Matrix"
teaching: 5
exercises: 10
objectives:
  - Don't Repeat Yourself (DRY)
  - Use a single job for multiple jobs
questions:
  - How can we make job templates?
hidden: false
keypoints:
  - Using `matrix` allows to test the code against a combination of versions.
---

<center>
<!--
<iframe width="420" height="263" src="https://www.youtube.com/embed/_cKm7FUTzQs?list=PLKZ9c4ONm-VmmTObyNWpz4hB3Hgx8ZWSb" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
-->
<iframe width="420" height="236" src="https://i.gifer.com/1TpS.gif" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</center>

# Matrix

From the previous lesson, we tried to build the code against two different ROOT images by adding an extra job: 

~~~
jobs:
  greeting:
    runs-on: ubuntu-latest
    steps:
      - run: echo hello world

  build_skim:
    runs-on: ubuntu-latest
    container: rootproject/root-conda:6.18.04
    steps:
      - name: checkout repository
        uses: actions/checkout@v2
      - name: build
        run: $COMPILER skim.cxx -o skim `root-config --cflags --glibs`
        env:
          COMPILER: g++

  build_skim_latest:
    runs-on: ubuntu-latest
    container: rootproject/root-conda:latest
    steps:
      - name: checkout repository
        uses: actions/checkout@v2

      - name: latest
        run: $COMPILER skim.cxx -o skim `root-config --cflags --glibs`
        env:
          COMPILER: g++
~~~
{: .language-yaml}

We could do better using `matrix`. The latter allows us to test the code against a combination of versions in a single job.

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
       run: $COMPILER skim.cxx -o skim `root-config --cflags --glibs`
       env:
         COMPILER: g++
~~~
{: .language-yaml}

Let's update our `.github/workflow/main.yml` and push the changes to GitHub and see how it will look like. **Note** that `act` doesn't run job with `matrix`.

~~~
git add .github/workflows/main.yml
git commit -m "add multi jobs"
git push -u origin feature/add-ci
~~~
{: .language-bash}

While the jobs are running, let's imagine we don't want our CI/CD to crash if that happens. We have to add `continue-on-error: true` to a job
~~~
runs-on: ubuntu-latest
continue-on-error: true
~~~
{: .language-yaml}
or `fail-fast: false` for the matrix case
~~~
strategy:
  fail-fast: false
~~~
{: .language-yaml}

> ## Allow a specific matrix job to fail
> But what if we want to **only** allow the job with version set to `latest` to fail without failing the workflow run?
>
> > ## Solution
> >
> > ~~~
> > runs-on: ubuntu-latest
> > container: rootproject/root-conda:{% raw %}${{ matrix.version }}{% endraw %}
> > continue-on-error: {% raw %}${{ matrix.allow_failure }}{% endraw %}
   strategy:
> > strategy:
> >   fail-fast: false
> >   matrix:
> >     version: [6.18.04, latest]
> >     allow_failure: [false]
> >     include:
> >       - version: latest
> >         allow_failure: true
> > ~~~
> > {: .language-yaml}
> {: .solution}
{: .challenge}


Look how much cleaner you've made the code. You should now see that it's pretty easy to start adding more build jobs for other images in a relatively clean way, as you've now abstracted the actual building from the definitions.

{% include links.md %}
