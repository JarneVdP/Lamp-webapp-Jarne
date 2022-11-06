from configparser import ConfigParser
from flask import render_template, request
from flask_socketio import SocketIO
import flask_login
import asyncio
from . import main
from .coapclient import *
from ..templates import *
from ..application import SOCKETIO, login_manager

@main.route('/lamps') 
@flask_login.login_required
def indexlamp():
    return render_template("lamps.html")


# cd Downloads sudo openvpn JarneVanderPlas.ovpn
# cd ../Desktop/GevorderdeWebappl/flask-webapp-Jarne python webapp.py
# source env/bin/activate

# test zodat de lampen aan gaan of niet aan gaan - check
# agendasysteem -> toegan op agenda met databases, accounts, etc.
# lampen -> toegang op lampen met slider, etc.\  - check
# via javascript en sliders de waardebn aanpassen en doorsturen naar de coapclient. using jquery ajax() function - check
# flask -login, -bcrypt: Hash and salt passwords - check
# sqlite database voor login via sqlAlchemy  - check
# flask-SocketIO() voor realtime communicatie tussen client en server
# niet toestaan dat mensen via postman get/set sturen zonder ingelogd te zijn dus server side blockeren. flask login extra decorator = login_manager.session_protection, geimplementeerd in authentication/app.py maar nog niet getest


# List with lamp names
lamps = ['lamp1a', 'lamp1b', 'lamp1c', 'lamp2a', 'lamp2b', 'lamp2c', 'lamp3a', 'lamp3b',
         'lamp3c', 'lamp4a', 'lamp4b', 'lamp4c', 'lamp5a', 'lamp5b', 'lamp5c', 'lamp6a']

@SOCKETIO.on('connect')
def socketioconnected():
    print("Socketio session connected.", request.sid)


@SOCKETIO.on('disconnect')
def socketiodisconnected():
    print("Socketio disconnected.")

@main.route('/api/<lamp>', methods=['GET', 'POST', 'PUT'])
def lampstatusrequest(lamp):
    if lamp not in lamps:
        return ({'Error': ' Lamp not found'}, 404)
    if request.method == 'GET':
        val = asyncio.run(coapgetlampstatus('coap://' + lamp + '.irst.be/lamp/dimming'))
        return {'lampvalue': str(val)}
    if request.method == 'POST' or request.method == 'PUT':
        if 'dimming' in request.form:
            value = request.form['dimming']
        else:
            return ({'Error': ' diming is not defined'}, 404)
        # input value parsing
        if int(value) > 100:
            value = 100
        elif int(value) < 0:
            value = 0

        asyncio.run(coapsetlampstatus('coap://' + lamp + '.irst.be/lamp/dimming', bytes(str(value), 'utf-8')))
        val = asyncio.run(coapgetlampstatus('coap://' + lamp + '.irst.be/lamp/dimming'))
        SOCKETIO.emit('ReceiveFromLampServer', val)
        return {'lampvalue': str(val)}
    return ({'Error': ' not supported'}, 405)


# Run the app
# if __name__ == "__main__":
#     SOCKETIO.run(APP, host='localhost', port=8080, debug=True, use_reloader=False)
