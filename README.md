[Docker for Mac]: https://docs.docker.com/docker-for-mac/install/  "Download Docker for Mac"
[Docker for Windows]: https://docs.docker.com/docker-for-windows/install/  "Download Docker for Windows"
[Docker Hub]: https://hub.docker.com/ "Docker Hub Homepage"
[BLITZ DockerHub]: https://hub.docker.com/u/blitzagency/ "BLITZ DockerHub"
[Node & Npm]: https://nodejs.org/en/download/ "Intsall Node"
[Homebrew]: http://brew.sh/ "Homebrew Homepage"
[Heroku]: https://www.heroku.com/ "Heroku Homepage"

# Mission

## Contribute

- [See CONTRIBUTING.md](./CONTRIBUTING.md)

## Learn

- [Docs](./docs)

## Required

- [Docker Hub] account (req. for deploys)
- [BLITZ DockerHub] Access (req. for deploys)
- BLITZ [Heroku] Access (or a valid Heroku account added as a collaborator) (req. for deploys)
- [Docker for Mac] __or__ [Docker for Windows]
- [Node & Npm]
    - Must be installed locally
    - [OSX] `brew install node` (requires [Homebrew])

## Setup

> If you're running __Windows__, please first read [Initial Setup For Windows](./docs/windows-setup.md).

```bash
# From a terminal run
# After running this, you may need to fill out required settings
cp site/env.dist site/.env

make up
make init
# To get data for testing. This use a fixture to import data into your DB.
# Add a setting to your .env file: REMOTE_MEDIA_URL='http://staging.missionfoods.com/uploads/
# This will serve images from the staging site
make fixture
# start the webserver
make serve

# From another terminal run
make assets
```

> Site is available at <http://localhost:8000>, <http://docker.local:8000> (requires etc/hosts entry).

## Start

```bash
# From a terminal run
make up
make serve

# From another terminal run
make assets
```

> Site is available at <http://localhost:8000>, <http://docker.local:8000> (requires etc/hosts entry).

## Test

```bash
# Run Python / Django test suite
make test.py

# Run Javascript test suite
make test.js
```

## Automate

```bash
# To see latest help message run
make help
```

## Deploy

> TODO: Update this table as env's become available

| Env Name | Description | Available |
|:-        | :-          | :-        |
| Dev      | This is a raw testing environment, least stable | no
| Staging  | This is a client preview enviornment, more stable than dev | no
| Prod     | This is the live enviornment, stable | no

### Setup

```bash
git remote add dev https://git.heroku.com/mission-dev.git
git remote add staging https://git.heroku.com/mission-staging.git
git remote add prod https://git.heroku.com/mission-prod.git
```

### Push

```bash
# Valid env-names are:
# dev
# staging
# prod
make heroku.deploy ENV_NAME=<env-name>
```



## Notes

### Images in HTML
> This setup isn't ideal, we are looking for alternatives. 😞

Images in HTML and other files that do not use a `require` statement (except for .scss) will not be picked up / watched by Webpack. A workaround has been added to __@static/@imgs__.

This workaround forces webpack to copy all image files under __@static/@imgs__ into the path specified in the loader configured to load images in __webpack.config.js__.

There are a couple of gotchas:


1. Any subdirs in __@imgs__ are discarded, so simply reference image paths like so: `{% static "imgs/path-to-file-no-subdir.png" %}`.
2. All image files _must have unique names_.
3. If webpack isn't picking up new image files in __@imgs__ restart the `make assets` process.
