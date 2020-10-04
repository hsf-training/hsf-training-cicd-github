---
title: Homework
teaching: 0
exercises: 30
objectives:
  - Add more testing, perhaps to statistics.
questions:
  - If you have any, ask on Discord!
hidden: false
keypoints:
  - Use everything you've learned to write your own CI/CD!
---

Like the last section, I will simply explain what you need to do. After the previous section, you should have the following in `.github/workflows/main.yml`:

~~~
jobs:
  build_skim:
    runs-on: ubuntu-latest
    container: rootproject/root-conda:6.18.04
    steps:
      - name: checkout repository
        uses: actions/checkout@v2

      - name: build
        run: {% raw %}${{ secrets.COMPILER }}{% endraw %} skim.cxx -o skim `root-config --cflags --glibs`

      - uses: actions/upload-artifact@v2
        with:
          name: skim6.18.04
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

      - uses: actions/upload-artifact@v2
        with:
          name: processed_data
          path: skim_ggH.root
  
  plot:
    needs: build_skim
    runs-on: ubuntu-latest
    container: rootproject/root-conda:6.18.04
    steps:
      - name: checkout repository
        uses: actions/checkout@v2

     - uses: actions/download-artifact@v2
       with:
         name: processed_data

     - name: plot
       run: python histograms.py skim_ggH.root ggH hist_ggH.root

      - uses: actions/upload-artifact@v2
        with:
          name: histograms
          path: hist_ggH.root

  test:
    needs: [skim,plot]
    runs-on: ubuntu-latest
    container: rootproject/root-conda:6.18.04
    steps:
      - name: checkout repository
        uses: actions/checkout@v2

     - uses: actions/download-artifact@v2
       with:
         name: histograms

     - name: test
       run: |
         python tests/test_cutflow_ggH.py
         python tests/test_plot_ggH.py
~~~
{: .language-yaml}

In your `virtual-pipelines-eventselection` repository, you need to:

1. Add more tests
2. Go wild!

{% include links.md %}
