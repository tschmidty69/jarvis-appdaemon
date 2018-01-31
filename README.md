# Jarvis 
##  An Appdaemon App for use with the Snips Voice Assistant and HomeAssistant

Control your home using Snips <https://github.com/snipsco/snips-platform-documentation/wiki>, 
a Voice Assistant that runs entirely locally, your audio and data is handled 100% on your system to protect 
your privacy.

This app is intended to be deployed on Appdaemon version 3 <http://appdaemon.readthedocs.io/en/latest/index.html>

It is mainly intended for use with Home Assistant at this point, but plans are to have a standalone mode and 
*maybe* write an OpenHab plugin.

#### What is this really?
Snips listens to you and creates intents (you've seen the commercials for that thing from some online book store).

The idea is that you can write some python code that registers intents and code to handle those intents. Right now
they are fairly basic and just handle turning on lights, playing music or TV shows, setting the thermostat, etc.
But Snips has built a good framework to making a more fully featured Voice Assistant so why not?

For instance I already have interactions like this in my assistant:
- Hey Snips, turn the heat up downstairs
- Snips: OK, turning the downstairs heat up

This is initiated from Home Assistant noticing the garage door has been open for over 15 minutes
- Snips: The garage door is still open, would you like me to close it?
- Me: Yes, please (you have to be polite for when the robots take over)
- Snips: OK, closing the garage door

#### Multi Language and Multi Assistant Support
One of my big motiviatons is to provide Multi Language and Multi Assistant support from the start so you can 
choose or edit a speech file and have appropriate responses and have an assistant that matches your character. 

Look at jarvis/data/jarvis_en.yaml for a basic idea of what I am going for.

Snips themselves are working on expanding their language support, and I will try to keep up with that. If their
snipsmanager and snips skills get to a mature/stable state I'd love to incorporate them as well to avoid duplication
of effort and increase the capabilities.

## This is 100% a Work in Progress and not complete or even close at this point
It works for me, and I feel like it is a good framework.

Feel free to file an issue though if you have a suggestion or request.

The intention is for you to *mostly* just have to configure the jarvis.yaml with your settings and it 
should work.

### Installation

- Install Home Assistiant
- Install Snips
- Install Appdaemon V3
- Install this app in your apps folder (git clone the repo)
- Configure it

### Updating

After using git to clone this repository into your appdaemon apps directory, simply cd to the directory and git pull

Use care that you don't overrun any local changes and you may need to manually change config file settings. I will try
to call out those situations in the CHANGELOG.md

### Configuration

Edit the jarvis/jarvis.yaml and enable modules and add settings

###  Configuring Snips

I have a lot of slots and words included in my intents, but if you want to work with generic queries
best results will be with the snips 500MB asr (bottom of page 6 on their docs) which is only available
in English at this point.

Create your assistant and add these bundles

#### Snips
- Smart Lights
- Weather
- *Music Player* (I prefer mine since I got a lot of false positives from play and pause)

#### AcidFlow
- Timers - En

#### TSchmidty
- TV Controls
- Music Player (If not using the official Snips Bundle)
- Thermostat

For my music bundle, I generated a large list of Artists for the slots to help with artist matching, which
is working well for me.

Create your assistant, download it, and unzip to /usr/share/snips (default location)

### Configure Home Assistant

The general idea is to fire the hotword topic to enable lowering media player volume (if configured)
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

