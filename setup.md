---
title: Setup
questions:
- "What do I need to start?"

---
## Prerequisites
> - We assume that you already have a Github account
> - You should have git working on your laptop
{: .prereq}


## ROOT setup
This exemple analysis needs ROOT software (>=6.16). The CI tools will handle this, but to anticipate what CI tool will do you need ROOT on your laptop.

If you don't have ROOT installed on your laptop, you can choose one of the following options

### Option 1: using docker
In order to run ROOT image "*rootproject/root-conda*" as container, you must have Docker installed. If this is not the case, install docker following the instructions [here](https://docs.docker.com/engine/install).

Once Docker is installed, you can run (you might need to run with *sudo*)

 ```bash
 docker run --rm -it  rootproject/root-conda
 root-config --version # check ROOT version
 exit
 ```
The `--rm` flag automatically cleans up the container on exit, `-t` to access the terminal, and`-i` for interactive mode. For more details, please refer to [Getting started](https://hub.docker.com/r/rootproject/root) section.


### Option 2: using conda
Make sure conda is installed otherwise go to [installation](https://docs.conda.io/projects/conda/en/latest/user-guide/install) section or refer to instructions in this [presentation](https://indico.cern.ch/event/759388/contributions/3306849/attachments/1816254/2968550/root_conda_forge.pdf).

Create an environment named "*root_env*" that contains Python 3.8 and ROOT:
 ```bash
 conda create -n root_env python=3.8 root -c conda-forge
 ```

Now you can run ROOT inside the new environment
 ```bash
 conda activate root_env
 root-config --version # check ROOT version
 conda deactivate
 ```
To remove the environment, run `conda env remove -n root_env`.


## Extra tool: act

This tool [act](https://github.com/nektos/act) will allow us to run CI tests locally. 

For Docker users run
  ```bash
  curl https://raw.githubusercontent.com/nektos/act/master/install.sh | bash
  ```
Otherwise you may have to run with *sudo*
  ```bash
  curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
  ```

## Set up new project

- Create a new project on your personal github account called *virtual-pipelines-eventselection*.

  > Make sure you click Public for the visibility level of the new project so that everyone can see your awesome work
  > (and it will also make things easier when we get to working with containers).
  > ![example of a properly-filled-in blank project form for gitlab]({{site.baseurl}}/fig/blank-project-form.png)
  {: .callout}

- Get the code

  ```bash
  git clone https://github.com/awesome-workshop/payload.git virtual-pipelines-eventselection
  ```

- We need to add the code to the new project (your github) 

  ```bash
  git remote -v
  ```
  ```
  origin	https://github.com/awesome-workshop/payload.git (fetch)
  origin	https://github.com/awesome-workshop/payload.git (push)  
  ```
  
- Rename the origin url

  ```bash
  git remote set-url https://github.com/<your login>/virtual-pipelines-eventselection.git
  ```

## Video Tutorials
<iframe width="420" height="263" src="https://www.youtube.com/embed/NcVGX8zWzQY?list=PLKZ9c4ONm-VmmTObyNWpz4hB3Hgx8ZWSb" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


If you're having issues, **please let us know immediately**
since you might not be able to follow this lesson without a proper setup.
