document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    socket.on('connect', () => {
        // Each button should emit a "submit vote" event
        document.querySelector('button').onclick = ()=>{
            const room = document.getElementById("name").value;
            socket.emit('create room', {room : room});
            document.getElementById("name").value = "";
        };

    });
    // socket.emit('submit vote', {'selection': selection});
    // When a new vote is announced, add to the unordered list
    socket.on('add room', data => {
        const p = document.getElementById('error_message');
        if(data.condition == false){
            p.innerHTML = "room name must be unique";
        }
        else{
            p.innerHTML = "room made successfully";
        }

    });
});