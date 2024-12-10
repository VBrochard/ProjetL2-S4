import socketio

sio = socketio.Client()
sio.connect('http://localhost:5000')
print("Connecté !")

message = "bonjour"
sio.emit('message', message)

@sio.event
def Renvoie2(data):
    print(data)


@sio.event
def Renvoie(data):
    print(data)



