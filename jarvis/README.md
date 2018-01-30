# Jarvis 
##  An Appdaemon App for use with the Snips Voice Assistant and HomeAssistant

Control your home using Snips <https://github.com/snipsco/snips-platform-documentation/wiki>, 
a Voice Assistant that runs entirely locally.

This app is intended to be deployed on Appdaemon version 3 <http://appdaemon.readthedocs.io/en/latest/index.html>

It is mainly intended for use with Home Assistant at this point, but plans are to have a standalone mode and 
*maybe* write an OpenHab plugin.

#### Multi Language and Multi Assistant Support
One of my big motiviatons is to provide Multi Language and Multi Assistant support from the start so you can 
choose or edit a speech file and have appropriate responses and have an assistant that matches your character. 

Snips themselves are working on expanding their language support, and I will try to keep up with that. If their
snipsmanager and snips skills get to a mature/stable state I'd love to incorporate them as well to avoid duplication
of effort and increase the capabilities.

## This is 100% a Work in Progress and not complete or even close at this point
It works for me, and I feel like it is a good framework.

Feel free to file an issue though if you have a suggestion or request.

The intention is for you to *mostly* just have to configure the jarvis.yaml with your settings and it 
should work.

### Installation

- Install Snips
- Install Appdaemon V3
- Install this app in your apps folder (git clone the repo)
- Configure it

### Configuration

Edit the jarvis/jarvis.yaml and enable modules and add settings

###  Configuring Snips

I have a lot of slots and words included in my intents, but if you want to work with generic queries
best results will be with the snips 500MB asr (bottom of page 6 on their docs) which is only available
in English at this point.

Create your assistant and add these bundles

#### Snips
Smart Lights
Weather
*Music Player* (I prefer mine since I got a lot of false positives from play and pause)

#### AcidFlow
Timers - En

#### TSchmidty
TV Controls
Music Player (If not using the official Snips Bundle)
Thermostat

For my music bundle, I generated a large list of Artists for the slots to help with artist matching, which
is working well for me.

Create your assistant, download it, and unzip to /usr/share/snips (default location)

### Configure Home Assistant

The general idea is to fire the hotword topic to enabled lowering media player volume (if configured)
and all intents to appdaemon to handle.

This does not preclude having additional intents handled directly by Home Assistant and you can disable
any modules as needed from the config file.

Create two automations like this

```yaml
automations:
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
