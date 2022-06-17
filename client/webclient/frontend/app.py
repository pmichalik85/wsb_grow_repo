import datetime
import json
import sys
from threading import Lock

from flask import Flask, render_template, session, request

from flask_socketio import SocketIO, emit
import requests
from flask_wtf import Form
from wtforms import SubmitField, HiddenField, StringField, IntegerField, DecimalField, RadioField
from google.protobuf.json_format import MessageToDict, MessageToJson
# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
from rpc_client.rpc_client import GrowRpcClient
#
# from flask_wtf.csrf import CSRFProtect

import logging
logging.basicConfig(level=logging.DEBUG)


async_mode = None

app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
rpc_client = GrowRpcClient()
app.config['SECRET_KEY'] = 'fiut'
url = 'https://api.coinbase.com/v2/prices/btc-usd/spot'

class LedSettingsForm(Form):
    led = RadioField(
        'LED settings:',
        choices=[('AUTO', 'AUTO'), ('ON', 'ON'), ('OFF', 'OFF')], default='AUTO'
    )


def get_response_data(sensor_data, buffer):
    for e in sensor_data:
        for item in MessageToDict(e)['state']['data']:
            buffer[item['key']] = item['value']

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(1)
        count += 1
        system_monitor_data = rpc_client.read_system_monitor()
        tsl2591_data = rpc_client.read_tsl2591()
        dht22_data = rpc_client.read_dht22()
        soil_moisture_senosr_data = rpc_client.soil_moisture_sensor()
        buffer = dict()
        for sensor_data in [system_monitor_data, tsl2591_data, dht22_data, soil_moisture_senosr_data]:
            get_response_data(sensor_data, buffer)
        socketio.emit('my_response',
                      {'data': buffer, 'count': count})

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        led_form = request.form
        led_state=request.get_json()
        logging.debug(led_state['led'])
        if led_state['led']=="ON":
            resp=rpc_client.led_on()
            for e in resp:
                logging.debug("{}".format(e))
        elif led_state['led']=="OFF":
            resp=rpc_client.led_off()
            for e in resp:
                logging.debug("{}".format(e))
        elif led_state['led']=="AUTO":
            resp = rpc_client.led_auto()
            for e in resp:
                logging.debug("{}".format(e))
        return render_template('index.html', led_form=led_form, led_state=led_state)

    if request.method == "GET":
        led_form=request.form
        return render_template('index.html', led_form=led_form)



@socketio.event
def my_event(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})

# Receive the test request from client and send back a test response
@socketio.on('test_message')
def handle_message(data):
    print('received message: ' + str(data))
    emit('test_response', {'data': rpc_client.read_system_monitor()})

# Broadcast a message to all clients
@socketio.on('broadcast_message')
def handle_broadcast(data):
    print('received: ' + str(data))
    emit('broadcast_response', {'data': rpc_client.read_system_monitor()}, broadcast=True)

@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})

if __name__ == '__main__':
    socketio.run(app, debug=True)
# from google.protobuf.json_format import MessageToJson
#
# # set async_mode to 'threading', 'eventlet', 'gevent' or 'gevent_uwsgi' to
# # force a mode else, the best mode is selected automatically from what's
# # installed
# async_mode = None
#
# from flask import Flask, render_template
# import socketio
#
# sio = socketio.Server(logger=True, async_mode=async_mode)
# app = Flask(__name__)
# app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)
# app.config['SECRET_KEY'] = 'secret!'
# thread = None
#
# import rpc_client.rpc_client as rpc_client
# rpc_client = rpc_client.GrowRpcClient()
#
# def background_thread():
#
#     """Example of how to send server generated events to clients."""
#     count = 0
#     while True:
#         system_monitor_request = rpc_client.mock_request()
#         socketio.sleep(3)
#         count += 1
#         for msg in rpc_client.send(iter([system_monitor_request])):
#             socketio.emit('system_monitor',
#                       {'data': MessageToJson(msg)})
#
# @app.route('/')
# def index():
#     global thread
#     if thread is None:
#         thread = sio.start_background_task(background_thread)
#     return render_template('base.html')
#
#
# @sio.event
# def my_event(sid, message):
#     sio.emit('system_monitor', {'data': message['data']}, room=sid)
#
#
# @sio.event
# def my_broadcast_event(sid, message):
#     sio.emit('system_monitor', {'data': message['data']})
#
#
# @sio.event
# def join(sid, message):
#     sio.enter_room(sid, message['room'])
#     sio.emit('system_monitor', {'data': 'Entered room: ' + message['room']},
#              room=sid)
#
#
# @sio.event
# def leave(sid, message):
#     sio.leave_room(sid, message['room'])
#     sio.emit('system_monitor', {'data': 'Left room: ' + message['room']},
#              room=sid)
#
#
# @sio.event
# def close_room(sid, message):
#     sio.emit('system_monitor',
#              {'data': 'Room ' + message['room'] + ' is closing.'},
#              room=message['room'])
#     sio.close_room(message['room'])
#
#
# @sio.event
# def my_room_event(sid, message):
#     sio.emit('system_monitor', {'data': message['data']}, room=message['room'])
#
#
# @sio.event
# def disconnect_request(sid):
#     sio.disconnect(sid)
#
#
# @sio.event
# def connect(sid, environ):
#     sio.emit('system_monitor', {'data': 'Connected', 'count': 0}, room=sid)
#
#
# @sio.event
# def disconnect(sid):
#     print('Client disconnected')
#
#
# if __name__ == '__main__':
#     if sio.async_mode == 'threading':
#         # deploy with Werkzeug
#         app.run(threaded=True)
#     elif sio.async_mode == 'eventlet':
#         # deploy with eventlet
#         import eventlet
#         import eventlet.wsgi
#         eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
#     elif sio.async_mode == 'gevent':
#         # deploy with gevent
#         from gevent import pywsgi
#         try:
#             from geventwebsocket.handler import WebSocketHandler
#             websocket = True
#         except ImportError:
#             websocket = False
#         if websocket:
#             pywsgi.WSGIServer(('', 5000), app,
#                               handler_class=WebSocketHandler).serve_forever()
#         else:
#             pywsgi.WSGIServer(('', 5000), app).serve_forever()
#     elif sio.async_mode == 'gevent_uwsgi':
#         print('Start the application through the uwsgi server. Example:')
#         print('uwsgi --http :5000 --gevent 1000 --http-websockets --master '
#               '--wsgi-file app.py --callable app')
#     else:
#         print('Unknown async_mode: ' + sio.async_mode)



