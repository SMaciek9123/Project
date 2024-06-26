async function isLogged(){
  if(document.cookie == "")
  {
      return false;
  }
  var result = await compareCookie();
  if(result == true)
  {
      console.log("zalogowano jako "+getCookie('username'));
      //alert("zalogowano jako "+getCookie('username'));
      return true;
  }
  else
  {
      console.log("zaloguj się");
      return false;
  }
}

function setCookie(cname, cvalue, exdays) {
const d = new Date();
d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
let expires = "expires="+d.toUTCString();
document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
let name = cname + "=";
let ca = document.cookie.split(';');
for(let i = 0; i < ca.length; i++) {
  let c = ca[i];
  while (c.charAt(0) == ' ') {
    c = c.substring(1);
  }
  if (c.indexOf(name) == 0) {
    return c.substring(name.length, c.length);
  }
}
return "";
}

async function compareCookie() {
  var socket = io();
  username=getCookie('username');
  var result = await asyncEmit('checkUsername', username);
  return result;
}

async function asyncEmit(eventName, data) {
var socket = io();
return new Promise(function (resolve, reject) {
  socket.emit(eventName, data);
  socket.on(eventName, result => {
    socket.off(eventName);
    resolve(result);
  });
  setTimeout(reject, 1000);
});
}

async function getBoard(room,username){
  var board = await asyncEmit('giveBoard', {'room': room, 'username': username}); //dodać który board ma zwrócic (room, player)
  console.log("tablica dla: "+username+" wynik "+board);
  logBoard(board);
  return board;
}

function logBoard(board){
    let breaker = Math.sqrt(board.length);
    for(let i=0; i<board.length; i++)
    {
        //console.log(board[i]);
        if(i==breaker)
        {
            breaker+=breaker;
         //   console.log('\n');
        }
    }
}

async function getData(room,username){
  var data = await asyncEmit('giveData', {'room': room,'username': username});
  console.log("getData wynik: "+data);
  return data;
}
async function getShips(room,username){
  var data = await asyncEmit('giveShips', {'room': room,'username': username});
  console.log("getShips wynik: "+data);
  return data;
}

async function getEnemyName(room,username){
  var enemyName = await asyncEmit('giveEnemyName', {'room': room,'username': username});
  return enemyName;
}

async function getEnemyBoard(room,username){
  var board = await asyncEmit('giveEnemyBoard', {'room':room, 'username':username}); //dodać który board ma zwrócic (room, player)
  console.log("tablica dla: "+username+" wynik ");
  logBoard(board);
  return board;
}

function exitGame(room,username) {
  if (confirm("Czy na pewno chcesz wyjść? "+username )) {
      // Tu możesz dodać kod do zamknięcia gry lub przekierowania do innej strony
      var enemy = getEnemyName(room,username)
      socket.emit('leave',{'room': room,'username': username})
      socket.emit('abandonGame',{'room': room,'username': enemy})
      window.location.href = "/"; // Przykład przekierowania do strony głównej
  }
}
function abandonGame(room,username) {
  if (confirm("Czy na pewno chcesz wyjść?")) {
      socket.emit('abandonGame', {username: username, room: room});
      alert('Opuszczasz grę');
      
  }
}


