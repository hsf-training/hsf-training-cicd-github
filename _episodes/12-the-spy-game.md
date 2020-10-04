---
title: "Getting into the Spy Game"
teaching: 5
exercises: 10
objectives:
  - Add custom environment variables
  - Learn how to give your CI/CD Runners access to private information
questions:
  - How can I give my GitHub actions private information?
hidden: false
keypoints:
  - Service accounts provide an extra layer of security between the outside world and your account
  - Environment variables in GitHub actions allow you to hide protected information from others who can see your code
---
<iframe width="420" height="263" src="https://www.youtube.com/embed/XNhi1dw6jxI?list=PLKZ9c4ONm-VmmTObyNWpz4hB3Hgx8ZWSb" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>



# Encrypted secrets

In the previous lessons we dealt with environment variables. Now say you want to hide them and load them into GitHub Actions. They could be your credentials, tokens, etc. 

> Recall
>
> ~~~
> build_skim:
>   needs: greeting
>   runs-on: ubuntu-latest
>   container: rootproject/root-conda:{% raw %}${{ matrix.version }}{% endraw %}
>   strategy:
>     matrix:
>       version: [6.18.04, latest]
>   steps:
>     - name: checkout repository
>       uses: actions/checkout@v2
>
>     - name: build
>       run: $COMPILER skim.cxx -o skim `root-config --cflags --glibs`
>       env:
>         COMPILER=g++
>
>     - uses: actions/upload-artifact@v2
>       with:
>         name: skim${{ matrix.root }}
>         path: skim
> ~~~
> {: .language-yaml}
{: .challenge}

## Running example

In the above `job` we have an environment variable called `COMPILER` that we would like to hide.

We first have to store its definition in GitHub:

1. navigate to the main page of the repository.
2. select `Settings`.
3. in the left sidebar, go to `Secrets` and then `New secret`.
4. type `COMPILER` in the Name input box and set the secret value to `g++`. 

> Let's remove the definition of `COMPILER` in the `main.yml`. 
>
> ~~~
> ...
> build_skim:
>   needs: greeting
>   runs-on: ubuntu-latest
>   container: rootproject/root-conda:{% raw %}${{ matrix.version }}{% endraw %}
>   strategy:
>     matrix:
>       version: [6.18.04, latest]
>   steps:
>     - name: checkout repository
>       uses: actions/checkout@v2
>
>     - name: build
>       run: $COMPILER skim.cxx -o skim `root-config --cflags --glibs`
>
>     - uses: actions/upload-artifact@v2
>       with:
>         name: skim{% raw %}${{ matrix.version }}{% endraw %}
>         path: skim
> ~~~
> {: .language-yaml}
{: .challenge}


> ## Failed to load secret?
> 
> How to access encrypted secrets in a workflow?
> Hint: $\{\{ secrets.\<secret name\> \}\}
>
> > ## Solution
> > ~~~
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
> >       run: {% raw %}${{ secrets.COMPILER }}{% endraw %} skim.cxx -o skim `root-config --cflags --glibs`
> >
> >     - uses: actions/upload-artifact@v2
> >       with:
> >         name: skim{% raw %}${{ matrix.version }}{% endraw %}
> >         path: skim
> > ~~~
> > {: .language-yaml}
> {: .solution}
{: .challenge}


![Actions_secret_variable]({{site.baseurl}}/fig/actions_secret_variable.png)


## Naming your secrets

Note that there are some rules applied to secret names:

- Secret names can only contain alphanumeric characters ([a-z], [A-Z], [0-9]) or underscores (_). Spaces are not allowed.
- Secret names must not start with the GITHUB_ prefix.
- Secret names must not start with a number.
- Secret names must be unique at the level they are created at. For example, a - - secret created at the organization-level must have a unique name at that level, and a secret created at the repository-level must have a unique name in that repository. If an organization-level secret has the same name as a repository-level secret, then the repository-level secret takes precedence.


> ## Further Reading
> - [https://docs.github.com/en/free-pro-team@latest/actions/reference/encrypted-secrets](https://docs.github.com/en/free-pro-team@latest/actions/reference/encrypted-secrets)
{: .checklist}

{% include links.md %}
