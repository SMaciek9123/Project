function isLogged(){
            socket.emit('getUsers');
            socket.on("giveUsers", (users) => {
            alert(users);
            if(users.includes(document.cookie)) //zrobić oddzielenie ciasteczek document.cookie="username=nicktwój"
            {
                alert("działa, zrób teraz funkcje!(i dodaj zaprzeczenie: !users.includes(document.cookie))");
            }
            });

            if(document.cookie==""){
            window.location.href = '/';
            }
            }