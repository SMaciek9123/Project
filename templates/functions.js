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
  //alert(username);
  //socket.emit('getUsers');
  var result = await asyncEmit('checkUsername', username);
  //alert(result);
  return result;
}

async function asyncEmit(eventName, data) {
var socket = io();
return new Promise(function (resolve, reject) {
  //alert("dzialam");
  //alert(eventName);
  socket.emit(eventName, data);
  socket.on(eventName, result => {
    socket.off(eventName);
    resolve(result);
  });
  setTimeout(reject, 1000);
});
}

async function getBoard(room){
  var board = await asyncEmit('giveBoard', room); //dodać który board ma zwrócic (room, player)
  console.log("getBoard alert: "+board);
  return board;
}

async function getData(room,username){
  var data = await asyncEmit('giveData', {'room': room,'username': username}); //dodać który board ma zwrócic (room, player)
  console.log("getData alert: "+data);
  return data;
}

async function shoot_game(){
  var data = await asyncEmit('getData',room); //update data
  if(game_not_over) // jezeli gra dalej jest
    {
        if(player_turn=id_player)// jezeli gracz ma swoja ture
          {
            var new_data = await asyncEmit('shoot',room);
          }
          else//jak nie to poczekaj na nia
          {
            wait_for_turn();
          }
    }
}
