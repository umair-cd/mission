# -------------------------------------
# DOCKERFILE
# -------------------------------------
# https://github.com/blitzagency/python-web
# https://hub.docker.com/r/blitzagency/python-web/

FROM blitzagency/python-web:3

# Build Args
# =====================================
# These are passed via the --build-arg flag during `docker build`
ARG ASSET_VERSION

# ENV Setup
# =====================================

# Single line form is preferred for caching
ENV PYTHONPATH=/usr/app/site/apps:/usr/app/site/vendor \
    DJANGO_SETTINGS_MODULE=apps.config.settings.prod

# Working Dir Setup
# =====================================
# We're about to work with the local context alot,
# let's make paths a little easir

WORKDIR /usr/app

# Install Dependencies
# =====================================

# Copy requirements before copying over all other files,
# preferred better caching, see:
# https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/#add-or-copy
#
# NOTE: Avoiding ./requirements/local.txt so we don't invalidate the cache for
# a local only update to reqs.

COPY ./site/requirements/base.txt ./requirements/base.txt
COPY ./site/requirements/production.txt ./requirements/production.txt
COPY ./site/requirements.txt ./

RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev

RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

# NOTE: Mostly everything that follows will invalidate the cache

# Copy Local Files
# =====================================
# Copy is (usually) preferred over Add, see:
#   https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/#add-or-copy

COPY ./site/ ./

# Copy env.build to .env temporarily for collect static
# NOTE: This overwrites any .env that may have been added from COPY above
RUN [ -f ./.build/.env ] || echo "Could not find ./.build/.env"
COPY ./site/.build/.env .env

# Run Collect Static
# =====================================

RUN python manage.py collectstatic --no-input

# We can get rid of .env now
# but leave env.build to keep as a build receipt.
RUN rm /usr/app/.env

# Asset Version
# =====================================
# Permanently embed ASSET_VERSION into container
# Separate from other ENV to avoid
# early / unintentional cache invalidation

ENV ASSET_VERSION=$ASSET_VERSION

# User Setup
# =====================================
# Recommended, run the image as non-root
# See: https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/#user

RUN adduser -D heroku
USER heroku

# Start the App
# =====================================
# CMD is required to run on Heroku
# $PORT is set by Heroku

CMD newrelic-admin run-program gunicorn apps.config.wsgi --bind 0.0.0.0:$PORT -w 3 -k gevent
