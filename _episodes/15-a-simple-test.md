---
title: "Let's Actually Make A Test (For Real)"
teaching: 5
exercises: 20
objectives:
  - Actually add a test on the output of running physics
questions:
  - I'm out of questions.
hidden: false
keypoints:
  - This kind of test is a regression test, as we're testing assuming the code up to this point was correct.
  - This is not a unit test. Unit tests would be testing individual pieces of the Framework code-base, or specific functionality you wrote into your algorithms.
---
<iframe width="560" height="315" src="https://www.youtube.com/embed/VgFgvCrXl9o" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

So at this point, I'm going to be very hands-off, and just explain what you will be doing. Here's where you should be starting from:

~~~
...
...
...
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
        ./skim root://eospublic.cern.ch//eos/root-eos/HiggsTauTauReduced/GluGluToHToTauTau.root skim_ggH.root 19.6 11467.0 0.1

    - uses: actions/upload-artifact@v2
      with:
        name: skim_ggH
        path: skim_ggH.root

 plot:
   needs: skim
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
~~~
{: .language-yaml}

> # Adding a regression test
>
> 1. Add a test job, `test_ggH` that has the right `dependencies`
>   - Note: `./skim` needs to be updated to produce a `skim_ggH.log` (hint: `./skim .... > skim_ggH.log`)
>   - We also need the hist_ggH.root file produced by the plot job
> 2. Create a directory called `tests/` and make two python files in it named `test_cutflow_ggH.py` and `test_plot_ggH.py` that uses `PyROOT` and `python3`
>   - you might find the following lines (below) helpful to set up the tests
> 3. Write a few different tests of your choosing that tests (and asserts) something about `hist_ggH.root`. Some ideas are:
>   - check the structure (does `ggH_pt_1` exist?)
>   - check that the integral of a histogram matches a value you expect
>   - check that the bins of a histogram matches the values you expect
> 4. Update your `test_ggH` job to execute the regression tests
> 5. Try causing your CI/CD to fail on the `test_ggH` job
>
> > ## Done?
> >
> > Once you're happy with setting up the regression test, mark your merge request as ready by clicking the `Resolve WIP Status` button, and then merge it in to master.
> {: .solution}
{: .challenge}

## Template for `test_cutflow_ggH.py`

~~~
import sys

logfile = open('skim_ggH.log', 'r')
lines = [line.rstrip() for line in logfile]

required_lines = [
   'Number of events: 47696',
   'Cross-section: 19.6',
   'Integrated luminosity: 11467',
   'Global scaling: 0.1',
   'Passes trigger: pass=3402       all=47696      -- eff=7.13 % cumulative eff=7.13 %',
   'nMuon > 0 : pass=3402       all=3402       -- eff=100.00 % cumulative eff=7.13 %',
   'nTau > 0  : pass=3401       all=3402       -- eff=99.97 % cumulative eff=7.13 %',
   'Event has good taus: pass=846        all=3401       -- eff=24.88 % cumulative eff=1.77 %',
   'Event has good muons: pass=813        all=846        -- eff=96.10 % cumulative eff=1.70 %',
   'Valid muon in selected pair: pass=813        all=813        -- eff=100.00 % cumulative eff=1.70 %',
   'Valid tau in selected pair: pass=813        all=813        -- eff=100.00 % cumulative eff=1.70 %',
]

print('\n'.join(lines))
for required_line in required_lines:
    if not required_line in lines:
        print(f'Did not find line in log file. {required_line}')
        sys.exit(1)
~~~
{: .language-python}

## Template for `test_plot_ggH.py`

~~~
import sys
import ROOT

f = ROOT.TFile.Open('hist_ggH.root')
keys = [k.GetName() for k in f.GetListOfKeys()]

required_keys = ['ggH_pt_1', 'ggH_pt_2']

print('\n'.join(keys))
for required_key in required_keys:
    if not required_key in keys:
        print(f'Required key not found. {required_key}')
        sys.exit(1)

integral = f.ggH_pt_1.Integral()
if abs(integral - 222.88716647028923) > 0.0001:
    print(f'Integral of ggH_pt_1 is different: {integral}')
    sys.exit(1)
~~~
{: .language-python}


{% include links.md %}
