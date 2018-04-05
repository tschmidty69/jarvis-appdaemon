# Welcome to The Magic Door on Snips!



### INSTALL

sudo apt-get -y install python3-pip python3-venv curl mpg321

sudo python3 -m venv /srv/jarvis
sudo chown -R pi.pi /srv/jarvis
source /srv/jarvis/bin/activate

pip3 install appdaemon
pip3 install paho-mqtt

cd /srv/jarvis
wget

### Running

There will be lots of debug output. Ignore an error about players list.

```appdaemon -c /srv/jarvis```

### Uninstall

```rm -rf /srv/jarvis```
