---
title: "Making Plots to Take Over The World"
teaching: 5
exercises: 10
objectives:
  - Use everything you learned to make plots!
questions:
  - How do we make plots?
hidden: false
keypoints:
  - Another action, another job, another artifact.
---
<!--
<iframe width="420" height="263" src="https://www.youtube.com/embed/BDpqN3nVVVo?list=PLKZ9c4ONm-VmmTObyNWpz4hB3Hgx8ZWSb" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
-->
# On Your Own

So in order to make plots, we just need to take the skimmed file `skim_ggH.root` and pass it through the `histograms.py` code that exists. This can be run with the following code

~~~
python histograms.py skim_ggH.root ggH hist_ggH.root
~~~
{: .language-bash}

This needs to be added to your `.github/workflows/main.yml` which should look like the following:

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
	
      - uses: actions/upload-artifact@v2
        with:
          name: skim{% raw %}${{ matrix.version }}{% endraw %}
          path: skim

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
       run: |
         chmod +x ./skim
         ./skim root://eospublic.cern.ch//eos/root-eos/HiggsTauTauReduced/GluGluToHToTauTau.root skim_ggH.root 19.6 11467.0 0.1
~~~
{: .language-yaml}

> ## Adding Artifacts
>
> So we need to do a two things:
>
> 1. add a `plot` job
> 2. save the output `hist_ggH.root` as an artifact
>
> You know what? While you're at it, why not delete the `greeting` job and multi versions job as well? There's no need for it anymore 🙂.
>
> > ## Solution
> > ~~~
> > ...
> > ...
> > ...
> >  skim:
> >    needs: build_skim
> >    runs-on: ubuntu-latest
> >    container: rootproject/root-conda:6.18.04
> >    steps:
> >      - name: checkout repository
> >        uses: actions/checkout@v2
> >
> >     - uses: actions/download-artifact@v2
> >       with:
> >         name: skim6.18.04
> >
> >     - name: skim
> >       run: |
> >         chmod +x ./skim
> >         ./skim root://eospublic.cern.ch//eos/root-eos/HiggsTauTauReduced/GluGluToHToTauTau.root skim_ggH.root 19.6 11467.0 0.1
> >
> >     - uses: actions/upload-artifact@v2
> >       with:
> >         name: processed_data
> >         path: skim_ggH.root
> >
> >  plot:
> >    needs: skim
> >    runs-on: ubuntu-latest
> >    container: rootproject/root-conda:6.18.04
> >    steps:
> >      - name: checkout repository
> >        uses: actions/checkout@v2
> >
> >     - uses: actions/download-artifact@v2
> >       with:
> >         name: processed_data
> >
> >     - name: plot
> >       run: python histograms.py skim_ggH.root ggH hist_ggH.root
> >
> >     - uses: actions/upload-artifact@v2
> >       with:
> >         name: histograms
> >         path: hist_ggH.root
> > ~~~
> > {: .language-yaml}
> {: .solution}
{: .challenge}

![Actions_secret_variable]({{site.baseurl}}/fig/actions_artifacts_final.png)

Once we're done, we should probably start thinking about how to test some of these outputs we've made. We now have a skimmed ggH ROOT file and a file of histograms of the skimmed ggH.

> ## Are we testing anything?
>
> Integration testing is actually testing that the scripts we have still run. So we are constantly testing as we go here which is nice. Additionally, there's also continuous deployment because we've been making artifacts that are passed to other jobs. There are many ways to deploy the results of the code base, such as pushing to a web server and so on. Artifacts are one way to deploy.
{: .callout}


{% include links.md %}
