+++
exercises = 5
hidden = false
keypoints = ['We can specify dependencies between jobs running in a series using the needs value.']
objectives = ['Run some jobs in serial.']
questions = ['How do you make some jobs run after other jobs?']
teaching = 5
title = 'Dependent Jobs'
weight = 110
+++
<!--
{{< youtube 1pnxBc33oyo >}}
-->

{{< youtube VZnckXqFOw8 >}}

## Defining dependencies

From the last session, we're starting with

```yaml
jobs:
  greeting:
   runs-on: ubuntu-latest
   steps:
     - run: echo hello world

 build_skim:
   runs-on: ubuntu-latest
   container: rootproject/root:${{ matrix.version }}
   strategy:
     matrix:
       version: [6.26.10-conda, latest]
   steps:
     - name: checkout repository
       uses: actions/checkout@v4

     - name: build
       run: |
        COMPILER=$(root-config --cxx)
        FLAGS=$(root-config --cflags --libs)
        $COMPILER -g -O3 -Wall -Wextra -Wpedantic -o skim skim.cxx $FLAGS
```

We're going to talk about another useful parameter `needs`.

{{< callout type="note" title="Specify dependencies between jobs" >}}
The key-value `needs: job or list of jobs` allows you to specify dependencies between jobs in the order you define.
<br/>Example:
```yaml
job2:
  needs: job1
```
job2 waits until job1 completes successfully. [Further reading](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#jobsjob_idneeds).
{{< /callout >}}

{{< challenge title="Dependent jobs" >}}
How to make `build_skim` job to run after `greeting`?

{{< solution title="Solution" >}}
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
    - name: checkout repository
      uses: actions/checkout@v4

    - name: build
      run: |
        COMPILER=$(root-config --cxx)
        FLAGS=$(root-config --cflags --libs)
        $COMPILER -g -O3 -Wall -Wextra -Wpedantic -o skim skim.cxx $FLAGS
```
{{< /solution >}}
{{< /challenge >}}


Let's go ahead and add those changes and look at GitHub.
```bash
git add .github/workflows/main.yml
git commit -m "add dependent jobs"
git push -u origin feature/add-actions
```

![CI/CD Pipeline Two Stages](fig/actions_multi_jobs.png)