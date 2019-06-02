#!/usr/bin/env bash

export DEBIAN_FRONTEND=noninteractive

apt-get update
apt-get upgrade -y

PACKAGES=$(xargs <<EOF
apt-utils
EOF
)

apt-get install -y $PACKAGES
apt-get clean