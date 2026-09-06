# Continuous Integration and Deployment (CI/CD) with GitHub
[![HSF Training Center][training-center-badge]][hsf-training-center]
[![Upcoming Events][schools-badge]][schools]
[![Twitter Follow][twitter-badge]][twitter]
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-4-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/hsf-training/hsf-training-cicd-github/gh-pages.svg)](https://results.pre-commit.ci/latest/github/hsf-training/hsf-training-cicd-github/gh-pages)
[![pages-build-deployment](https://github.com/hsf-training/hsf-training-cicd-github/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/hsf-training/hsf-training-cicd-github/actions/workflows/pages/pages-build-deployment)

> **Note**
> Click [here](https://hsf-training.github.io/hsf-training-cicd-github/) for the training website!

This learning module explores how to build a CI/CD workflow, guiding participants through the development of automated processes using GitHub actions.      

## Records from past events

* 🎥 [GitHub CI/CD Training](https://indico.cern.ch/event/1001128/)

## Contributing
<!-- CENTRALLY MAINTAINED SECTION -->
<!-- Remove the above marker to disable having this section be overwritten -->

We welcome all contributions to improve the lesson! Maintainers will do their best to help you if you have any
questions, concerns, or experience any difficulties along the way.

If you make non-trivial changes (i.e., more than fixing a simple typo), you are eligible to be added to the [HSF Training Community page][hsf-training-community],
as well as to the list of contributors [below](#contributors-).

We'd like to ask you to familiarize yourself with our [Contribution Guide](CONTRIBUTING.md) and have a look at
the [more detailed guidelines][lesson-example] on proper formatting, ways to render the lesson locally, and even
how to write new episodes.

Quick summary of how to get a local preview: Install [jekyll][jekyll] and then run

```
bundle install
bundle update
bundle exec jekyll serve
```

Unless we change framework versions, only the last command needs to be typed after the first time.

Before committing anything, we also ask you to install the [pre-commit][pre-commit] hooks of this repository:

```bash
pip3 install pre-commit
pre-commit install
```

Please see the current list of [issues][issues] for ideas for contributing to this
repository. For making your contribution, we use the GitHub flow, which is
nicely explained in the chapter [Contributing to a Project][progit] in Pro Git
by Scott Chacon.
Look for the tag ![good first issue][gfi-badge], which marks particularly simple issues to get you started.

<!-- END CENTRALLY MAINTAINED SECTION -->

## Authors

<!-- If we have a primary author/maintainer, who kicked off the whole lessen etc, he should get a dedicated shoutout here -->

Thanks goes to these wonderful people who contributed to
the content of the lesson:

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/enibigir"><img src="https://avatars.githubusercontent.com/u/38688778?v=4?s=100" width="100px;" alt="Emery Nibigira"/><br /><sub><b>Emery Nibigira</b></sub></a><br /><a href="#content-enibigir" title="Content">🖋</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/fleble"><img src="https://avatars.githubusercontent.com/u/69905035?v=4?s=100" width="100px;" alt="Florian Eble"/><br /><sub><b>Florian Eble</b></sub></a><br /><a href="https://github.com/hsf-training/hsf-training-cicd-github/issues?q=author%3Afleble" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/amanmdesai"><img src="https://avatars.githubusercontent.com/u/98302868?v=4?s=100" width="100px;" alt="Aman Desai"/><br /><sub><b>Aman Desai</b></sub></a><br /><a href="#content-amanmdesai" title="Content">🖋</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://saransh-cpp.github.io/"><img src="https://avatars.githubusercontent.com/u/74055102?v=4?s=100" width="100px;" alt="Saransh Chopra"/><br /><sub><b>Saransh Chopra</b></sub></a><br /><a href="#content-Saransh-cpp" title="Content">🖋</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

Even more people contributed to the framework, but they are too many to list!
Instead, all regular contributors are listed on our [HSF Training Community page][hsf-training-community].

## Citation

To cite this lesson, please consult with [CITATION](CITATION.cff)

## Open Educational Resources (OER) on Zenodo

This lesson is included in the [HEP Software Foundation Training Material](https://zenodo.org/communities/hsf-training/records) and in the [ETH Domain Open Educational Resources for Research Data Management](https://zenodo.org/communities/eth-domain-oer-rdm/records) communities on Zenodo.                                    

The materials developed here are published under open licenses (CC BY 4.0) and can be freely reused and adapted for teaching and training initiatives worldwide.

See the Zenodo record [here](https://doi.org/10.5281/zenodo.22016969).


[lesson-example]: https://carpentries.github.io/lesson-example
[pre-commit]: https://pre-commit.com/
[hsf-training-community]: https://hepsoftwarefoundation.org/training/community
[hsf-training-center]: https://hepsoftwarefoundation.org/training/curriculum.html
[training-center-badge]: https://img.shields.io/badge/HSF%20Training%20Center-browse-ff69b4
[schools]: https://hepsoftwarefoundation.org/Schools/events.html
[issues]: https://github.com/hsf-training/hsf-training-cicd-github/issues
[progit]: http://git-scm.com/book/en/v2/GitHub-Contributing-to-a-Project
[jekyll]: https://jekyllrb.com/
[allcontrib-emoji-key]: https://allcontributors.org/docs/en/emoji-key
[gfi-badge]: https://img.shields.io/badge/-good%20first%20issue-gold.svg
[schools-badge]: https://img.shields.io/badge/upcoming%20events-browse-ff69b4
[twitter-badge]: https://img.shields.io/twitter/follow/hsftraining?style=social
[twitter]: https://twitter.com/hsftraining
