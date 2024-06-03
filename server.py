from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

users = []
lobbies = {}
boards = {} # {"1": "([][], [][])"}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/functions.js')
def functions():
    return render_template('functions.js')

@app.route('/game-settings')
def game_settings():
    username = request.args.get('username')
    room = request.args.get('room')
    return render_template('game-settings.html', username=username, room=room)

@app.route('/waiting-room')
def waiting_room():
    username = request.args.get('username')
    room = request.args.get('room')
    size = request.args.get('size')
    return render_template('waiting-room.html', username=username, room=room, size=size)

@app.route('/lobby-list')
def lobby_list():
    print(users)
    username = request.args.get('username')
    return render_template('lobby-list.html', username=username)

@app.route('/game')
def game():
    username = request.args.get('username')
    room = request.args.get('room')
    size = request.args.get('size')
    return render_template('game.html', username=username, room=room, size=size)


@socketio.on('create_user')
def create_user(data):
    username = data['username']
    users.append(username)
    print(users)


@socketio.on('checkUsername')
def give_users(username):
    print("username"+username);
    if username in users:
        emit('checkUsername', True)
    else:
        emit('checkUsername', False)


@socketio.on('create')
def on_create(data):
    username = data['username']
    room = data['room']
    lobbies[room] = {'host': username, 'players': [username]} #useless
    join_room(room)

@socketio.on('selectBoardSize')
def on_select_board_size(data):
    room = data['room']
    size = data['size']
    if room in lobbies:
        board = create_board(size)
        lobbies[room]['size'] = size #nwm po co to
        boards[room]=(board, board)
        print(boards[room][0])
        emit('waitingForPlayer', room=room)


def create_board(size):
    return [['O' for _ in range(int(size))] for _ in range(int(size))]


@socketio.on('giveBoard')
def on_give_board(room):
    print(boards[room][0])
    emit('giveBoard', boards[room][0])


@socketio.on('waitForPlayer')
def on_wait_for_player(data):
    username = data['username']
    room = data['room']
    join_room(room)
    if len(lobbies[room]['players']) == 2:
        size = lobbies[room]['size']
        emit('startGame', {'size': size}, room=room)


@socketio.on('getLobbies')
def on_get_lobbies():
    available_lobbies = [room for room in lobbies if len(lobbies[room]['players']) == 1 and lobbies[room]['size']]
    emit('lobbies', available_lobbies)

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    if room in lobbies and len(lobbies[room]['players']) == 1:
        lobbies[room]['players'].append(username)
        join_room(room)
        size = lobbies[room]['size']
        emit('startGame', {'size': size}, room=room)

@socketio.on('disconnect')
def on_disconnect():
    for room in lobbies:
        if request.sid in lobbies[room]['players']:
            lobbies[room]['players'].remove(request.sid)
            if not lobbies[room]['players']:
                del lobbies[room]
            else:
                emit('message', {'msg': 'A player has disconnected.'}, room=room)
            break




@socketio.on('shoot')
def on_shoot(data):
    room = data['room']

    x = (data['x'])
    y = (data['y'])
    print(x)
    print(y)
    boards[room][x][y]='1';
    print(boards[room]);


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8002, debug=True)



