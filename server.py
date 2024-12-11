from flask import *
from flask_socketio import *

app = Flask(__name__)
socketio = SocketIO(app, ping_timeout=10)


taille_deck = 7

@app.route('/')
def Arrivée():
    return render_template('clientgraphique')

@socketio.on('message')
def handle_message(data):
    print("Message reçu : ",data)
    emit("Renvoie",data)
    print("Renvoie 1 fait")
    emit("Renvoie2","Samy va avoir du boulot")
    print("Renvoie 2 fait")


if __name__ == '__main__':
    socketio.run(app, debug=True)

lettres_freq = {"A": 9, "B": 2, "C": 2, "D":3, "E":15, "F":2, "G": 2, "H":}

def motExiste(mot):
    with open("Ressources/Dico.txt", 'r', encoding='utf-8') as fichier:
        mots_dictionnaire = {ligne.strip().upper() for ligne in fichier}
        if mot.upper() in mots_dictionnaire:
            return True
        else:
            return False

def genererToutesLesCombis(s):
    result = []
    def permuter(prefixe, remaining):
        if motExiste(prefixe):
            result.append(prefixe)
        for i in range(len(remaining)):
            permuter(prefixe + remaining[i], remaining[:i] + remaining[i+1:])
    permuter("", s)
    return result

def plusLongDansUneListe(l):
    return max(l, key=len)

def motLePlusLong(s):
    b = genererToutesLesCombis(s)
    a = plusLongDansUneListe(b)
    return f"Le mot le plus long avec ces lettres est '{a}'"


