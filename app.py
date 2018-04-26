#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import request
from flask_wtf import CSRFProtect
from flask import make_response
from flask import session
from flask import url_for
from flask import redirect
from flask import flash
from flask import g
from pymongo import MongoClient
import json
from bson import json_util
from bson.objectid import ObjectId

#MODELS
from ConfigData import ConfigData

import forms

# PASO 1: Conexion al Server de MongoDB Pasandole el host y el puerto
mongoClient = MongoClient('mongodb://localhost:27017')
# PASO 2: Conexion a la base de datos
db = mongoClient.DataSensors
# PASO 3: Obtenemos una coleccion para trabajar con ella
collection       = db.Lecturas
collectionUsers  = db.Usuarios
collectionConfig = db.Configuracion

app = Flask(__name__)

#Protegiendo del CSRF
app.secret_key = 'bypass'
csrf = CSRFProtect(app)


def toJson(data):
	"""Convert Mongo object(s) to JSON"""
	return json.dumps(data, default=json_util.default)

#MANEJADOR DE ERRORES
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


#INDEX PRINCIPAL
@app.route('/')
def index():
	if 'userID' in session:
		login=1
	else:
		login=0
	return render_template('index.html', sign=login)


#LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
	login_form = forms.FormLogin(request.form)

	#CACHANDO EL POST
	if request.method == 'POST' and login_form.validate():
		#session['username'] = login_form.username.data
		usuario = collectionUsers.find_one(
			{"usuario": login_form.username.data, "password": login_form.password.data})

		if usuario:
			print usuario
			session['userID'] = toJson(usuario['_id'])
			return redirect( '/' )
		else:
			print "Negativo Pariente"


	else:
		print 'Esta peticion no es POST'

	return render_template('login.html', form=login_form)


#LOGOUT
@app.route('/logout')
def logout():
	if 'userID' in session:
		print 'aio bye'
		session.pop('userID')
	return redirect( '/' )




#CONFIGURACION
@app.route('/configuracion', methods=['GET','POST'])
def configuracion():
	config_form = forms.ConfigForm(request.form)
	if request.method == 'POST' and config_form.validate():
		print "Fierro por la 300"
		numeroSerie = config_form.numeroSerie.data
		mqttbroker  = config_form.MQTTBroker.data
		mqttport    = config_form.MQTTPort.data
		mqttusuario = config_form.MQTTUser.data
		mqttpass    = config_form.MQTTPass.data

		cursor = collectionConfig.find_one_and_update({"numeroserie": numeroSerie}, {
		                                        '$set': {"numeroserie": numeroSerie, "mqttbroker": mqttbroker, "mqttport": mqttport, "mqttusuario":mqttusuario, "mqttpass": mqttpass}}, 
												upsert=True)
		if cursor:
			flash("Actualizado con exito")
			print "exito!"

	else:
		print "Peticion GET"


	#VALIDANDO QUE SOLO ENTE CUANDO INICIO SESION EL USUARIO
	if 'userID' in session:
		usuario = session['userID']
		print 'Logueado correctamente'
		data = collectionConfig.find_one({})
		

		return render_template('configuracion.html', form=config_form, data=data)
	else:
		return render_template( url_for('login') )




#PETICION AJAX
@app.route('/data', methods=['GET'])
def ajx_data():
	enQuery = collection.find({})
	mongoClient.close()
	"""
	data = []
	for dato in enQuery:
		data.append(dato)
	dataa = toJson(data)
	flash(dataa)
	"""
	if 'userID' in session:
		login = 1
	else:
		login = 0
	return render_template('boxData.html', data=enQuery, sign=login)


#PETICION AJAX
@app.route('/ajx-delete', methods=['POST'])
def ajx_delete():
	idx = request.form['id']
	print idx
	if 'userID' in session:
		enQuery = collection.find_one({'_id': ObjectId(idx) })
		print enQuery
		if enQuery:
			collection.find_one_and_delete({'_id':  ObjectId(idx)})

		response = {'status': 1}
		mongoClient.close()
		return json.dumps(response)
	else:
		response = {'status': 0}
		return json.dumps(response)
	




#DEPLOY DE APP
if __name__ == '__main__':
	app.run(debug=True, port=7000)
