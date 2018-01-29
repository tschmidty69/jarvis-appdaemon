import appdaemon.plugins.hass.hassapi as hass
import ast
import sys
import random
import string
import json
import yaml
import requests
from pathlib import Path
import os, re, time
from fuzzywuzzy import fuzz, process

#########################
# Jarvis thermostat Skill
#########################

class jarvis_thermostat(hass.Hass):

    def initialize(self):
        if not self.args.get('enabled'):
            return
        self.jarvis = self.get_app('jarvis_core')
        self.jarvis.jarvis_register_intent('set_thermostat',
                                      self.jarvis_set_thermostat)

    def jarvis_set_thermostat(self, data, *args, **kwargs):
        self.log("__function__: {}".format(data), "INFO")
        if data.get('payload'):
            data = json.loads(data.get('payload', data))
        #self.log("jarvis_thermostat: intent {}".format(data['intent']), "INFO")
        #self.log("jarvis_thermostat: slots {}".format(data['slots']), "INFO")

        if not data.get('slots'):
            self.log("jarvis_thermostat: no slot information")
            return

        slots = {}
        for slot in data['slots']:
            slots[slot['slotName']] = slot['value']['value']

        self.log("jarvis_thermostat: {}".format(slots), "INFO")
        if slots.get('zone') == 'upstairs':
            thermostat = 'upstairs'
        else:
            thermostat = 'downstairs'

        if not slots.get('temperature') and not slots.get('direction'):
            self.jarvis_notify(None, {'siteId': data.get('siteId', 'default'),
                                 'text': self.jarvis_speech('sorry')
                                 + ", I can only do heat or ac"})
            return
        if slots.get('direction'):
            if slots.get('temperature'):
                if not 1 <= int(slots['temperature']) < 10:
                    self.jarvis_notify(None,
                                {'siteId': data.get('siteId', 'default'),
                                 'text': self.jarvis_speech('sorry')
                                 + str(slots['temperature'])
                                 + ' degrees is too big of a change for me.'})
                    return
                else:
                    temperature = int(slots['temperature'])
            elif slots.get('direction') == 'up':
                temperature = 2
            else:
                temperature = -2
            cur_temp = self.get_state(
                entity='climate.'+self.thermostats['heat'][thermostat],
                attribute='current_temperature')
            target_temp = int(cur_temp) + int(temperature)
        elif slots.get('temperature'):
            if not 60 <= int(slots['temperature']) < 91:
                self.jarvis_notify(None, {'siteId': data.get('siteId', 'default'),
                                     'text': self.jarvis_speech('sorry')
                                     + "I cant set the temperature"
                                     + 'to ' + slots['temperature']
                                     + ' degrees.'})
                return
            else:
                target_temp = int(slots['temperature'])
        if target_temp:
            self.log("jarvis_thermostat: target_temp {}".format(target_temp),
                     "INFO")
            if slots.get('mode') == 'cool':
                mode = 'cool'
            else:
                mode = 'heat'
            self.call_service('climate/set_temperature',
                              entity_id='climate.'
                                        + self.thermostats[mode][thermostat],
                              temperature=target_temp)
            self.jarvis_notify(None, {'siteId': data.get('siteId', 'default'),
                                      'text': self.jarvis_speech('ok')
                                      + ", setting the "
                                      + thermostat + ' '
                                      + mode + ' to ' + str(target_temp)
                                      + ' degrees'})
        else:
            self.jarvis_notify(None, {'siteId': data.get('siteId', 'default'),
                                      + 'text':"Sorry, I didnt understand"})
