# Senior Design Project

## Installation and Running
Steps for the installation of the server are given for ubuntu. You will need to run the following commands, but a script (install.sh) has been provided on this github repository.

```bash
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

git clone https://github.com/raglnd/intell_game.git
cp INTELL_Game/cs499-intell-1.0.tar.gz ./
tar -xvf cs499-intell-1.0.tar.gz

python3 cs499-intell-1.0/manage.py makemigrations
python3 cs499-intell-1.0/manage.py migrate
python3 cs499-intell-1.0/manage.py test
```

You will also need to modify some of the settings in intell/settings.py, namely whether or not DEBUG is True or False and what the ALLOWED_HOSTS are. (Allowed hosts would be your external IP or domain name, or something similar.)
Below are some steps for successful running of the server.

```bash
# Steps for ease of use - must be run manually.
# python3 cs499-intell-1.0/manage.py createsuperuser
# python3 cs499-intell-1.0/manage.py crontab add

# How to run server without interruption.
# sudo nohup python3 cs499-intell-1.0/manage.py runserver 0.0.0.0:80 &
```
Once the server is running, you will need to load in the official scenario. Log in to the website (using either the admin user you just created, or a new user), go to the scenario editor, click the open button, select Official Scenario.json, and then click the submit button. The official scenario is located in the home folder of the git repo.