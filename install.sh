#!/usr/bin/env bash

sudo apt install -y python3-pip
sudo apt install -y npm
sudo apt install -y git
sudo ln -s /usr/bin/nodejs /usr/bin/node

pip3 install --upgrade pip
sudo pip3 install Django==1.10.5
sudo pip3 install django-crontab
sudo pip3 install django-jenkins

sudo npm install -g phantomjs-prebuilt 
sudo npm install -g casperjs 
sudo pip3 install django-casper
sudo sed -i 's/django.test/django.contrib.staticfiles.testing/g' /usr/local/lib/python3.5/dist-packages/casper/tests.py
sudo sed -i 's/LiveServerTestCase/StaticLiveServerTestCase/g' /usr/local/lib/python3.5/dist-packages/casper/tests.py

sudo apt-get install sqlite3 libsqlite3-dev

sudo apt-get install -y python-software-properties
sudo add-apt-repository -y ppa:openjdk-r/ppa
sudo apt-get update
sudo apt-get install -y openjdk-7-jdk

git clone https://github.com/Numorphan/INTELL_Game.git
cp INTELL_Game/cs499-intell-1.0.tar.gz ./
tar -xvf cs499-intell-1.0.tar.gz

python3 cs499-intell-1.0/manage.py makemigrations
python3 cs499-intell-1.0/manage.py migrate