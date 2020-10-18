---
title: "Adding CI to Your Existing Code"
teaching: 5
exercises: 10
objectives:
  - Learn how to get your CI/CD Runners to build your code
  - Try and see if the CI/CD can catch problems with our code.
questions:
  - I have code already in GitHub, how can I add CI to it?
hidden: false
keypoints:
  - Setting up CI/CD shouldn't be mind-numbing
  - All defined jobs run in parallel by default
---
<!--
<iframe width="420" height="263" src="https://www.youtube.com/embed/GiwtSwtMYzg?list=PLKZ9c4ONm-VmmTObyNWpz4hB3Hgx8ZWSb" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
-->
# Time To Skim

## The Naive Attempt

As of right now, your `.github/workflows/main.yml` should look like

~~~
on: push
jobs:
  greeting:
    runs-on: ubuntu-latest
    steps:
      - run: echo hello world
~~~
{: .language-yaml}

Let's go ahead and teach our CI to build our code. Let's add another job (named `build_skim`) that runs in parallel for right now, and runs the compiler `ROOT` uses. 

This should work. But let's give a try.

If you already have ROOT installed on your computer use
~~~
cd virtual-pipelines-eventselection
COMPILER=g++
$COMPILER skim.cxx -o skim `root-config --cflags --glibs`
~~~
{: .language-bash}

No worries if you don't have ROOT, use `Docker` instead
~~~
cd virtual-pipelines-eventselection
docker run -it --rm -v $PWD:/virtual-pipelines-eventselection -w /virtual-pipelines-eventselection rootproject/root-conda:6.18.04 /bin/bash 
COMPILER=g++
$COMPILER skim.cxx -o skim `root-config --cflags --glibs`
exit  # quit interactive Docker session
~~~
{: .language-bash}
**Note** that you may have to run `docker` with sudo.

The compilation will result in an output binary called `skim`.

> ## Adding a new job
>
> How do we change the CI in order to add a new parallel job that compiles our code?
>
> > ## Solution
> > ~~~
> > jobs:
> >   greeting:
> >     runs-on: ubuntu-latest
> >     steps:
> >       - run: echo hello world
> >
> >   build_skim:
> >     runs-on: ubuntu-latest
> >     steps:
> >       - name: build
> >         run: |
> >           COMPILER=g++
> >           $COMPILER skim.cxx -o skim `root-config --cflags --glibs`
> > ~~~
> > {: .language-yaml}
> {: .solution}
{: .challenge}

<!--![CI/CD Two Parallel Jobs]({{site.baseurl}}/fig/ci-cd-two-parallel-jobs.png)-->

## Check jobs

```bash
act -l
```
![Act two parallel jobs]({{site.baseurl}}/fig/act_list_parallel_jobs.png)

We can see 2 parallel jobs. Let's commit the changes we made.

```bash
git add .github/workflows/main.yml
git commit -m "add build skim job"
git push -u origin feature/add-actions
```

![Job failure root-config]({{site.baseurl}}/fig/actions_parallel_jobs_failure1a.png)
![Job failure root-config details]({{site.baseurl}}/fig/actions_parallel_jobs_failure1b.png)

## No root-config?

Ok, so maybe we were a little naive here. Let's start debugging locally.

We can reproduce this error:
```bash
act -j build_skim
```

You got this error when you tried to build
![CI/CD Two Parallel Jobs]({{site.baseurl}}/fig/act_run_parallel_jobs_failure.png)
{: .output}

> ## Broken Build
>
> What happened?
>
> > ## Answer
> > It turns out we had the wrong docker image for our build. If you look at the log, you'll see
> > ~~~
> > 🚀  Start image=node:12.6-buster-slim
> >   🐳  docker run image=node:12.6-buster-slim entrypoint=["/usr/bin/tail" "-f" "/dev/null"] cmd=[]
> > ~~~
> > {: .output}
> > How do we fix it? We need to define the image with ROOT installed.
> {: .solution}
{: .challenge}

> ## Docker???
>
> Don't panic. You do not need to understand docker to be able to use it.
{: .callout}

Let's go ahead and update our `.github/workflow/main.yml` and fix it to use a versioned docker image that has `root`: `rootproject/root-conda:6.18.04` from the [rootproject/root-conda](https://hub.docker.com/r/rootproject/root-conda) docker hub page.

~~~
runs-on: ubuntu-latest
container: rootproject/root-conda:6.18.04
~~~
{: .language-yaml}

If you run again `act -j build_skim`, you see
```
[example/build_skim] 🚀  Start image=rootproject/root-conda:6.18.04
```
{: .output}


> ## Failed again???
>
> What's that?
> ![Error no such file]({{site.baseurl}}/fig/act_error_no_such_file.png)
>
> > ## Answer
> > It seems the job cannot access the repository. We need to instruct GitHub actions to checkout the repository. 
> > ~~~
> > steps:
> >    - name: checkout repository
> >      uses: actions/checkout@v2
> > ~~~
> > {: .language-yaml}
> {: .solution}
{: .challenge}

Ok, let's go ahead and update our `.github/workflow/main.yml` again, and it better be fixed or so help me...

We could separate the environment variables being set like `COMPILER=g++` in the last step since this is actually preparation for setting up our environment -- rather than part of the script we want to test! For example,

~~~
build_skim:
  runs-on: ubuntu-latest
  container: rootproject/root-conda:latest
  steps:
    - name: checkout repository
      uses: actions/checkout@v2

    - name: build
      run: $COMPILER skim.cxx -o skim `root-config --cflags --glibs`
      env:
        COMPILER: g++
~~~
{: .language-yaml}
`env` can be set under `job:steps:` or under `job:` as well.

# Building multiple versions

Great, so we finally got it working... CI/CD isn't obviously powerful when you're only building one thing. Let's build both the version of the code we're testing and also test that the latest ROOT image (`rootproject/root-conda:latest`) works with our code. Call this new job `build_skim_latest`.

> ## Adding the `build_skim_latest` job
>
> What does the `.github/workflow/main.yml` look like now?
>
> > ## Solution
> >
> > ~~~
> > jobs:
> >   greeting:
> >     runs-on: ubuntu-latest
> >     steps:
> >       - run: echo hello world
> >
> >   build_skim:
> >     runs-on: ubuntu-latest
> >     container: rootproject/root-conda:6.18.04
> >     steps:
> >       - name: checkout repository
> >         uses: actions/checkout@v2
> >
> >       - name: build
> >         run: $COMPILER skim.cxx -o skim `root-config --cflags --glibs`
> >         env:
> >           COMPILER: g++
> >
> >   build_skim_latest:
> >     runs-on: ubuntu-latest
> >     container: rootproject/root-conda:latest
> >     steps:
> >       - name: checkout repository
> >         uses: actions/checkout@v2
> >
> >       - name: latest
> >         run: $COMPILER skim.cxx -o skim `root-config --cflags --glibs`
> >         env:
> >           COMPILER: g++
> > ~~~
> > {: .language-yaml}
> {: .solution}
{: .challenge}


We're ready for a coffee break.


{% include links.md %}
