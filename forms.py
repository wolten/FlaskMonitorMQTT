# -*- coding: utf-8 -*-
from wtforms import Form
from wtforms import StringField, TextField
from wtforms import PasswordField

from wtforms import validators

class FormLogin(Form):
    username = StringField('Usuario', [
        validators.length(
            min=4, max=10, message='Ingresa un usuario valido!.'),
        validators.Required(message='Este campo es requerido')
    ])
    password = PasswordField('Escribe tu password', [
        validators.Required(message='Este campo es requerido')
    ])


class ConfigForm(Form):
    numeroSerie = StringField('Numero de serie', [validators.Required(message='Numero de serie es requerido')])
    MQTTBroker = StringField('URL Broker', [validators.Required(message='URL Broker es requerido')])
    MQTTPort   = StringField('Puerto MQTT', [validators.Required(message='Puerto requerido')])
    MQTTUser   = StringField('Usuario MQTT', [validators.Required(message='Puerto requerido')])
    MQTTPass   = StringField('Password MQTT', [validators.Required(message='Puerto requerido')])

