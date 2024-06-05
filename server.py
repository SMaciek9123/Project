from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, emit
import copy
import random
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

users = []
lobbies = {}
game_data = {}# {'room' => {'user1'=> tura,
              #             'user2' =>,tura}} 
game_ships = {}
win = {}

boards = {} # {'room' => {'user1'=> 'board',
            #             'user2' =>'board2'}} 
ship_type = {
            '10': [4,4,3,2,1,1],
            '7': [4,3,2,2,1],
            '5': [3,2,1,1],
            '3': [2,1],
            }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/functions')
def functions():
    return render_template('functions.js')

@app.route('/ship')
def ship():
    return render_template('put-ships.html')

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

@app.route('/win')
def congratulations():
    return render_template('win.html')

@app.route('/lose')
def sorry():
    return render_template('lose.html')

@socketio.on('create_user')
def create_user(data):
    username = data['username']
    users.append(username)
    print(users)


@socketio.on('checkUsername')
def give_users(username):
    print("username "+username)
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
        host = lobbies[room]['host']
        lobbies[room]['size'] = size #nwm po co to
        win[room]= {host: 0}
        game_data[room]= {host: True}
        ship_temp = copy.deepcopy(ship_type[size])
        game_ships[room]= {host: ship_temp}
        print(game_ships[room][host])
        print("tuuuuuutajjjjjjjj sa statki dla:")
        print(host)
        boards[room]={host: board}
        print(boards[room][host])
        emit('waitingForPlayer', room=room)


def create_board(size):
    board = [[0 for _ in range(int(size))] for _ in range(int(size))]
    return board


@socketio.on('giveBoard')
def on_give_board(data):
    room = data['room']
    username = data['username']
    emit('giveBoard', boards[room][username])

@socketio.on('giveShips')
def on_give_(data):
    room = data['room']
    h =lobbies[room]['host']
    username = data['username']
    print(game_ships[room])
    emit('giveShips', game_ships[room][username])


@socketio.on('giveEnemyBoard')
def give_enemy_board(data):
    room=data['room']
    username=data['username']
    if lobbies[room]['players'][0] == username:
        emit('giveEnemyBoard', boards[room][lobbies[room]['players'][1]])
    elif lobbies[room]['players'][1] == username:
        emit('giveEnemyBoard', boards[room][lobbies[room]['players'][0]])
    else:
        print("Błąd pobrania tablicy przeciwnika");

@socketio.on('giveEnemyName')
def give_enemy_name(data):
    room=data['room']
    username=data['username']
    emit('giveEnemyName', get_enemy_username(room, username))

@socketio.on('giveData')
def on_give_data(data):
    username = data['username']
    room = data['room']
    print("wartosc ") 
    print( game_data[room][username])
    emit('giveData',  game_data[room][username])

@socketio.on('givePlayersTable')
def on_give_players_table(data):
    room = data['room']
    emit('givePlayersTable', lobbies[room]['players'])


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
    available_lobbies = [room for room in lobbies if len(lobbies[room]['players']) == 1]
    emit('lobbies', available_lobbies)

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    if room in lobbies and len(lobbies[room]['players']) == 1:
        lobbies[room]['players'].append(username)
        host = lobbies[room]['host']
        join_room(room)
        size = lobbies[room]['size']
        boards[room][username]= copy.deepcopy(boards[room][host])
        game_ships[room][username] = copy.deepcopy(ship_type[size])
        print(game_ships[room][username])
        game_data[room][username]= False
        win[room][username]= 0
        print("\n")
        print(boards[room])
        print("\n")
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


@socketio.on('clear')
def on_clear(data):
    room = data['room']
    username = data['username']
    size =  len(boards[room][username]) 
    game_ships[room][username]= copy.deepcopy(ship_type[str(size)])
    boards[room][username] = [[0 for _ in range(int(size))] for _ in range(int(size))]

@socketio.on('put_ship')
def on_put_ship(data):
    
    room = data['room']
    username = data['username']
    x = data['x']
    y = data['y'] 
    ship_lenght = data['ship_lenght']  
    ship_high = data['ship_high']
    
    if(room in boards):
        if(username in boards[room]):
            if(ship_lenght>1):
                game_ships[room][username].remove(ship_lenght)
                print("teraz takie ci zostaly")
                print(game_ships[room][username])
                for i in range(ship_lenght):
                        boards[room][username][x+i][y]=2
            else:
                game_ships[room][username].remove(ship_high)
                print("teraz takie ci zostaly")
                print(game_ships[room][username])
                for i in range(ship_high):
                        boards[room][username][x][y+i]=2
        else:
            boards[room][username]=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    else:
        boards[room]={username: [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]}
    print(boards[room][username])

@socketio.on('shoot')
def on_shoot(data):
    room = data['room']
    username = data['username']
    x = (data['x'])
    y = (data['y'])
    players= lobbies[room]['players']
    print(boards[room])
 

    if(game_data[room][username]):
        temp=boards[room][get_enemy_username(room, username)]
        temp[x][y]=temp[x][y]+1
        print(boards[room][username])
        print(temp)
        liczba_trafien = sum(1 for w in temp for e in w if e == 3)
        print("liczba trafien= ")
        print(liczba_trafien)
        if(liczba_trafien==4):
            win[room][players[0]]=-1
            win[room][players[1]]=-1
            win[room][username]=1
            emit('End',{'username': username})
            print("wygrał")
            print(username)
            print(win[room])
        if(win[room][username]==-1):
            emit('lose',{})
        print("wykonano strzal teraz zamiana tur")
        print( game_data[room])
        game_data[room][players[0]], game_data[room][players[1]]=game_data[room][players[1]], game_data[room][players[0]]
        print( game_data[room])
    else:
        print("nie twoja tura")
    emit('shootsFired', {}, broadcast=True)


def get_enemy_username(room, username):
    if lobbies[room]['players'][0] == username:
        return lobbies[room]['players'][1]
    elif lobbies[room]['players'][1] == username:
        return lobbies[room]['players'][0]
    else:
        print("Błąd pobrania nazwy przeciwnika");

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8002, debug=True)
