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
<!--
<iframe width="420" height="263" src="https://www.youtube.com/embed/XNhi1dw6jxI?list=PLKZ9c4ONm-VmmTObyNWpz4hB3Hgx8ZWSb" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
-->

> ## Recall
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
> skim:
>   needs: build_skim
>   runs-on: ubuntu-latest
>   container: rootproject/root-conda:6.18.04
>   steps:
>     - name: checkout repository
>       uses: actions/checkout@v2
>
>     - uses: actions/download-artifact@v2
>       with:
>         name: skim6.18.04
>
>     - name: skim
>       run: ./skim
> ~~~
> {: .language-yaml}
{: .challenge}

In the previous lesson, we saw that the executable `skim` takes 5 arguments: input (remote data), output (processed data), cross-section, integrated luminosity, and scale.

Let's consider the following values
```
input: root://eosuser.cern.ch//eos/user/g/gstark/AwesomeWorkshopFeb2020/GluGluToHToTauTau.root
output: skim_ggH.root
cross_section: 19.6
integrated_luminosity: 11467.0
scale: 0.1
```
<!-- 
root://eosuser.cern.ch//eos/user/g/gstark/AwesomeWorkshopFeb2020/GluGluToHToTauTau.root
root://eospublic.cern.ch//eos/root-eos/HiggsTauTauReduced/GluGluToHToTauTau.root
-->

Our YAML file should look like
~~~
...
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
       run: ./skim root://eosuser.cern.ch//eos/user/g/gstark/AwesomeWorkshopFeb2020/GluGluToHToTauTau.root skim_ggH.root 19.6 11467.0 0.1
~~~
{: .language-yaml}

What about the output?
~~~
>>> Process input: root://eosuser.cern.ch//eos/user/g/gstark/AwesomeWorkshopFeb2020/GluGluToHToTauTau.root
Error: n <TNetXNGFile::Open>: [ERROR] Server responded with an error: [3010] Unable to give access - user access restricted - unauthorized identity used ; Permission denied
~~~
{: .output}

# Access Control

The data we're using are on CERN User Storage (EOS). As a general rule, access to protected data should be authenticated, CERN can’t just grab it!.
It means we need to give our GitHub Actions access to our data.


Anyhow, this is done by pretty much done by executing `printf $USER_PASS | base64 -d | kinit $USER_NAME` assuming that we've set the corresponding environment variables by safely encoding them (`printf "hunter42" | base64`).

> ## Running example
>
> Sometimes you'll run into a code example here that you might want to run locally but relies on variables you might not have set? Sure, simply do the following
> ~~~
> USER_PASS=hunter42 USER_NAME=GoodWill printf $USER_PASS | base64 -d | kinit $USER_NAME
> ~~~
> {: .language-bash}
{: .callout}

> ## Base-64 encoding?
>
> Sometimes you have a string that contains certain characters that would be interpreted incorrectly by GitHub Actions runners. In order to protect against that, you can safely base-64 encode the string, store it, and then decode it as part of the Actions job. This is entirely safe and recommended.
{: .callout}

# Encrypted secrets

We first have to store our sensitive information in GitHub:

1. navigate to the main page of the repository.
2. select `Settings`.
3. in the left sidebar, go to `Secrets` and then `New secret`.
4. type `USER_NAME` in the Name input box and add the secret value.
5. similarly add `USER_PASS` as well.
6. Click to save the variables.


## Naming your secrets

Note that there are some rules applied to secret names:

- Secret names can only contain alphanumeric characters ([a-z], [A-Z], [0-9]) or underscores (_). Spaces are not allowed.
- Secret names must not start with the GITHUB_ prefix.
- Secret names must not start with a number.
- Secret names must be unique at the level they are created at. For example, a - - secret created at the organization-level must have a unique name at that level, and a secret created at the repository-level must have a unique name in that repository. If an organization-level secret has the same name as a repository-level secret, then the repository-level secret takes precedence.



> ## Access encrypted secrets
> The secrets you've created are available to use in GitHub Actions workflows. GitHub allows to access them using secrets context: $\{\{ secrets.\<secret name\> \}\}.
> 
> e.g:
> ~~~
> printf {% raw %}${{ secrets.USER_PASS }}{% endraw %} | base64 -d | kinit {% raw %}${{ secrets.USER_NAME }}{% endraw %}
> ~~~
> {: .language-bash}
{: .challenge}




![Actions_secret_variable]({{site.baseurl}}/fig/actions_secret_variable.png)



> ## Further Reading
> - [https://docs.github.com/en/free-pro-team@latest/actions/reference/encrypted-secrets](https://docs.github.com/en/free-pro-team@latest/actions/reference/encrypted-secrets)
{: .checklist}

{% include links.md %}
