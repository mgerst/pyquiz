var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
    socket.emit('board.current');
});

socket.on('board.current', function(data) {
    console.log(data);
});