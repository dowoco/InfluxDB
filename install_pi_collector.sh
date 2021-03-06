#!/bin/bash

set -e

# Create a log file of the build as well as displaying the build on the tty as it runs
exec &> >(tee collector_install.log)
exec 2>&1

#Download the collector.py file overwriting any existing ones
wget -q https://raw.githubusercontent.com/dowoco/InfluxDB/master/collector.py -O collector.py

#Add execute priveliges to the collector.py file
chmod +x collector.py

#Install the dependencies
sudo apt-get update

#Install pip to allow Python stuff to be installed
sudo apt-get install python-pip -y

#Use pip to install psutils so that the collector can get CPU and memeory stats
sudo pip install psutil

#Install request to allow data to be sent
sudo apt-get update
sudo apt-get install python-requests -y

#Get the Unit File that will be used to run collector.py as a service
wget -q https://raw.githubusercontent.com/dowoco/InfluxDB/master/collector.service -O collector.service
sudo mv -f collector.service /lib/systemd/system/collector.service

#Set permissions on the Unit File
sudo chmod 644 /lib/systemd/system/collector.service

#Setup Service
sudo systemctl daemon-reload
sudo systemctl enable collector.service

echo Installed, just reboot
