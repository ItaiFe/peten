var net = require('net');

var host = 'localhost';
var port = 8000;

var socket = new net.Socket();

socket.connect(port, host, () => {

    socket.write("hello world");
});

socket.on('data', (data) => {

    console.log(`${data}`);
    socket.destroy();
});