#!/bin/bash

set -e

# Create a log file of the build as well as displaying the build on the tty as it runs
exec &> >(tee collector_install.log)
exec 2>&1

#Install the dependencies
sudo apt-get update

#Install pip to allow Python stuff to be installed
sudo apt-get install python-pip

#Use pip to install psutils so that the collector can get CPU and memeory stats
sudo pip install psutil

#Install request to allow data to be sent
sudo apt-get update
sudo apt-get install python-requests
