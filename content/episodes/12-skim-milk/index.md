+++
exercises = 10
hidden = false
keypoints = ['Making jobs aware of each other is pretty easy.', 'Artifacts are files created by the CI that are offered for download and inspection.']
objectives = ['Learn how to skim code and set up artifacts.']
questions = ['How can I run my skimming code in the GitHub Actions?']
teaching = 5
title = 'A Skimmer Higgs'
weight = 120
+++
<!--
{{< youtube -cO4yHz5dp4 >}}
-->

{{< youtube XIprY9Km4k8 >}}

## The First Naive Attempt

Let's just attempt to try and get the code working as it is. Since it worked for us already locally, surely the CI/CD must be able to run it?

As a reminder of what we've ended with from the last session:

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
```

Since the `skim` binary is built, let's see if we can run it. We need to add a job , with name `skim`.

`skim` is meant to process data (skimming) we are going to run on.

Let's go ahead and figure out how to define a run job. Seems too easy to be true?
```yaml
skim:
  needs: build_skim
  runs-on: ubuntu-latest
  container: rootproject/root:6.26.10-conda
  steps:
      - name: install node
        run: wget -qO- https://nodejs.org/dist/v20.18.1/node-v20.18.1-linux-x64.tar.gz | tar -xz -C /usr/local --strip-components=1

      - name: checkout repository
        uses: actions/checkout@v4

      - name: skim
        run: ./skim
```


After you've added the `skim` job you can push your changes to GitHub:
```bash
git add .github/workflows/main.yml
git commit -m "add skim job"
git push -u origin feature/add-actions
```

{{< tabs >}}
{{< tab name="GitHub" selected=true >}}
![Skim waiting](fig/actions_skim_job_wait.png)

![Skim failure](fig/actions_skim_job_failure1.png)
{{< /tab >}}
{{< tab name="Gitea" >}}
![Skim waiting](fig/gitea_actions_skim_job_wait.png)

![Skim failure](fig/gitea_actions_skim_job_failure1.png)
{{< /tab >}}
{{< /tabs >}}

{{< challenge title="Failed???" >}}
Let's have a look at the log message
```text
./skim: not found
```
{{< /challenge >}}

## We're too naive

Ok, fine. That was way too easy. It seems we have a few issues to deal with. The `skim` binary in the `build_skim` job isn't in the `skim` job by default. We need to use GitHub `artifacts` to copy over this from the right job.

### Artifacts

Artifacts are used to upload (`upload-artifact`) and download  (`download-artifact`) files and directories which should be attached to the job after this one has completed. That way it can share those files with another job in the same workflow.

{{< callout type="checklist" title="More Reading" >}}
- [https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts](https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts)
{{< /callout >}}

{{< callout type="note" title="Passing data between two jobs in a workflow" >}}
```yaml
job_1:
  - uses: actions/upload-artifact@v4
    with:
      name: <name>
      path: <file>
job_2:
  - uses: actions/download-artifact@v4
    with:
      name: <name>
```
{{< /callout >}}

**Note** that the artifact name should not contain any of the following characters `"`,`:`,`<`,`>`,`|`,`*`,`?`,`\`,`/`.

In order to take advantage of passing data between two jobs, one combines `download-artifact` with `needs`.

{{< challenge title="Combining `download-artifact` with `needs`" >}}
Let's do it.

{{< solution title="Solution" >}}
```yaml
...
...
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

    - uses: actions/upload-artifact@v3
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

    - uses: https://github.com/actions/download-artifact@v3
      with:
        name: skim6.26.10-conda

    - name: skim
      run: ./skim
```

{{< /solution >}}
{{< /challenge >}}


{{< challenge title="What happened?" >}}
```text
./skim: Permission denied
```

Permissions can be changed using the `chmod` command.
{{< solution title="Solution" >}}
```yaml
run: |
  chmod +x ./skim
  ./skim
```
{{< /solution >}}
{{< /challenge >}}

From the log message, one can see that we are missing arguments.
```text
Use executable with following arguments: ./skim input output cross_section integrated_luminosity scale
```

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
```yaml
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
         name: skim6.26.10-conda

     - name: skim
       run: ./skim root://eosuser.cern.ch//eos/user/g/gstark/AwesomeWorkshopFeb2020/GluGluToHToTauTau.root skim_ggH.root 19.6 11467.0 0.1
```

This will produce a file `skim_ggH.root` containing processed data.
-->
