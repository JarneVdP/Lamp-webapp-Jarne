from flask import render_template, request
from flask_socketio import SocketIO
import flask_login
import asyncio
from . import main
from .coapclient import *
from ..templates import *
from ..application import SOCKETIO, login_manager

#lamps template for displaying all lamps values and the sliders
@main.route('/lamps') 
@flask_login.login_required
def indexlamp():
    return render_template("lamps.html")


# List with lamp names
lamps = ['lamp1a', 'lamp1b', 'lamp1c', 'lamp2a', 'lamp2b', 'lamp2c', 'lamp3a', 'lamp3b',
         'lamp3c', 'lamp4a', 'lamp4b', 'lamp4c', 'lamp5a', 'lamp5b', 'lamp5c', 'lamp6a']

@SOCKETIO.on('connect')
def socketioconnected():
    print("Socketio session connected.", request.sid)


@SOCKETIO.on('disconnect')
def socketiodisconnected():
    print("Socketio disconnected.")

# Socketio event handler for lamp status request
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

