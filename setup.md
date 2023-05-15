---
title: Setup
questions:
- "What do I need to start?"
---

<!--## Video Tutorials-->
<iframe width="560" height="315" src="https://www.youtube.com/embed/-Xd5D6xKugk" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


## Set up Python

Part of this lesson consists in learning how to make scripts exit correctly. At some point, we will need to test exit codes with Pytest, Python testing tool.

To know whether your Python has `pytest`, just run `python -c "import pytest"`. If this command returns nothing, it means everything is fine. Otherwise, please visit [https://docs.pytest.org/en/stable/getting-started.html](https://docs.pytest.org/en/stable/getting-started.html) for installation.

## Set up ACT

An optional substitute for running GitHub Actions is the `nektos/act` tool, which runs GitHub commands locally.

Make sure you have it properly installed. Instructions can be found at this web page [https://github.com/nektos/act](https://github.com/nektos/act#installation).

Once the installation is done, you can run a quick test:
```bash
act --version
```

## Set up Docker

`nektos/act` uses `Docker` to run GitHub Actions on your computer. Therefore you must have Docker installed.

If this is not the case, follow the above link for instructions.

- Install Docker:  [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)
<!-- Mac OS:  [https://docs.docker.com/docker-for-mac/install/](https://docs.docker.com/docker-for-mac/install/)-->
<!-- Windows: [https://docs.docker.com/docker-for-windows/install/](https://docs.docker.com/docker-for-windows/install/)-->

To check your installation open a terminal and run:
  ```bash
  docker --version
  ```
**Note** that you may have to run with *sudo*. If you don’t want to preface the *docker* command with *sudo*, you may need to checkout [https://docs.docker.com/engine/install/linux-postinstall/](https://docs.docker.com/engine/install/linux-postinstall/).


## Set up the code

- Create a new project on your personal GitHub account and name it `virtual-pipelines-eventselection`.

  Make sure you click Public for the visibility level of the new project so that everyone can see your awesome work.
  ![example of a properly-filled-in blank project form for gitlab]({{site.baseurl}}/fig/blank-project-form.png)
  {: .callout}

- Get the code

  Open a terminal and clone the repository that contains files required for this lesson.

  ```bash
  git clone git@github.com:hsf-training/hsf-training-cms-analysis.git virtual-pipelines-eventselection
  cd virtual-pipelines-eventselection
  ```

- Add the code to your personal GitHub account

  At the moment, your clone is the remote repository stored on someone GitHub account. To get the name of the existing remote use
  ```bash
  git remote -v # -v stands for verbose
  ```

  ```
  origin	git@github.com:hsf-training/hsf-training-cms-analysis.git (fetch)
  origin	git@github.com:hsf-training/hsf-training-cms-analysis.git (push)
  ```
  {: .output}

  You have to change remote's URL in order to be able to add the code to your personal GitHub account.

  ```bash
  git remote set-url origin git@github.com:<GitHub username>/virtual-pipelines-eventselection.git
  ```
  Check again the name of the current remote:
  ```bash
  git remote -v
  ```

  The last step is to run the push command as follows
  ```bash
  git push -u origin master
  ```
  This will add the code to your GitHub account. Done!

If you're having issues, **please let us know immediately**
since you might not be able to follow this lesson without a proper setup.
