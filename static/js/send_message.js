document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    socket.on('connect', () => {
        // Each button should emit a "submit vote" event
        document.querySelector('button').onclick = ()=>{
            const room = document.getElementById("special").innerHTML;
            const message = document.getElementById("message_text").value;
            document.getElementById("message_text").value = "";
            socket.emit('send message', {message : message , room : room}) 
        };

    });
    // socket.emit('submit vote', {'selection': selection});
    // When a new vote is announced, add to the unordered list
    socket.on('tell message', data => {
        const li = document.createElement('li');
        li.innerHTML = `${data.user}:- ${data.message}`;
        document.querySelector('#text_chat').append(li);
    });


});