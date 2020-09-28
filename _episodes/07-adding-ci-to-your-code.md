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
  - Jobs can be allowed to fail without breaking your CI/CD
---
<iframe width="420" height="263" src="https://www.youtube.com/embed/GiwtSwtMYzg?list=PLKZ9c4ONm-VmmTObyNWpz4hB3Hgx8ZWSb" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
# Time To Skim

## The Naive Attempt

As of right now, your `.github/workflows/main.yml` should look like

~~~
jobs:
	hello_word:
		runs-on: ubuntu-latest
		steps:
			- name: my first ci/cd
			  run: |
				  echo hello world
~~~
{: .language-yaml}

Let's go ahead and teach our CI to build our code. Let's add another job (named `build_skim`) that runs in parallel for right now, and runs the compiler `ROOT` uses. This worked for me on my computer, so we should try it:

~~~
COMPILER=$(root-config --cxx)
$COMPILER -g -O3 -Wall -Wextra -Wpedantic -o skim skim.cxx
~~~
{: .language-bash}

which will produce an output binary called `skim`.

> ## Adding a new job
>
> How do we change the CI in order to add a new parallel job that compiles our code?
>
> > ## Solution
> > ~~~
> > jobs:
> > 	hello_word:
> > 		runs-on: ubuntu-latest
> > 		steps:
> > 			- name: my first ci/cd
> > 			  run: |
> > 				  echo hello world
> >
> > 	build_skim:
> > 		runs-on: ubuntu-latest
> > 		steps:
> > 			- name: my first ci/cd
> > 			  run: |
> > 				  COMPILER=$(root-config --cxx)
> > 				  $COMPILER -g -O3 -Wall -Wextra -Wpedantic -o skim skim.cxx
> > ~~~
> > {: .language-yaml}
> {: .solution}
{: .challenge}

![CI/CD Two Parallel Jobs]({{site.baseurl}}/fig/ci-cd-two-parallel-jobs.png)

## No root-config?

Ok, so maybe we were a little naive here. Let's start debugging. You got this error when you tried to build

~~~
[example/build_skim] 🚀  Start image=node:12.6-buster-slim
[example/build_skim]   🐳  docker run image=node:12.6-buster-slim entrypoint=["/usr/bin/tail" "-f" "/dev/null"] cmd=[]
[example/build_skim] ⭐  Run build skim
| /github/workflow/0: line 2: root-config: command not found
[example/build_skim]   ❌  Failure - build skim
Error: exit with `FAILURE`: 127
~~~

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
container:
	image: rootproject/root-conda:6.18.04
~~~

If you look at the log now, you see
```
[example/build_skim] 🚀  Start image=rootproject/root-conda:6.18.04
```

> ## Failed again???
>
> What's that?
>
> > ## Answer
> > It seems the job cannot access the repository.
> > ~~~
> > steps:
> >    - name: checkout
> >      uses: actions/checkout@v2
> > ~~~


> ## Still failed??? What the hell.
>
> What happened?
>
> > ## Answer
> > It turns out we just forgot the include flags needed for compilation. If you look at the log, you'll see
> > ~~~
> >  $ COMPILER=$(root-config --cxx)
> >  $ $COMPILER -g -O3 -Wall -Wextra -Wpedantic -o skim skim.cxx
> >  skim.cxx:11:10: fatal error: ROOT/RDataFrame.hxx: No such file or directory
> >   #include "ROOT/RDataFrame.hxx"
> >            ^~~~~~~~~~~~~~~~~~~~~
> >  compilation terminated.
> >  ERROR: Job failed: exit code 1
> > ~~~
> > {: .output}
> > How do we fix it? We just need to add another variable to add the flags at the end via `$FLAGS` defined as `FLAGS=$(root-config --cflags --libs)`.
> {: .solution}
{: .challenge}

Ok, let's go ahead and update our `.github/workflow/main.yml` again, and it better be fixed or so help me...

# Building multiple versions

Great, so we finally got it working... CI/CD isn't obviously powerful when you're only building one thing. Let's build both the version of the code we're testing and also test that the latest ROOT image (`rootproject/root-conda:latest`) works with our code. Call this new job `build_skim_latest`.

> ## Adding the `build_skim_latest` job
>
> What does the `.github/workflow/main.yml` look like now?
>
> > ## Solution

> > ~~~
> > jobs:
> > 	hello_word:
> > 		runs-on: ubuntu-latest
> > 		steps:
> > 			- name: my first ci/cd
> > 			  run: |
> > 				  echo hello world
> >
> > 	build_skim:
> > 		runs-on: ubuntu-latest
> >         container:
> >             image: rootproject/root-conda:6.18.04
> > 		steps:
> >             -name: checkout
> >               uses: actions/checkout@v2
> >
> > 			- name: build
> > 			  run: |
> > 				  COMPILER=$(root-config --cxx)
> >                   FLAGS=$(root-config --cflags --libs)
> > 				  $COMPILER -g -O3 -Wall -Wextra -Wpedantic -o skim skim.cxx $FLAGS
> >
> > 	build_skim_latest:
> > 		runs-on: ubuntu-latest
> >         container:
> >             image: rootproject/root-conda:latest
> > 		steps:
> >             -name: checkout
> >               uses: actions/checkout@v2

> > 			- name: latest
> > 			  run: |
> > 				  COMPILER=$(root-config --cxx)
> >                   FLAGS=$(root-config --cflags --libs)
> > 				  $COMPILER -g -O3 -Wall -Wextra -Wpedantic -o skim skim.cxx $FLAGS
> > ~~~
> > {: .language-yaml}
> {: .solution}
{: .challenge}


{% include links.md %}
