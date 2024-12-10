from flask import Flask
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)
socketio = SocketIO(app)

#@app.route('/')
#def hello():
#    print("Connecté")
#    return 'Hello'




@socketio.on('message')
def handle_message(data):
    print("Message reçu : ",data)
    emit("Renvoie",data)
    emit("Renvoie2","Samy va avoir du boulot")


if __name__ == '__main__':
    socketio.run(app)