async function isLogged(){
  if(document.cookie == "")
  {
      return false;
  }
  var result = await compareCookie();
  if(result == true)
  {
      alert("zalogowano jako "+getCookie('username'));
      return true;
  }
  else
  {
      alert("zaloguj się");
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

async function getBoard(room,username){
  var board = await asyncEmit('giveBoard', {'room': room, 'username': username}); //dodać który board ma zwrócic (room, player)
  console.log("tablica dla: "+username+" wynik "+board);
  return board;
}

async function getData(room,username){
  var data = await asyncEmit('giveData', {'room': room,'username': username}); //dodać który board ma zwrócic (room, player)
  alert("getData alert: "+data);
  return data;
}