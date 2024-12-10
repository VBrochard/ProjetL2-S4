from flask import *
from flask_socketio import *

app = Flask(__name__)
socketio = SocketIO(app)

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


def motExiste(mot):
    with open('Ressources/Dico.txt', 'r', encoding='utf-8') as fichier:
        mots_dictionnaire = {ligne.strip().upper() for ligne in fichier}
        if mot.upper() in mots_dictionnaire:
            return True
        else:
            return False

def genererToutesLesCombis(s):
    result = []
    def permuter(prefixe, remaining):
        if prefixe:
            result.append(prefixe)
        for i in range(len(remaining)):
            permuter(prefixe + remaining[i], remaining[:i] + remaining[i+1:])
    permuter("", s)
    return result

def plusLongDansUneListe(l):
    return max(liste_mots, key=len)

def motLePlusLong(s):
    genererToutesLesCombis(s)
    a = plusLongDansUneListe(result)
    print(f"Le mot le plus long avec ces lettres est {a}")

