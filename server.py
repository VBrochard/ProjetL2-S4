from flask import *
from flask_socketio import *
from random import *
from itertools import permutations

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

TokenReponse = int(0)
ListeJoueurs = []
NbrJoueurs = 2
taille_deck = 7
deck = []
MeilleurMotJoueur = ""
NomMeilleurJoueur = ""
MeilleurPossible = ""
limiteScore = 10
jetonPret = 0

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
    return max_mot



def sommeDesFreq():
    b = 0
    for lettre, freq in lettres_freq.items():
        b+= freq
    return b

def eniemeCarte(n):
    return cartes_freq[n - 1]



def genererUnDeck():
    global deck
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
    global ListeJoueurs
    ListeJoueurs.append([str(data),0])
    print(data, "Rejoint la partie")
    if len(ListeJoueurs) == NbrJoueurs:
        socketio.emit('Lancement',ListeJoueurs)
        socketio.emit('tirageLettres',genererUnDeck())

@socketio.on('nouveauTour')
def handle_nouveauTour():
    global jetonPret
    jetonPret+=1
    if jetonPret == NbrJoueurs:
        socketio.emit('tirageLettres',genererUnDeck())
        jetonPret = 0

@socketio.on('envoiMot')
def handle_envoieMot(data):
    global deck
    global TokenReponse
    global MeilleurMotJoueur
    global NomMeilleurJoueur
    global ListeJoueurs
    global MeilleurPossible
    
    if ((motExiste(data.get("mot"))) and (len(data.get("mot")) > len(MeilleurMotJoueur))):
        MeilleurMotJoueur = data.get("mot")
        NomMeilleurJoueur = data.get("nom")
    TokenReponse += 1
    print(TokenReponse)
    MeilleurPossible = motLePlusLong(deck)
    nomsVainqueurs = []
    scoresVainqueurs = []
    if TokenReponse == NbrJoueurs:
        
        for joueur in ListeJoueurs:
            if joueur[0] == NomMeilleurJoueur: 
                joueur[1] += len(MeilleurMotJoueur) 
                break

        for joueur in ListeJoueurs:
            if joueur[1]>=limiteScore:
                nomsVainqueurs.append(joueur[0])
                scoresVainqueurs.append(joueur[1])
        if len(nomsVainqueurs)>0:
            socketio.emit('victoire',{"nomsVainqueurs":nomsVainqueurs,"scoresVainqueurs":scoresVainqueurs})
        else:
            socketio.emit('résultat', {
                "nom" : NomMeilleurJoueur,
                "ListeScore" : ListeJoueurs,
                "PointGagnée" : len(MeilleurMotJoueur),
                "meilleurPossible" : MeilleurPossible,
                "MotGagnant" : MeilleurMotJoueur
                })
        TokenReponse = 0
        MeilleurMotJoueur = ""

if __name__ == '__main__':
    socketio.run(app, debug=True)

