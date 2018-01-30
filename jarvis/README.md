# Jarvis 
##  An Appdaemon App for use with the Snips Voice Assistant and HomeAssistant

Control your home using Snips <https://github.com/snipsco/snips-platform-documentation/wiki>, 
a Voice Assistant that runs entirely locally.

This app is intended to be deployed on Appdaemon version 3 <http://appdaemon.readthedocs.io/en/latest/index.html>

It is mainly intended for use with Home Assistant at this point, but plans are to have a standalone mode and 
*maybe* write an OpenHab plugin.

### Installation

- Install Snips
- Install Appdaemon V3
- Install this app in your apps folder (git clone the repo)
- Configure it

### Configuration

Configure it
Edit the jarvis/jarvis.yaml and enable modules and add settings

###  Configuring Snips

Create your assistant and add these bundles

#### Snips
Smart Lights
Weather
##### Optional
Music Player # I prefer mine since I got a lot of false positives from play and pause

#### AcidFlow
Timers - En

### TSchmidty
TV Controls
Music Player - If not using the official Snips
Thermostat

Download your assistant and unzip to /usr/share/snips (default location)

### Configure Home Assistant

Create two automations like this

```yaml
- alias: jarvis_hotword_toggle
  trigger:
    platform: mqtt
    topic: hermes/hotword/#
  action:
    event: JARVIS_MQTT
    event_data_template:
      topic: '{{ trigger.topic }}'
      payload: '{{ trigger.payload }}'

- alias: jarvis_intent
  trigger:
    platform: mqtt
    topic: hermes/intent/#
  action:
    event: JARVIS_MQTT
    event_data_template:
      topic: '{{ trigger.topic }}'
      payload: '{{ trigger.payload }}'
```

### Running and Troubleshooting

Start appdaemon

Watch logs, if on raspbian and using the default it will output to syslog, can be read with journalctl
