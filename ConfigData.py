# -*- coding: utf-8 -*-
__author__ = 'woltenX'


class ConfigData:

    def __init__(self, noserie, mqttbroker, mqttport, mqttusuario, mqttpass):
        self.noserie    = noserie
        self.mqttbroker = mqttbroker
        self.mqttport = mqttport
        self.mqttusuario = mqttusuario
        self.mqttpass = mqttpass

    def toDBCollection(self):
        return {
            "numeroserie": self.noserie,
            "mqttbroker": self.mqttboroker,
            "mqttport": self.mqttport,
            "mqttusuario": self.mqttusuario,
            "mqttpass":self.mqttpass
        }

    def __str__(self):
        return "noserie: %s - mqttbroker: %s - mqttport: %s - mqttusuario: %s - mqttpass: %" \
               % (self.noserie, self.mqttbroker, self.mqttport, self.mqttusuario, self.mqttpass)
