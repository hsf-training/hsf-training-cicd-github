+++
exercises = 10
hidden = false
keypoints = ['Secrets in GitHub actions allow you to hide protected information from others who can see your code']
objectives = ['Add custom environment variables', 'Learn how to give your CI/CD Runners access to private information']
questions = ['How can I give my GitHub actions private information?']
teaching = 5
title = 'Getting into the Spy Game'
weight = 130
+++
<!-- Service accounts provide an extra layer of security between the outside world and your account-->

<!--
{{< youtube arfeBX-wOxs >}}
-->

{{< youtube Bu8-gjtqQNM >}}

{{< challenge title="Recall" >}}
```yaml
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
        ./skim
```
{{< /challenge >}}

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
```yaml
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
         ./skim root://eosuser.cern.ch//eos/user/g/gstark/AwesomeWorkshopFeb2020/GluGluToHToTauTau.root skim_ggH.root 19.6 11467.0 0.1
```

What about the output?
```text
>>> Process input: root://eosuser.cern.ch//eos/user/g/gstark/AwesomeWorkshopFeb2020/GluGluToHToTauTau.root
Error: n <TNetXNGFile::Open>: [ERROR] Server responded with an error: [3010] Unable to give access - user access restricted - unauthorized identity used ; Permission denied
```

## Access Control

The data we're using are on CERN User Storage (EOS). As a general rule, access to protected data should be authenticated, CERN can’t just grab it!.
It means we need to give our GitHub Actions access to our data. CERN uses `kinit` for access control.

Anyhow, this is pretty much done by executing `echo $USER_PASS | kinit $USER_NAME@CERN.CH` assuming that we've set the corresponding environment variables.

If you are not a CERN user, don't worry. We have a backup solution for you!
You can use this file `root://eospublic.cern.ch//eos/root-eos/HiggsTauTauReduced/GluGluToHToTauTau.root` and skip the rest of this lesson.

If this still does not work, for example if the port xrootd uses to fetch the data is blocked on your network, you can instead use `https://root.cern/files/HiggsTauTauReduced/GluGluToHToTauTau.root`.


{{< callout type="note" title="Running example" >}}
Sometimes you'll run into a code example here that you might want to run locally but relies on variables you might not have set? Sure, simply do the following
```bash
USER_PASS=hunter42 USER_NAME=GoodWill echo $USER_PASS | kinit $USER_NAME@CERN.CH
```
{{< /callout >}}

## GitHub secrets

We first have to store our sensitive information in GitHub:

1. Navigate to the main page of the repository.
2. Select `Settings`.
3. In the left sidebar, go to `Secrets and variables`, then `Actions`, and then `New repository secret`.
4. Type `USER_NAME` in the Name input box and add your username in the Secret input box.
5. Similarly add `USER_PASS` as well.

{{< callout type="testimonial" title="DON'T PEEK" >}}
DON'T PEEK AT YOUR FRIEND'S SCREEN WHILE DOING THIS.
{{< /callout >}}


### Naming your secrets

Note that there are some rules applied to secret names:

- Secret names can only contain alphanumeric characters ([a-z], [A-Z], [0-9]) or underscores (_). Spaces are not allowed.
- Secret names must not start with the GITHUB_ prefix.
- Secret names must not start with a number.
- Secret names must be unique at the level they are created at. For example, a secret created at the organization-level must have a unique name at that level, and a secret created at the repository-level must have a unique name in that repository. If an organization-level secret has the same name as a repository-level secret, then the repository-level secret takes precedence.


{{< challenge title="Access secrets" >}}
The secrets you've created are available to use in GitHub Actions workflows. GitHub allows to access them using secrets context: $\{\{ secrets.\<secret name\> \}\}.

e.g:

```bash
echo ${{ secrets.USER_PASS }} | kinit ${{ secrets.USER_NAME }}@CERN.CH
```
{{< /challenge >}}


<!--
![Actions_secret_variable](fig/actions_secret_variable.png)
-->


{{< callout type="checklist" title="Further Reading" >}}
- [https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions)
{{< /callout >}}

## Adding Artifacts on Success

As it seems like we have a complete CI/CD that does physics - we should see what came out. We just need to add artifacts for the `skim` job. This is left as an exercise to you.

{{< challenge title="Adding Artifacts" >}}
Let's add `artifacts` to our `skim` job to save the `skim_ggH.root` file. Let's have the artifacts expire in a week instead.

{{< solution title="Solution" >}}
```yaml
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

     - name: access control
       run: echo ${{ secrets.USER_PASS }} | kinit ${{ secrets.USER_NAME }}@CERN.CH

     - name: skim
       run: |
         chmod +x ./skim
         ./skim root://eosuser.cern.ch//eos/user/g/gstark/AwesomeWorkshopFeb2020/GluGluToHToTauTau.root skim_ggH.root 19.6 11467.0 0.1

     - uses: actions/upload-artifact@v4
       with:
         name: skim_ggH
         path: skim_ggH.root
         retention-days: 7
```
{{< /solution >}}
{{< /challenge >}}

And this allows us to download artifacts from the successfully run job.
