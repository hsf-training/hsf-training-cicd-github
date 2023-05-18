---
title: "Matrix"
teaching: 5
exercises: 10
objectives:
  - Don't Repeat Yourself (DRY)
  - Use a single job for multiple jobs
questions:
  - How can we make job templates?
hidden: false
keypoints:
  - Using `matrix` allows to test the code against a combination of versions.
---

<center>
<iframe width="560" height="315" src="https://www.youtube.com/embed/o4vZf3Pr6rY" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<iframe width="420" height="236" src="https://i.gifer.com/1TpS.gif" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</center>

# Matrix

From the previous lesson, we tried to build the code against two different ROOT images by adding an extra job:

~~~
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
        uses: actions/checkout@v3
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
        uses: actions/checkout@v3
      - name: latest
        run: |
          COMPILER=$(root-config --cxx)
          FLAGS=$(root-config --cflags --libs)
          $COMPILER -g -O3 -Wall -Wextra -Wpedantic -o skim skim.cxx $FLAGS
~~~
{: .language-yaml}

> ## Building a matrix across different versions
>
> We could do better using `matrix`. The latter allows us to test the code against a combination of versions in a single job.
>
> ~~~
> jobs:
>   greeting:
>    runs-on: ubuntu-latest
>    steps:
>      - run: echo hello world
>
>  build_skim:
>    runs-on: ubuntu-latest
>    container: rootproject/root:{% raw %}${{ matrix.version }}{% endraw %}
>    strategy:
>      matrix:
>        version: [6.26.10-conda, latest]
>    steps:
>      - name: checkout repository
>        uses: actions/checkout@v3
>
>      - name: build
>         run: |
>           COMPILER=$(root-config --cxx)
>           FLAGS=$(root-config --cflags --libs)
>           $COMPILER -g -O3 -Wall -Wextra -Wpedantic -o skim skim.cxx $FLAGS
> ~~~
> {: .language-yaml}
> YAML truncates trailing zeroes from a floating point number, which means that `version: [3.9, 3.10, 3.11]` will automatically
> be converted to `version: [3.9, 3.1, 3.11]` (notice `3.1` instead of `3.10`). The conversion will lead to unexpected failures
> as your CI will be running on a version not specified by you. This behavior resulted in several failed jobs after the release
> of Python 3.10 on GitHub Actions. The conversion (and the build failure) can be avoided by converting the floating point number
> to strings - `version: ['3.9', '3.10', '3.11']`.
>
> More details on matrix: [https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#jobsjob_idstrategymatrix).
{: .callout}

>## `act` is optional.
>
> Remember that `act` is not required but encouraged for completeing this workshop.
{: .callout} 

Let's update our `.github/workflow/main.yml` and use `act` to run the job with `matrix`.
```bash
act -j build_skim
```

```
[example/build_skim-1] 🧪  Matrix: map[version:6.26.10-conda]
[example/build_skim-1] 🚀  Start image=rootproject/root:6.26.10-conda
[example/build_skim-2] 🧪  Matrix: map[version:latest]
[example/build_skim-2] 🚀  Start image=rootproject/root:latest
[example/build_skim-1]   🐳  docker run image=rootproject/root:6.26.10-conda entrypoint=["/usr/bin/tail" "-f" "/dev/null"] cmd=[]
[example/build_skim-1]   🐳  docker cp src=/tmp/eventselection/. dst=/github/workspace
[example/build_skim-1] ⭐  Run checkout repository
[example/build_skim-1]   ✅  Success - checkout repository
[example/build_skim-1] ⭐  Run COMPILER=$(root-config --cxx)
FLAGS=$(root-config --cflags --libs)
$COMPILER -g -O3 -Wall -Wextra -Wpedantic -o skim skim.cxx $FLAGS
[example/build_skim-1]   ✅  Success - COMPILER=$(root-config --cxx)
FLAGS=$(root-config --cflags --libs)
$COMPILER -g -O3 -Wall -Wextra -Wpedantic -o skim skim.cxx $FLAGS
[example/build_skim-2]   🐳  docker run image=rootproject/root:latest entrypoint=["/usr/bin/tail" "-f" "/dev/null"] cmd=[]
[example/build_skim-2]   🐳  docker cp src=/tmp/eventselection/. dst=/github/workspace
[example/build_skim-2] ⭐  Run checkout repository
[example/build_skim-2]   ✅  Success - checkout repository
[example/build_skim-2] ⭐  Run COMPILER=$(root-config --cxx)
FLAGS=$(root-config --cflags --libs)
$COMPILER -g -O3 -Wall -Wextra -Wpedantic -o skim skim.cxx $FLAGS
[example/build_skim-2]   ✅  Success - COMPILER=$(root-config --cxx)
FLAGS=$(root-config --cflags --libs)
$COMPILER -g -O3 -Wall -Wextra -Wpedantic -o skim skim.cxx $FLAGS
```
{: .output}

We can push the changes to GitHub and see how it will look like.
~~~
git add .github/workflows/main.yml
git commit -m "add multi jobs"
git push -u origin feature/add-ci
~~~
{: .language-bash}

While the jobs are running, let's imagine we don't want our CI/CD to crash if that happens. We have to add `continue-on-error: true` to a job
~~~
runs-on: ubuntu-latest
continue-on-error: true
~~~
{: .language-yaml}
For the matrix case, Github Actions fails the entire workflow and stops all the running jobs if any of the jobs in the matrix fails. This can be prevented by using `fail-fast: false` key:value.
~~~
strategy:
  fail-fast: false
~~~
{: .language-yaml}

More details: [https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#jobsjob_idcontinue-on-error).

> ## Allow a specific matrix job to fail
> But what if we want to **only** allow the job with version set to `latest` to fail without failing the workflow run?
>
> > ## Solution
> >
> > ~~~
> > runs-on: ubuntu-latest
> > container: rootproject/root:{% raw %}${{ matrix.version }}{% endraw %}
> > continue-on-error: {% raw %}${{ matrix.allow_failure }}{% endraw %}
> > strategy:
> >   matrix:
> >     version: [6.26.10-conda]
> >     allow_failure: [false]
> >     include:
> >       - version: latest
> >         allow_failure: true
> > ~~~
> > {: .language-yaml}
> {: .solution}
{: .challenge}


Look how much cleaner you've made the code. You should now see that it's pretty easy to start adding more build jobs for other images in a relatively clean way, as you've now abstracted the actual building from the definitions.

{% include links.md %}
