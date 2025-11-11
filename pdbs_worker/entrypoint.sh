#!/bin/bash

micromamba activate proteindj

# This will exec the CMD from your Dockerfile, i.e. "npm start"
exec "$@"
