function isLogged(){
    var jprdl = compareCookie();
    alert(jprdl);
    if(jprdl == true)
    {
        alert("zalogowano jako "+getCookie('username'));
        return true;
    }
    else
    {
        //window.location.href = '/';
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

function compareCookie() {
    var socket = io();
    username=getCookie('username');
    socket.emit('getUsers');
    var result =
    socket.on("giveUsers", async function(users, callback) { //nie działam
    if(users.includes(username))
        {
            alert('zawiera');
            return true;
        }
    else
        {
           alert('nie zawiera');
           return false;
        }
    });
    alert(result);
    return result;
}

/* PROPOZYCJA CZATU
async function checkUserInList(username) {
    return new Promise((resolve, reject) => {
        socket.emit('getUsers', null, function(users) {
            if (users.includes(username)) {
                resolve(true);
            } else {
                resolve(false);
            }
        });
    });
}