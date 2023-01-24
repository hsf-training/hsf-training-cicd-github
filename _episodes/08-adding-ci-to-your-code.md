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
<iframe width="560" height="315" src="https://www.youtube.com/embed/fjIBMRUKVOI" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
# Time To Skim

## The Naive Attempt

As of right now, your `.github/workflows/main.yml` should look like

~~~
name: example
on: push
jobs:
  greeting:
    runs-on: ubuntu-latest
    steps:
      - run: echo hello world
~~~
{: .language-yaml}

Let's go ahead and teach our CI to build our code. Let's add another job (named `build_skim`) that runs in parallel for right now, and runs the compiler `ROOT` uses.
<br/>
**Note**: `ROOT` is a open source framework uses in High Energy Physics.<!-- ([https://root.cern/](https://root.cern/)).-->

Let's give a try.

~~~
COMPILER=$(root-config --cxx)
$COMPILER -g -O3 -Wall -Wextra -Wpedantic -o skim skim.cxx
~~~
{: .language-bash}

The compilation will result in an output binary called `skim`.

> ## Adding a new job
>
> How do we change the CI in order to add a new job that compiles our code?
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
> >           COMPILER=$(root-config --cxx)
> >           $COMPILER -g -O3 -Wall -Wextra -Wpedantic -o skim skim.cxx
> > ~~~
> > {: .language-yaml}
> {: .solution}
{: .challenge}

<!--![CI/CD Two Parallel Jobs]({{site.baseurl}}/fig/ci-cd-two-parallel-jobs.png)-->

## Check jobs

```bash
act -l
```
<!--![Act two parallel jobs]({{site.baseurl}}/fig/act_list_parallel_jobs.png)-->
```
ID          Stage  Name
build_skim  0      build_skim
greeting    0      greeting
```
{: .output}

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
<!--![CI/CD Two Parallel Jobs]({{site.baseurl}}/fig/act_run_parallel_jobs_failure.png)-->
```
[example/build_skim] 🚀  Start image=catthehacker/ubuntu:act-latest
[example/build_skim]   🐳  docker run image=catthehacker/ubuntu:act-latest entrypoint=["/usr/bin/tail" "-f" "/dev/null"] cmd=[]
[example/build_skim] ⭐  Run COMPILER=$(root-config --cxx)
$COMPILER -g -O3 -Wall -Wextra -Wpedantic -o skim skim.cxx
| /github/workflow/0: line 1: root-config: command not found
[example/build_skim]   ❌  Failure - COMPILER=$(root-config --cxx)
```
{: .output}

> ## Broken Build
>
> What happened?
>
> > ## Answer
> > It turns out we had the wrong docker image for our build. If you look at the log, you'll see
> > ~~~
> > 🚀  Start image=catthehacker/ubuntu:act-latest
> >   🐳  docker run image=catthehacker/ubuntu:act-latest entrypoint=["/usr/bin/tail" "-f" "/dev/null"] cmd=[]
> > ~~~
> > {: .output}
> > How do we fix it? We need to define the image with ROOT installed.
> {: .solution}
{: .challenge}

> ## Docker???
>
> Don't panic. You do not need to understand docker to be able to use it.
{: .callout}

Let's go ahead and update our `.github/workflow/main.yml` and fix it to use a versioned docker image that has `root`: `rootproject/root:6.22.06-conda` from the [rootproject/root](https://hub.docker.com/r/rootproject/root) docker hub page.

~~~
runs-on: ubuntu-latest
container: rootproject/root:6.22.06-conda
~~~
{: .language-yaml}

If you run again `act -j build_skim`, you see
```
[example/build_skim] 🚀  Start image=rootproject/root:6.22.06-conda
```
{: .output}


> ## Failed again???
>
> What's that?
<!-- ![Error no such file]({{site.baseurl}}/fig/act_error_no_such_file.png)-->
> <br/>error: skim.cxx: No such file or directory
>
> > ## Answer
> > It seems the job cannot access the repository. We need to instruct GitHub actions to checkout the repository.
> > ~~~
> > steps:
> >    - name: checkout repository
> >      uses: actions/checkout@v3
> > ~~~
> > {: .language-yaml}
> > Let’s go ahead and tell our CI to checkout the repository.
> {: .solution}
{: .challenge}


> ## Still failed??? What the hell.
>
> What happened?
>
> > ## Answer
> > It turns out we just forgot the include flags needed for compilation. If you look at the log, you'll see
> > ~~~
> >  | skim.cxx:11:10: fatal error: ROOT/RDataFrame.hxx: No such file or directory
> >  |  #include "ROOT/RDataFrame.hxx"
> >  |           ^~~~~~~~~~~~~~~~~~~~~
> >   #include "ROOT/RDataFrame.hxx"
> >            ^~~~~~~~~~~~~~~~~~~~~
> >  | compilation terminated.
> >  Error: exit with `FAILURE`: 1
> > ~~~
> > {: .output}
> > How do we fix it? We just need to add another variable to add the flags at the end via `$FLAGS` defined as `FLAGS=$(root-config --cflags --libs)`.
> {: .solution}
{: .challenge}

Ok, let's go ahead and update our `.github/workflow/main.yml` again, and it better be fixed or so help me...


<!--If you already have ROOT installed on your computer, you can run
~~~
cd virtual-pipelines-eventselection
COMPILER=$(root-config --cxx)
$COMPILER -g -O3 -Wall -Wextra -Wpedantic -o skim skim.cxx
~~~
{: .language-bash}
No worries if you don't have ROOT, use `Docker` instead
~~~
cd virtual-pipelines-eventselection
docker run -it --rm -v $PWD:/virtual-pipelines-eventselection -w /virtual-pipelines-eventselection rootproject/root:6.22.06-conda /bin/bash
COMPILER=$(root-config --cxx)
$COMPILER -g -O3 -Wall -Wextra -Wpedantic -o skim skim.cxx
exit  # quit interactive Docker session
~~~
{: .language-bash}
**Note** that you may have to run `docker` with sudo.-->

<!--
## Environment variables

We could separate the environment variables being set like `COMPILER=$(root-config --cxx)` in the last step since this is actually preparation for setting up our environment -- rather than part of the script we want to test! For example,

~~~
build_skim:
  runs-on: ubuntu-latest
  container: rootproject/root:latest
  steps:
    - name: checkout repository
      uses: actions/checkout@v3

    - name: build
      run: $COMPILER skim.cxx -o skim `root-config --cflags --glibs`
      env:
        COMPILER: $(root-config --cxx)
~~~
{: .language-yaml}
`env` can be set under `job:steps:` or under `job:` as well. For more details, you can checkout out: [https://docs.github.com/en/actions/reference/environment-variables](https://docs.github.com/en/actions/reference/environment-variables).
-->

# Building multiple versions

Great, so we finally got it working... Let's build both the version of the code we're testing and also test that the latest ROOT image (`rootproject/root:latest`) works with our code. Call this new job `build_skim_latest`.

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
> >     container: rootproject/root:6.22.06-conda
> >     steps:
> >       - name: checkout repository
> >         uses: actions/checkout@v3
> >
> >       - name: build
> >         run: |
> >           COMPILER=$(root-config --cxx)
> >           FLAGS=$(root-config --cflags --libs)
> >           $COMPILER -g -O3 -Wall -Wextra -Wpedantic -o skim skim.cxx $FLAGS
> >
> >   build_skim_latest:
> >     runs-on: ubuntu-latest
> >     container: rootproject/root:latest
> >     steps:
> >       - name: checkout repository
> >         uses: actions/checkout@v3
> >
> >       - name: latest
> >         run: |
> >           COMPILER=$(root-config --cxx)
> >           FLAGS=$(root-config --cflags --libs)
> >           $COMPILER -g -O3 -Wall -Wextra -Wpedantic -o skim skim.cxx $FLAGS
> > ~~~
> > {: .language-yaml}
> {: .solution}
{: .challenge}


## Dependabot for updating gh action version

Github actions are accompanied by the tags ("@v2"...) which are versions/tags of that action. One might need to update this tags for example from "@v2" to "@v3" because the Github actions developers may fix existing bugs to the action or there may be other updates.

However, this process can be automated by using "Dependabot" which ensures that the workflow references the updated version of the action. If that is not the case, the Dependabot will open a pull request updating the tag of the Github action.

The dependabot action can be added to a Github repository by creating file `dependabot.yml` in the `.github/` folder. The content of the file looks like this: 

~~~
version: 2
updates:
  # Maintain dependencies for GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
 ~~~
{: .language-yaml}

where interval is the frequency of looking for updates to Github actions.

For more information on Dependabot, see e.g., [LINK](https://docs.github.com/en/code-security/dependabot)

{% include links.md %}
