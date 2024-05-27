from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('message', {'msg': f'{username} has entered the room.'}, room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit('message', {'msg': f'{username} has left the room.'}, room=room)

@socketio.on('send_message')
def handle_send_message_event(data):
    room = data['room']
    emit('message', {'msg': data['msg'], 'username': data['username']}, room=room)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000, debug=True)
