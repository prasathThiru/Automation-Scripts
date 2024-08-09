//var unirest = require(process.env['HOME_PATH'] + '/node_modules/unirest');
const Net = require('net')
const express = require(process.env['HOME_PATH'] + '/node_modules/express');
var cors = require(process.env['HOME_PATH'] + '/node_modules/cors');
var bodyParser = require(process.env['HOME_PATH'] + '/node_modules/body-parser');

const tcpServer = new Net.Server()
var clientSocket = null
var TCP_SERVER_PORT = 8100
var API_SERVER_PORT = 8101
const HEARTBEAT_INTERVAL = 60000

const app = express()
app.use(cors())
app.use(bodyParser.urlencoded({
    extended: true
}))
app.use(bodyParser.json())

console.log("RESTtoTCP: Arguments " + process.argv)

if (process.argv[2] == null || process.argv[3] == null ) {
	console.log("RESTtoTCP: Usage TCPServerPort APIServerPort\n")
	return
}
try {
    TCP_SERVER_PORT = parseInt(process.argv[2])
    API_SERVER_PORT = parseInt(process.argv[3])
} catch (error) {
    console.log("RESTtoTCP: Invalid port number")
    return
}


setInterval(function() {

	if (clientSocket && !clientSocket.destroyed){
	var obj = { "timestamp": new Date().getTime() }
	let message = JSON.stringify(obj).toString('utf8')
	let dataLength = 4 + message.length
	let data = new Uint8Array(dataLength)
	let buff = Buffer.from(data.buffer)
        buff.writeUInt32BE(dataLength)
		        buff.write(message, 4)
		        clientSocket.write(data, function(err) {
				                if (err){
							                        console.log("RESTtoTCP: Error TCP for heartbeat " + JSON.stringify(err))
							                }
				                else {
							                       console.log("RESTtoTCP: Heartbeat sent successfully " + JSON.stringify(obj) + " Port: " + TCP_SERVER_PORT)
							                }
				        })
    	} else {
	    console.log("RESTtoTCP: No client heartbeat " + "Port: " + TCP_SERVER_PORT)
	}


}, HEARTBEAT_INTERVAL);

app.post('/api/tcp', function (req, res) {
    console.log("RESTtoTCP: Received on API:" + JSON.stringify(req.body, null, 4));
    if (clientSocket && !clientSocket.destroyed){
        let event = JSON.stringify(req.body).toString('utf8')
        let dataLength = 4 + event.length
        let data = new Uint8Array(dataLength)
        let buff = Buffer.from(data.buffer)
        buff.writeUInt32BE(dataLength)
        buff.write(event, 4)
        clientSocket.write(data, function(err) {
		if (err){
			console.log("RESTtoTCP: Error TCP " + JSON.stringify(err))
		}
		else {
			console.log("RESTtoTCP: Message sent to client successfully " + "LP reading: " + req.body.event.reading + " Port: " + TCP_SERVER_PORT)
		}
            res.json({
                    message: 'Sent Status:' + err
                })
        })
    } else {
	    console.log("RESTtoTCP: No client")
        res.json({
            message: 'Dropped Status: no client'
        })
    }
})

tcpServer.on('connection', function (socket) {

	console.log('RESTtoTCP: New connection ' + socket.remoteAddress + ":" + socket.remotePort)
    socket.setKeepAlive(true)
    clientSocket = socket
	socket.on('data', function (data) {
        console.log("RESTtoTCP: Message from " + socket.remoteAddress + ":" + socket.remotePort + ' msg:' + data.toString('utf8'))
	})

	socket.on('end', function () {
        if (clientSocket) {
            clientSocket.destroy()
            clientSocket = null
        }
		console.log("RESTtoTCP: Connection end " + socket.remoteAddress + ":" + socket.remotePort)
	})

	socket.on('error', function (err) {
        if (clientSocket) {
            clientSocket.destroy()
            clientSocket = null
        }
        console.log("RESTtoTCP: Connection error " + socket.remoteAddress + ":" + socket.remotePort, " err:" + JSON.stringify(err))
	})

	socket.on('close', function (err) {
        if (clientSocket) {
            clientSocket.destroy()
            clientSocket = null
        }
        console.log("RESTtoTCP: Connection close " + socket.remoteAddress + ":" + socket.remotePort, " err:" + JSON.stringify(err))
	})

});

tcpServer.listen(TCP_SERVER_PORT, function () {
    console.log("RESTtoTCP: TCP Server Started " + TCP_SERVER_PORT)
})

var apiServer = app.listen(API_SERVER_PORT, function () {
    console.log("RESTtoTCP: API Server Started " + API_SERVER_PORT)
})

process.on('SIGINT', function() {
    apiServer.close(function(apiErr) {
      tcpServer.close(function(tcpErr) { 
        process.exit(tcpErr || apiErr ? 1 : 0)
      })
    })
 })
