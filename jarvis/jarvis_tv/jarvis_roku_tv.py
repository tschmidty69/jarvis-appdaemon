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

######################
# Jarvis Roku TV Skill
######################

class jarvis_roku_tv(hass.Hass):

    def initialize(self):
        if not self.args.get('enabled'):
            return
        self.jarvis = self.get_app("jarvis_core")
        self.jarvis.jarvis_register_intent('playTv',
                                      self.jarvis_play_tv)
        self.jarvis.jarvis_register_intent('pauseTv',
                                      self.jarvis_pause_tv)
        self.jarvis.jarvis_register_intent('pressPlayTv',
                                      self.jarvis_press_play_tv)
        self.jarvis.jarvis_register_intent('playSelectTv',
                                      self.jarvis_press_select_tv)
        self.jarvis.jarvis_register_intent('turnOnTv',
                                      self.jarvis_turn_on_tv)
        self.jarvis.jarvis_register_intent('turnOffTv',
                                      self.jarvis_turn_off_tv)

    def jarvis_play_tv(self, data, *args, **kwargs):
        self.log("__function__: {}".format(data), "INFO")
        if data.get('payload'):
            data = json.loads(data.get('payload', data))
        zone = data.get('zone', 'living_room')
        channel = '12' # Netflix
        if data.get('channel'):
            if data['channel'] == 'amazon':
                channel = '13'

        if data.get('slots'):
            #self.log("jarvis_tv: {}".format(data.get('slots')), "INFO")
            for slot in data['slots']:
                #self.log("jarvis_tv: {}".format(slot), "INFO")
                if slot.get('slotName') == 'show':
                    #self.log("jarvis_tv: {}".format(self.netflix.keys()),
                    #         "INFO")
                    show = process.extractBests(slot['value']['value'],
                        list(self.tv.keys()), score_cutoff=60)
                    self.log("jarvis_tv: shows {}".format(show), "INFO")
                    self.log("jarvis_tv: best_match {}".format(
                        self.tv[show[0][0]]), "INFO")

                    url = ("http://"
                          + str(self.roku[zone])
                          + ":8060/launch/"
                          + str(self.tv[show[0][0]]['channel'])
                          + "?ContentID="
                          + str(self.tv[show[0][0]]['seasons'][1])
                          + "&MediaType=series")
                    self.log("jarvis_tv: url {}".format(url), "INFO")

                    response = requests.post(url)
                    self.log("jarvis_tv: response {}".format(response), "INFO")
                    if str(self.tv[show[0][0]]['channel']) == '13':
                        time.sleep(3)
                        url = ("http://"
                               + str(self.roku[zone])
                               + ":8060/keypress/Select")
                        response = requests.post(url)
                        self.log("jarvis_tv: response {}".format(response), "INFO")
                        self.jarvis_notify(None, {'siteId':
                            data.get('siteId', 'default'),
                            'text': self.jarvis_speech('ok')
                            + ", I put " + self.tv[show[0][0]]['long_title']
                            + " on for you"})

    def jarvis_pause_tv(self, data, *args, **kwargs):
        self.log("__function__: {}".format(data), "INFO")

    def jarvis_press_play_tv(self, data, *args, **kwargs):
        self.log("__function__: {}".format(data), "INFO")

    def jarvis_press_select_tv(self, data, *args, **kwargs):
        self.log("__function__: {}".format(data), "INFO")

    def jarvis_turn_on_tv(self, data, *args, **kwargs):
        self.log("__function__: {}".format(data), "INFO")

    def jarvis_turn_off_tv(self, data, *args, **kwargs):
        self.log("__function__: {}".format(data), "INFO")
