from flask import *
from flask_socketio import *
from random import *
from itertools import permutations
import sys
import time



app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

TokenReponse = int(0)
ListeJoueurs = []


deck = []
MeilleurMotsJoueur = []
NomMeilleursJoueurs = []
listePropositions = []
MeilleurPossible = ""
limiteScore = 10
jetonPret = 0
listeMots = []
jetonTourTirage = 0
nbrJoueur = 0

if len(sys.argv) != 3:
    print("Veuillez spécifier en argument le nombre de joueurs et la taille du deck")
    sys.exit(1)

try:
    nbrJoueur = int(sys.argv[1])
    print("Le serveur est configuré pour",nbrJoueur,"joueurs")
    taille_deck = int(sys.argv[2])
    print("Le serveur est configuré pour un deck de",taille_deck,"cartes")
except ValueError:
    print("Veuillez entrer un nombre valide pour le nombre de joueurs et la taille du deck")
    sys.exit(1)

lettres_freq = {"A": 9, "B": 2, "C": 2, "D":3, "E":15, "F":2, "G": 2, "H": 2, "I":8,"J":1, "K":1, "L":5, "M":3, "N":6, "O":6, "P":2, "Q":1, "R":6, "S":6, "T":6, "U":6,
"V": 2, "W": 1, "X": 1, "Z": 2}

cartes_freq = [carte for carte, freq in lettres_freq.items() for i in range(freq)]

def ouvrirDico():
    with open("Ressources/Dico.txt", 'r', encoding='utf-8') as fichier:
        return {ligne.strip().upper() for ligne in fichier}

dico = ouvrirDico()

def sommeDesFreq():
    b = 0
    for lettre, freq in lettres_freq.items():
        b+= freq
    return b

def eniemeCarte(n, tabCartes):
    return tabCartes[n - 1]

def genererUnDeck():
    deck = []
    for i in range(taille_deck):
        a = randint(0, sommeDesFreq())
        deck.append(eniemeCarte(a, cartes_freq))
    return deck

voyelles = [carte for carte, freq in lettres_freq.items() if carte in "AEIOUY" for i in range(freq)]
consonnes = [carte for carte, freq in lettres_freq.items() if carte not in "AEIOUY" for i in range(freq)]

def tirageCarteVoyelle():
    a = randint(0, len(voyelles))
    return eniemeCarte(a, voyelles)

def tirageCarteConsonne():
    a = randint(0, len(consonnes))
    return eniemeCarte(a, consonnes)

def motMax(listeMots):
    return len(max(listeMots, key=len))

def retireDoublon(liste):
    listeRes = []
    for elt in liste:
        if elt not in listeRes:
            listeRes.append(elt)
    return listeRes

def motLePlusLong(s):
    max_mot = ""
    for i in range(len(s), 0, -1): 
        for combi in permutations(s, i):
            mot = ''.join(combi)
            if motExiste(mot) and len(mot) > len(max_mot):
                max_mot = mot
    
    return max_mot

def motExiste(mot):
    return mot.upper() in dico


@app.route('/Ressources/<path:filename>')
def ressources(filename):
    return send_from_directory('Ressources', filename)

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
    if len(ListeJoueurs) == nbrJoueur:
        socketio.emit('Lancement',ListeJoueurs)
        time.sleep(0.5)
        socketio.emit('choixLettre',{"deck":deck,"joueur":ListeJoueurs[jetonTourTirage][0]})
    else:
        socketio.emit('ListePresence',ListeJoueurs)



@socketio.on('Declancheur')
def handle_declancheur():
        global nbrJoueur
        nbrJoueur = len(ListeJoueurs)
        socketio.emit('Lancement',ListeJoueurs)
        time.sleep(0.5)
        socketio.emit('choixLettre',{"deck":deck,"joueur":ListeJoueurs[jetonTourTirage][0]})


@socketio.on('DemandeTailleDeck')
def handle_DemandeTailleDeck():
    socketio.emit('EnvoieTailleDeck',taille_deck)


@socketio.on('voyelle')
def handle_voyelle():
    global deck
    global ListeJoueurs
    global jetonTourTirage
    global nbrJoueur
    deck += tirageCarteVoyelle()
    jetonTourTirage += 1
    if jetonTourTirage == nbrJoueur:
        jetonTourTirage = 0
    if len(deck) == taille_deck:
        socketio.emit('tirageLettres',{"deck" : deck, "TokenComplet" : len(deck)== taille_deck})
    else:
        socketio.emit('choixLettre',{"deck":deck,"joueur":ListeJoueurs[jetonTourTirage][0]})

@socketio.on('consonne')
def handle_voyelle():
    global deck
    global ListeJoueurs
    global jetonTourTirage
    deck += tirageCarteConsonne()
    jetonTourTirage += 1
    if jetonTourTirage == nbrJoueur:
        jetonTourTirage = 0
    if len(deck) == taille_deck:
        socketio.emit('tirageLettres',{"deck" : deck, "TokenComplet" : len(deck)== taille_deck})
    else:
        socketio.emit('choixLettre',{"deck":deck,"joueur":ListeJoueurs[jetonTourTirage][0]})


@socketio.on('nouveauTour')
def handle_nouveauTour():
    global jetonPret
    global deck
    deck = []
    
    jetonPret+=1
    if jetonPret == nbrJoueur:
        socketio.emit('choixLettre',{"deck":deck,"joueur":ListeJoueurs[jetonTourTirage][0]})
        jetonPret = 0

@socketio.on('envoiMot')
def handle_envoieMot(data):
    global deck
    global TokenReponse
    global MeilleurMotsJoueur
    global NomMeilleursJoueurs
    global ListeJoueurs
    global MeilleurPossible
    global listePropositions
    global listeMots

    listePropositions.append([data.get("nom"),data.get("mot")])
    listeMots.append(data.get("mot"))
    
    TokenReponse += 1
    MeilleurPossible = motLePlusLong(deck)
    nomsVainqueurs = []
    scoresVainqueurs = []
    if TokenReponse == nbrJoueur:

        tailleMotPlusGrand = motMax(listeMots)
        for reponse in listePropositions:
            if len(reponse[1]) == tailleMotPlusGrand and motExiste(reponse[1]):
                MeilleurMotsJoueur.append(reponse[1])
                NomMeilleursJoueurs.append(reponse[0])

        for joueur in ListeJoueurs:
            if joueur[0] in NomMeilleursJoueurs: 
                joueur[1] += tailleMotPlusGrand
                

        for joueur in ListeJoueurs:
            if joueur[1]>=limiteScore:
                nomsVainqueurs.append(joueur[0])
                scoresVainqueurs.append(joueur[1])

        if len(nomsVainqueurs)>0:
            socketio.emit('victoire',{"nomsVainqueurs":nomsVainqueurs,"tableauScores":ListeJoueurs})
        else:
            socketio.emit('résultat', {
                "nom" : retireDoublon(NomMeilleursJoueurs),
                "ListeScore" : ListeJoueurs,
                "PointGagnée" : tailleMotPlusGrand,
                "meilleurPossible" : MeilleurPossible,
                "MotGagnant" : retireDoublon(MeilleurMotsJoueur)
                })
        TokenReponse = 0
        NomMeilleursJoueurs = []
        MeilleurMotsJoueur = []
        listePropositions = []
        listeMots = []

if __name__ == '__main__':
    socketio.run(app, debug=True)

