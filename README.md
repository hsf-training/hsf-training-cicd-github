[![github pages](https://github.com/hsf-training/hsf-training-cicd-github/actions/workflows/website.yml/badge.svg)](https://github.com/hsf-training/hsf-training-cicd-github/actions/workflows/website.yml)
[![HSF Training Center](https://img.shields.io/badge/HSF%20Training%20Center-browse-ff69b4)](https://hepsoftwarefoundation.org/training/curriculum.html)

HSF Training CI/CD -- Github Edition
====================================

An introduction to continuous integration (CI) and continuous deployment (CD) using GitHub Actions. This repository holds the source code of the webpage that is rendered [here](https://hsf-training.github.io/hsf-training-cicd-github/). Contributions are welcome (see below)!

This training module is part of an initiative of the [HEP Software foundation](https://hepsoftwarefoundation.org/) to build up a full software [training curriculum](https://hepsoftwarefoundation.org/training/curriculum) for high energy physics.

## Contributing

1. If you find a problem or have a suggestion but don't know how to (or don't have the time to) solve it yourself, [file an issue in this repository](https://github.com/hsf-training/hsf-training-cicd-github/issues)
2. If you want to contribute, please fork this repository and submit a pull request.

## Local preview and development

1.  To preview material,
    please run `make serve` from the command line
    to launch Jekyll with the correct parameters,
    or push to your repository's `gh-pages` branch
    and let GitHub take care of the rendering.
2.  Run `make lesson-check` to check that your files follow our formatting rules.
