import socketio

sio = socketio.Client()
sio.connect('http://localhost:5000')
print("Connecté !")

message = "bonjour"
sio.emit('message', message)
print("envoie du message")

@sio.event
def Renvoie2(data):
    print("evenement recu 2")
    print(data)


@sio.event
def Renvoie(data):
    print("evenement recu 1 ")
    print(data)


sio.wait()


