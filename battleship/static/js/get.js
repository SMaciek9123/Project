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
            console.log(board[i]);
            if(i==breaker)
            {
                breaker+=breaker;
                console.log('\n');
            }
        }
    }
    
    async function getData(room,username){
      var data = await asyncEmit('giveData', {'room': room,'username': username});
      console.log("getData wynik: "+data);
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