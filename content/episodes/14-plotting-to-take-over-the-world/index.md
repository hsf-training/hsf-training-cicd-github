+++
exercises = 10
hidden = false
keypoints = ['Another action, another job, another artifact.']
objectives = ['Use everything you learned to make plots!']
questions = ['How do we make plots?']
teaching = 5
title = 'Making Plots to Take Over The World'
weight = 140
+++
<!--
{{< youtube xPEf5oOMm3A >}}
-->

{{< youtube dV4wEkjLxKQ >}}

## On Your Own

So in order to make plots, we just need to take the skimmed file `skim_ggH.root` and pass it through the `histograms.py` code that exists. This can be run with the following code

```bash
python histograms.py skim_ggH.root ggH hist_ggH.root
```

This needs to be added to your `.github/workflows/main.yml` which should look like the following:

```yaml
jobs:
  greeting:
    runs-on: ubuntu-latest
    steps:
      - run: echo hello world

  build_skim:
    needs: greeting
    runs-on: ubuntu-latest
    container: rootproject/root:${{ matrix.version }}
    strategy:
      matrix:
        version: [6.26.10-conda, latest]
    steps:
      - name: install node
        run: wget -qO- https://nodejs.org/dist/v20.18.1/node-v20.18.1-linux-x64.tar.gz | tar -xz -C /usr/local --strip-components=1

      - name: checkout repository
        uses: actions/checkout@v4

      - name: build
        run: |
          COMPILER=$(root-config --cxx)
          FLAGS=$(root-config --cflags --libs)
          $COMPILER -g -O3 -Wall -Wextra -Wpedantic -o skim skim.cxx $FLAGS

      - uses: actions/upload-artifact@v4
        with:
          name: skim${{ matrix.version }}
          path: skim

  skim:
    needs: build_skim
    runs-on: ubuntu-latest
    container: rootproject/root:6.26.10-conda
    steps:
      - name: install node
        run: wget -qO- https://nodejs.org/dist/v20.18.1/node-v20.18.1-linux-x64.tar.gz | tar -xz -C /usr/local --strip-components=1

      - name: checkout repository
        uses: actions/checkout@v4

      - uses: actions/download-artifact@v4
        with:
          name: skim6.26.10-conda

      - name: skim
        run: |
          chmod +x ./skim
          ./skim root://eospublic.cern.ch//eos/root-eos/HiggsTauTauReduced/GluGluToHToTauTau.root skim_ggH.root 19.6 11467.0 0.1

      - uses: actions/upload-artifact@v4
        with:
          name: skim_ggH
          path: skim_ggH.root
```

{{< challenge title="Adding Artifacts" >}}
So we need to do a two things:

1. add a `plot` job
2. save the output `hist_ggH.root` as an artifact

You know what? While you're at it, why not delete the `greeting` job and multi versions job as well? There's no need for it anymore 🙂.

{{< solution title="Solution" >}}
```yaml
...
...
...
 skim:
   needs: build_skim
   runs-on: ubuntu-latest
   container: rootproject/root:6.26.10-conda
   steps:
     - name: install node
       run: wget -qO- https://nodejs.org/dist/v20.18.1/node-v20.18.1-linux-x64.tar.gz | tar -xz -C /usr/local --strip-components=1

     - name: checkout repository
       uses: actions/checkout@v4

     - uses: actions/download-artifact@v4
       with:
         name: skim6.26.10-conda

     - name: skim
       run: |
         chmod +x ./skim
         ./skim root://eospublic.cern.ch//eos/root-eos/HiggsTauTauReduced/GluGluToHToTauTau.root skim_ggH.root 19.6 11467.0 0.1

     - uses: actions/upload-artifact@v4
       with:
         name: skim_ggH
         path: skim_ggH.root

 plot:
   needs: skim
   runs-on: ubuntu-latest
   container: rootproject/root:6.26.10-conda
   steps:
     - name: install node
       run: wget -qO- https://nodejs.org/dist/v20.18.1/node-v20.18.1-linux-x64.tar.gz | tar -xz -C /usr/local --strip-components=1

     - name: checkout repository
       uses: actions/checkout@v4

     - uses: actions/download-artifact@v4
       with:
         name: skim_ggH

     - name: plot
       run: python histograms.py skim_ggH.root ggH hist_ggH.root

     - uses: actions/upload-artifact@v4
       with:
         name: histograms
         path: hist_ggH.root
```
{{< /solution >}}
{{< /challenge >}}

<!--
![Actions_secret_variable](fig/actions_artifacts_final.png)
-->

Once we're done, we should probably start thinking about how to test some of these outputs we've made. We now have a skimmed ggH ROOT file and a file of histograms of the skimmed ggH.

{{< callout type="note" title="Are we testing anything?" >}}
Integration testing is actually testing that the scripts we have still run. So we are constantly testing as we go here which is nice. Additionally, there's also continuous deployment because we've been making artifacts that are passed to other jobs. There are many ways to deploy the results of the code base, such as pushing to a web server and so on. Artifacts are one way to deploy.
{{< /callout >}}