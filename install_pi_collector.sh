#!/bin/bash

set -e

# Create a log file of the build as well as displaying the build on the tty as it runs
exec &> >(tee collector_install.log)
exec 2>&1

#Install the dependencies
apt-get update
