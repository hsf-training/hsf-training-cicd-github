+++
exercises = 0
keypoints = [' Python packages can be installed in Docker images along with ubuntu packages.', ' It is possible to publish and share Docker images over github packages.']
objectives = ['To be able to build a Docker container and share it via GitHub packages']
questions = ['How to build a Docker container for python packages?', 'How to share Docker images?']
teaching = 40
title = 'Bonus Episode: Building and deploying a Docker container to Github Packages'
weight = 170
+++
{{< callout type="prereq" title="Prerequisites" >}}
For this lesson you should already be familiar with Docker images.
Head over to [our training on Docker](https://hsf-training.github.io/hsf-training-docker/) if you aren't already!
{{< /callout >}}

### Docker Container for python packages

Python packages can be installed using a Docker image. The following example illustrates how to write a Dockerfile for building an image containing python packages.

```dockerfile
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
  && apt-get install wget -y \
  && apt-get install dpkg-dev cmake g++ gcc binutils libx11-dev libxpm-dev \
    libxft-dev libxext-dev python3 libssl-dev libgsl0-dev libtiff-dev \
    python3-pip -y

RUN pip3 install numpy awkward uproot4 particle hepunits matplotlib \
  mplhep vector fastjet iminuit
```

As we see, several packages are installed.

### Publish Docker images with GitHub/Gitea Packages and share them!

It is possible to publish Docker images with [GitHub packages](https://github.com/features/packages)
or with Gitea's built-in [container registry](https://docs.gitea.com/usage/packages/container).
To do so, one needs to use GitHub/Gitea CI/CD. A step-by-step guide is presented here.

* **Step 1**: Create a GitHub/Gitea repository and clone it locally.
* **Step 2**: In the empty repository, make a folder called `.github/workflows`. In this folder we will store the file containing the YAML script for a workflow, named `Docker-build-deploy.yml` (the name doesn't really matter).
* **Step 3**: In the top directory of your repository, create a file named `Dockerfile`.
* **Step 4**: Copy-paste the content above and add it to the Dockerfile. (In principle it is possible to build this image locally, but we will not do that here, as we wish to build it with CI/CD).
* **Step 5**: In the `Docker-build-deploy.yml` file, add the content below.
* **Step 6**: Add LICENSE and README as recommended in the [SW Carpentry Git-Novice Lesson](https://swcarpentry.github.io/git-novice/), and then the repository is good to go.

{{< tabs >}}
{{< tab name="GitHub" selected=true >}}

```yaml
name: Create and publish a Docker image

on:
  pull_request:
  push:
    branches: main

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-push-image:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Log in to the Container registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Docker Metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```

{{< /tab >}}
{{< tab name="Gitea" >}}

```yaml
name: Create and publish a Docker image

on:
  pull_request:
  push:
    branches: main

env:
  # the hostname of your Gitea instance, e.g. gitea.psi.ch
  REGISTRY: <gitea.example.com>
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-push-image:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: https://github.com/actions/checkout@v4

      - name: Log in to the Container registry
        uses: https://github.com/docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.REGISTRY_TOKEN }}

      - name: Docker Metadata
        id: meta
        uses: https://github.com/docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}

      - name: Build and push Docker image
        uses: https://github.com/docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```

{{< /tab >}}
{{< /tabs >}}

Note that on Gitea the automatic `secrets.GITHUB_TOKEN` [cannot write to the package registry](https://github.com/go-gitea/gitea/issues/23642), so generate a personal access token with read and write permission on `package` (**Settings → Applications**) and add it to the repository as the secret `REGISTRY_TOKEN`.
