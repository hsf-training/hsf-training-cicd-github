---
title: Homework
teaching: 0
exercises: 30
objectives:
  - Add more testing, perhaps to statistics.
questions:
  - If you have any, ask on Mattermost channel!
hidden: false
keypoints:
  - Use everything you've learned to write your own CI/CD!
---

Like the last section, I will simply explain what you need to do. After the previous section, you should have the following in `.github/workflows/main.yml`:

<!--run: {% raw %}${{ secrets.COMPILER }}{% endraw %} skim.cxx -o skim `root-config --cflags --glibs`-->
~~~
jobs:
  build_skim:
    runs-on: ubuntu-latest
    container: rootproject/root:6.26.10-conda
    steps:
      - name: checkout repository
        uses: actions/checkout@v3

      - name: build
        run: |
          COMPILER=$(root-config --cxx)
          FLAGS=$(root-config --cflags --libs)
          $COMPILER -g -O3 -Wall -Wextra -Wpedantic -o skim skim.cxx $FLAGS

      - uses: actions/upload-artifact@v2
        with:
          name: skim6.22.06
          path: skim

  skim:
    needs: build_skim
    runs-on: ubuntu-latest
    container: rootproject/root:6.26.10-conda
    steps:
      - name: checkout repository
        uses: actions/checkout@v3

     - uses: actions/download-artifact@v3
       with:
         name: skim6.22.06

     - name: skim
       run: |
         chmod +x ./skim
         ./skim root://eospublic.cern.ch//eos/root-eos/HiggsTauTauReduced/GluGluToHToTauTau.root skim_ggH.root 19.6 11467.0 0.1 > skim_ggH.log

      - uses: actions/upload-artifact@v2
        with:
          name: skim_ggH
          path: |
            skim_ggH.root
            skim_ggH.log

  plot:
    needs: build_skim
    runs-on: ubuntu-latest
    container: rootproject/root:6.26.10-conda
    steps:
      - name: checkout repository
        uses: actions/checkout@v3

     - uses: actions/download-artifact@v3
       with:
         name: skim_ggH

     - name: plot
       run: python histograms.py skim_ggH.root ggH hist_ggH.root

      - uses: actions/upload-artifact@v2
        with:
          name: histograms
          path: hist_ggH.root

  test:
    needs: plot
    runs-on: ubuntu-latest
    container: rootproject/root:6.22.06
    steps:
      - name: checkout repository
        uses: actions/checkout@v3

      - name: Download from skim
        uses: actions/download-artifact@v3
        with:
          name: skim_ggH

      - name: Download from plot
        uses: actions/download-artifact@v3
        with:
          name: histograms

      - name: cutflow test
        run: python tests/test_cutflow_ggH.py

      - name: plot test
        run: python tests/test_plot_ggH.py
~~~
{: .language-yaml}

In your `virtual-pipelines-eventselection` repository, you need to:

1. Add more tests
2. Go wild!

{% include links.md %}
