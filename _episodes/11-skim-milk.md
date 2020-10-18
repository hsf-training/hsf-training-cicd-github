---
title: "A Skimmer Higgs"
teaching: 5
exercises: 10
objectives:
  - Learn how to skim code and set up artifacts.
questions:
  - How can I run my skimming code in the GitHub Actions?
hidden: false
keypoints:
  - Making jobs aware of each other is pretty easy.
  - Artifacts are pretty neat.
  - We're too naive.
---
<!--
<iframe width="420" height="263" src="https://www.youtube.com/embed/omYX4uRxCKI?list=PLKZ9c4ONm-VmmTObyNWpz4hB3Hgx8ZWSb" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
-->
# The First Naive Attempt

Let's just attempt to try and get the code working as it is. Since it worked for us already locally, surely the CI/CD must be able to run it???

As a reminder of what we've ended with from the last session:

~~~
jobs:
  greeting:
    runs-on: ubuntu-latest
    steps:
      - run: echo hello world
 
  build_skim:
    needs: greeting
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
          COMPILER=g++
~~~
{: .language-yaml}

Since the `skim` binary is built, let's see if we can run it. We need to add a job , with name `skim`. 

`skim` is meant to process data (skimming) we are going to run on.

Let's go ahead and figure out how to define a run job. Seems too easy to be true?
~~~
skim:
  needs: build_skim
  runs-on: ubuntu-latest
  container: rootproject/root-conda:6.18.04
  steps:
      - name: checkout repository
        uses: actions/checkout@v2

      - name: skim
        run: ./skim
~~~
{: .language-yaml}

After you've added the `skim` job you can push your changes to GitHub:
~~~
git add .github/workflows/main.yml
git commit -m "add skim job"
git push -u origin feature/add-actions
~~~
{: .language-bash

~~~
./skim: not found
~~~
{: .output}

# We're too naive

Ok, fine. That was way too easy. It seems we have a few issues to deal with. The `skim` binary in the `build_skim` job isn't in the `skim` job by default. We need to use GitHub `artifacts` to copy over this from the right job.

## Artifacts

Artifacts are used to upload (`upload-artifact`) and download  (`download-artifact`) files and directories which should be attached to the job after this one has completed. That way it can share those files with another job in the same workflow.

> ## More Reading
> - [https://docs.github.com/en/free-pro-team@latest/actions/guides/storing-workflow-data-as-artifacts](https://docs.github.com/en/free-pro-team@latest/actions/guides/storing-workflow-data-as-artifacts)
{: .checklist}

> ## Passing data between two jobs in a workflow
> ~~~
> job_1:
>   - uses: actions/upload-artifact@v2
>     with:
>       name: <name>
>       path: <file>
> job_2:
>   - uses: actions/download-artifact@v2
>     with:
>       name: <name>
> ~~~
> {: .language-yaml}
{: .callout}

**Note** that the artifact name should not contain any of the following characters `"`,`:`,`<`,`>`,`|`,`*`,`?`,`\`,`/`.

In order to take advantage of passing data between two jobs, one combines `download-artifact` with `needs`.

> ## Combining `download-artifact` with `needs`
> Let's do it.
>
> > ## Solution
> > ~~~
> > ...
> > ...
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
> >       run: $COMPILER skim.cxx -o skim `root-config --cflags --glibs`
> >       env:
> >         COMPILER=g++
> >
> >     - uses: actions/upload-artifact@v2
> >       with:
> >         name: skim${{ matrix.root }}
> >         path: skim
> >
> > skim:
> >   needs: build_skim
> >   runs-on: ubuntu-latest
> >   container: rootproject/root-conda:6.18.04
> >   steps:
> >     - name: checkout repository
> >       uses: actions/checkout@v2
> >
> >     - uses: actions/download-artifact@v2
> >       with:
> >         name: skim6.18.04
> >
> >     - name: skim
> >       run: ./skim
> > ~~~
> > {: .language-yaml}
> {: .solution}
{: .challenge}

![Skim waiting]({{site.baseurl}}/fig/actions_skim_job_wait.png)

![Skim waiting]({{site.baseurl}}/fig/actions_skim_job_failure1.png)


> ## What happened?
>
> ~~~
> ./skim: Permission denied
> ~~~
> {: .output}
> 
> Permissions can be changed using the `chmod` command.
> > ## Solution
> > ~~~
> > run: |
> >   chmod +x ./skim
> >   ./skim
> > ~~~
> > {: .language-yaml}
> {: .solution}
{: .challenge}

From the log message, one can see that we are missing arguments.
~~~
Use executable with following arguments: ./skim input output cross_section integrated_luminosity scale
~~~
{: .output}

We will deal with that in the next lesson.

<!--
Our executable takes 5 arguments: input (remote data), output (processed data), cross-section, integrated luminosity, and scale.

Let's consider the following value
```
input: root://eospublic.cern.ch//eos/root-eos/HiggsTauTauReduced/GluGluToHToTauTau.root
output: skim_ggH.root
cross_section: 19.6
integrated_luminosity: 11467.0
scale: 0.1
```

Our YAML file should look like
~~~
...
 skim:
   needs: build_skim
   runs-on: ubuntu-latest
   container: rootproject/root-conda:6.18.04
   steps:
     - name: checkout repository
       uses: actions/checkout@v2

     - uses: actions/download-artifact@v2
       with:
         name: skim6.18.04

     - name: skim
       run: ./skim root://eosuser.cern.ch//eos/user/g/gstark/AwesomeWorkshopFeb2020/GluGluToHToTauTau.root skim_ggH.root 19.6 11467.0 0.1
~~~
{: .language-yaml}

This will produce a file `skim_ggH.root` containing processed data.
-->

{% include links.md %}
