from flask import *
from flask_socketio import *
from random import *
from itertools import permutations

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

ListeJoueurs = []
NbrJoueurs = 2
TokenReponse = 0

lettres_freq = {"A": 9, "B": 2, "C": 2, "D":3, "E":15, "F":2, "G": 2, "H": 2, "I":8,"J":1, "K":1, "L":5, "M":3, "N":6, "O":6, "P":2, "Q":1, "R":6, "S":6, "T":6, "U":6,
"V": 2, "W": 1, "X": 1, "Z": 2}

cartes_freq = [carte for carte, freq in lettres_freq.items() for _ in range(freq)]

def ouvrirDico():
    with open("Ressources/Dico.txt", 'r', encoding='utf-8') as fichier:
        return {ligne.strip().upper() for ligne in fichier}

dico = ouvrirDico()

def motExiste(mot):
    return mot.upper() in dico

def motLePlusLong(s):
    max_mot = ""
    
    for i in range(len(s), 0, -1): 
        for combi in permutations(s, i):
            mot = ''.join(combi)
            if motExiste(mot) and len(mot) > len(max_mot):
                max_mot = mot
    
    return f"Le mot le plus long avec ces lettres est '{max_mot}'"



def sommeDesFreq():
    b = 0
    for lettre, freq in lettres_freq.items():
        b+= freq
    return b

def eniemeCarte(n):
    return cartes_freq[n - 1]

taille_deck = 7

def genererUnDeck():
    deck = []
    for i in range(taille_deck):
        a = randint(0, sommeDesFreq())
        deck.append(eniemeCarte(a))
    return deck

@app.route('/')
def Arrivée():
    socketio.emit('connecté')
    return render_template('index.html')

@app.route('/le_plus_long.html')
def LeMotlepluslong():
    return render_template('le_plus_long.html')

@socketio.on('AnnonceJoueur')
def handle_AnnonceJoueur(data):
    ListeJoueurs.append(data)
    print(data, "Rejoint la partie")
    if len(ListeJoueurs) == NbrJoueurs:
        socketio.emit('Lancement',ListeJoueurs)
        socketio.emit('tirageLettres',genererUnDeck())

if __name__ == '__main__':
    socketio.run(app, debug=True,log_output=True)


