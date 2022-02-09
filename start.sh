#!/bin/sh
# Entrypoint for Railway

set -eux

prisma generate

python -m bot
