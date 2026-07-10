+++
exercises = 10
hidden = false
keypoints = ['Using `matrix` allows to test the code against a combination of versions.']
objectives = ["Don't Repeat Yourself (DRY)", 'Use a single job for multiple jobs']
questions = ['How can we make job templates?']
teaching = 5
title = 'Matrix'
weight = 90
+++
{{< youtube LwMKCVVGCD0 >}}

## Matrix

From the previous lesson, we tried to build the code against two different ROOT images by adding an extra job:

```yaml
jobs:
  greeting:
    runs-on: ubuntu-latest
    steps:
      - run: echo hello world

  build_skim:
    runs-on: ubuntu-latest
    container: rootproject/root:6.26.10-conda
    steps:
      - name: checkout repository
        uses: actions/checkout@v4
      - name: build
        run: |
          COMPILER=$(root-config --cxx)
          FLAGS=$(root-config --cflags --libs)
          $COMPILER -g -O3 -Wall -Wextra -Wpedantic -o skim skim.cxx $FLAGS

  build_skim_latest:
    runs-on: ubuntu-latest
    container: rootproject/root:latest
    steps:
      - name: checkout repository
        uses: actions/checkout@v4
      - name: latest
        run: |
          COMPILER=$(root-config --cxx)
          FLAGS=$(root-config --cflags --libs)
          $COMPILER -g -O3 -Wall -Wextra -Wpedantic -o skim skim.cxx $FLAGS
```

{{< callout type="note" title="Building a matrix across different versions" >}}
We could do better using `matrix`. The latter allows us to test the code against a combination of versions in a single job.

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
YAML truncates trailing zeroes from a floating point number, which means that `version: [3.9, 3.10, 3.11]` will automatically
be converted to `version: [3.9, 3.1, 3.11]` (notice `3.1` instead of `3.10`). The conversion will lead to unexpected failures
as your CI will be running on a version not specified by you. This behavior resulted in several failed jobs after the release
of Python 3.10 on GitHub Actions. The conversion (and the build failure) can be avoided by converting the floating point number
to strings - `version: ['3.9', '3.10', '3.11']`.

More details on matrix: [https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#jobsjob_idstrategymatrix).
{{< /callout >}}


We can push the changes to GitHub and see how it will look like.
```bash
git add .github/workflows/main.yml
git commit -m "add multi jobs"
git push -u origin feature/add-ci
```

While the jobs are running, let's imagine we don't want our CI/CD to crash if that happens. We have to add `continue-on-error: true` to a job
```yaml
runs-on: ubuntu-latest
continue-on-error: true
```
For the matrix case, Github Actions fails the entire workflow and stops all the running jobs if any of the jobs in the matrix fails. This can be prevented by using `fail-fast: false` key:value.
```yaml
strategy:
  fail-fast: false
```

More details: [https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#jobsjob_idcontinue-on-error).

{{< challenge title="Allow a specific matrix job to fail" >}}
But what if we want to **only** allow the job with version set to `latest` to fail without failing the workflow run?

{{< solution title="Solution" >}}
```yaml
runs-on: ubuntu-latest
container: rootproject/root:${{ matrix.version }}
continue-on-error: ${{ matrix.allow_failure }}
strategy:
  matrix:
    version: [6.26.10-conda]
    allow_failure: [false]
    include:
      - version: latest
        allow_failure: true
```
{{< /solution >}}
{{< /challenge >}}


Look how much cleaner you've made the code. You should now see that it's pretty easy to start adding more build jobs for other images in a relatively clean way, as you've now abstracted the actual building from the definitions.