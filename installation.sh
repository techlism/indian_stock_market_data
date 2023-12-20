#!/bin/bash

# Install tools required to extract Chrome version
apt-get install -y wget unzip

CHROME_VERSION=$(google-chrome-stable --version | grep -oP '(?<=Google Chrome )[^ ]+')
CHROME_URL=https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROME_VERSION/linux64/chromedriver-linux64.zip
wget -q $CHROME_URL
unzip chromedriver-linux64.zip
chmod +x chromedriver-linux64/chromedriver
