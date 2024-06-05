
async function isLogged(){
  if(document.cookie == "")
  {
      return false;
  }
  var result = await compareCookie();
  if(result == true)
  {
      console.log("zalogowano jako "+getCookie('username'));
      alert("zalogowano jako "+getCookie('username'));
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