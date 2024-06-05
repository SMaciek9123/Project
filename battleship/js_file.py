from battleship import app
from flask import Flask, render_template, request, send_from_directory
from flask_socketio import SocketIO, join_room, leave_room, emit

@app.route('/functions')
def functions():
    return send_from_directory('static/js', 'functions.js')

@app.route('/cookies')
def cookies():
    return send_from_directory('static/js', 'cookies.js')

@app.route('/geter')
def geter():
    return send_from_directory('static/js', 'get.js')
