+++
questions = ['What do I need to start?']
title = 'Setup'
+++
<!--## Video Tutorials
{{< youtube -Xd5D6xKugk >}}
-->

{{< youtube RSj_0vtE1ZA >}}

{{< callout type="note" title="GitHub versus Gitea" >}}
This course is compatible with Github and Gitea.

Gitea is meant to be a drop-in replacement for GitHub, this course will only menton Gitea explicitly when this does not hold.
Otherwise, you can assume that what works for GitHub will work for Gitea.

The Gitea actions, for example, described later in this course are meant to be compatible with GitHub actions, but there are still some differences between the two.
A full comparison can be found [here](https://docs.gitea.com/usage/actions/comparison/) in Gitea's documentation.
{{< /callout >}}

## Set up Python

Part of this lesson consists in learning how to make scripts exit correctly. At some point, we will need to test exit codes with Pytest, Python testing tool.

To know whether your Python has `pytest`, just run `python -c "import pytest"`. If this command returns nothing, it means everything is fine. Otherwise, it can be installed by running `python -m pip install -U pytest`. More information can be found in the [`pytest` website](https://docs.pytest.org/en/stable/getting-started.html) for installation.


## Set up the code

1. Create a new project on your personal GitHub/Gitea account and name it `virtual-pipelines-eventselection`.

    Make sure you set the visibility level of the new project to public so that everyone can see your awesome work.

    {{< tabs >}}
    {{< tab name="GitHub" selected=true >}}
    ![example of a properly-filled-in blank project form](fig/blank-project-form.png)

    {{< /tab >}}
    {{< tab name="Gitea" >}}
    ![example of a properly-filled-in blank project form](fig/gitea_blank_project_form.png)

    {{< /tab >}}
    {{< /tabs >}}

2. Get the code

    Open a terminal and clone the repository that contains files required for this lesson.

    ```bash
    git clone git@github.com:hsf-training/hsf-training-cms-analysis.git virtual-pipelines-eventselection
    cd virtual-pipelines-eventselection
    ```

3. Add the code to your personal GitHub/Gitea account

    At the moment, your clone is the remote repository stored on someone GitHub account. To get the name of the existing remote use
    ```bash
    git remote -v # -v stands for verbose
    ```

    ```
    origin	git@github.com:hsf-training/hsf-training-cms-analysis.git (fetch)
    origin	git@github.com:hsf-training/hsf-training-cms-analysis.git (push)
    ```

    You have to change remote's URL in order to be able to add the code to your personal GitHub account.


    {{< tabs >}}
    {{< tab name="GitHub" selected=true >}}

    ```bash
    git remote set-url origin git@github.com:<GitHub username>/virtual-pipelines-eventselection.git
    ```

    {{< /tab >}}
    {{< tab name="Gitea" >}}

    ```bash
    git remote set-url origin <gitea clone url of new project>
    
    # e.g.
    # git@gitea.psi.ch:fatour_m/virtual-pipelines-eventselection.git
    ```

    {{< /tab >}}
    {{< /tabs >}}


    Check again the name of the current remote:
    ```bash
    git remote -v
    ```

4. The last step is to rename the branch to main, and push it to GitHub.
    ```bash
    git branch -M main
    git push -u origin main
    ```
    This will add the code to your new repository on GitHub. Done!
  
  

If you're having issues, **please let us know immediately**
since you might not be able to follow this lesson without a proper setup.
