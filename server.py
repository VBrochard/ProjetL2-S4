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

#Variables mot le plus long
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
"V": 2, "W": 1, "X": 1, "Y" : 1, "Z": 2}

cartes_freq = [carte for carte, freq in lettres_freq.items() for i in range(freq)]

def ouvrirDico():
    with open("Ressources/Dico.txt", 'r', encoding='utf-8') as fichier:
        return {ligne.strip().upper() for ligne in fichier}

dico = ouvrirDico()

def sommeDesFreq(cartes):
    return len(cartes)

def eniemeCarte(n, tabCartes):
    return tabCartes[n - 1]

voyelles = [carte for carte, freq in lettres_freq.items() if carte in "AEIOUY" for i in range(freq)]
consonnes = [carte for carte, freq in lettres_freq.items() if carte not in "AEIOUY" for i in range(freq)]

def tirageCarteVoyelle():
    a = randint(0, len(voyelles))
    return eniemeCarte(a, voyelles)

def tirageCarteConsonne():
    a = randint(0, len(consonnes))
    return eniemeCarte(a, consonnes)

def motMax(listeMots):
    motsValides = [mot for mot in listeMots if motExiste(mot)]
    return len(max(motsValides, key=len))

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

def retireUneVoyelle_lplm(lettre):
    voyelles.remove(lettre)

def retireUneConsonne_lplm(lettre):
    consonnes.remove(lettre)

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

@app.route('/OptiMot.html')
def Optimot():
    return render_template('OptiMot.html')

@app.route('/banana_solitaire.html')
def Banana_Solitaire():
    return render_template('banana_solitaire.html')

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
        socketio.emit('afficheLettres',deck)
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
    b = tirageCarteVoyelle()
    deck += b
    retireUneVoyelle_lplm(b)
    jetonTourTirage += 1
    if jetonTourTirage == nbrJoueur:
        jetonTourTirage = 0
    if len(deck) == taille_deck:
        socketio.emit('tirageLettres',{"deck" : deck, "TokenComplet" : len(deck)== taille_deck})
    else:
        socketio.emit('choixLettre',{"deck":deck,"joueur":ListeJoueurs[jetonTourTirage][0]})

@socketio.on('consonne')
def handle_consonne():
    global deck
    global ListeJoueurs
    global jetonTourTirage
    a = tirageCarteConsonne()
    deck += a
    retireUneConsonne_lplm(a)
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


##########################################################################
#Variables Opti'Mot
listeJoueursOM = []
jetonTourOM = 0

lettres_freq_opti = {"A": 5, "B": 1, "C": 2, "D":2, "E":9, "F":2, "G": 1, "H": 1, "I":5,"J":1, "K":1, "L":3, "M":3, "N":3, "O":3, "P":2, "Q":1, "R":3, "S":4, "T":3, "U":3,
"V": 2, "W": 1, "X": 1, "Y" : 1, "Z": 1}

cartes_freq_opti = [carte for carte, freq in lettres_freq_opti.items() for i in range(freq)]

def ajouterLettreDansPioche_opti(lettre):
    cartes_freq_opti.append(lettre)

def tirageCarteOpti():
    a = randint(0, len(cartes_freq_opti))
    return eniemeCarte(a, cartes_freq_opti)

def retireUneCarte_opti(lettre):
    cartes_freq_opti.remove(lettre)

@socketio.on('connexionOM')
def handle_connexionOM(data):
    nomJoueur = data
    mainDepart = []
    listeJoueursOM.append(nomJoueur)  
    for i in range(10):
        j = tirageCarteOpti()
        mainDepart.append(j)
        retireUneCarte_opti(j)
        socketio.emit('MainDepart',{"nom" : nomJoueur,'mainDepart' : mainDepart})
    if len(listeJoueursOM) == nbrJoueur:
        deckDepart = []
        for i in range(5):
            f = tirageCarteOpti()
            retireUneCarte_opti(f)
            deckDepart.append(f)
        socketio.emit("lancementOM",{"liste" :listeJoueursOM,"depart" : deckDepart})


@socketio.on('victoireOM')
def handle_victoireOM(data):
    socketio.emit('afficheVictoireOM',data)
    
@socketio.on('finTourOM')
def handle_tourSuivantOM():
    global jetonTourOM
    jetonTourOM+=1
    if jetonTourOM == len(listeJoueursOM):
        jetonTourOM = 0
    socketio.emit('tourSuivantOM',listeJoueursOM[jetonTourOM])

@socketio.on('verifierMotsOM')
def verifier_mots(mots):

    # Valider tous les mots
    tous_valides = all(motExiste(mot) for mot in mots)

    # Retourner le résultat au client
    emit('resultatValidationMotsOM', tous_valides)


@socketio.on('DemandePiocheOM')
def handle_DemandePioche(data):
    carte = tirageCarteOpti()
    socketio.emit('RetourPiocheOM',{"joueur" : data, 'pioche' : carte})


@socketio.on('TransmissionCaseRemplieOM')
def handle_TransmissionCaseRemplie(data):
    tab = data['position']
    socketio.emit('MettreLettreOM',{"position" : tab, "nomJ" :  data['nomJ']})



###############################################################################
# Nécessaire Banana Solitaire

lettres_regime = {"A": 14, "B": 3, "C": 4, "D":4, "E":21, "F":3, "G": 2, "H": 2, "I":12,"J":1, "K":1, "L":7, "M":4, "N":9, "O":9, "P":3, "Q":1, "R":9, "S":9, "T":9, "U":9,
"V": 3, "W": 1, "X": 1, "Z": 2}

cartes_regime = [carte for carte, freq in lettres_regime.items() for i in range(freq)]

def genererUnDeck(cartes, taille):
    deck = []
    for i in range(taille):
        a = randint(0, sommeDesFreq(cartes))
        lettre = eniemeCarte(a, cartes)
        deck.append(lettre)
        cartes.remove(lettre)
    return deck

def deckBanana(nbj):
    if(nbj == 2 or nbj == 3 or nbj == 4):
        return genererUnDeck(cartes_regime, 21)
    if(nbj == 5 or nbj == 6):
        return genererUnDeck(cartes_regime, 15)
    if(nbj == 7 or nbj == 8):
        return genererUnDeck(cartes_regime, 11)
    return "Erreur, le nombre de joueurs doit être compris entre 2 et 8 inclus "


@socketio.on('connexionBSolitaire')
def handle_connexionBSolitaire(data):
    mainDepart = genererUnDeck(cartes_regime,int(data))
    socketio.emit('MainDepart', mainDepart)



if __name__ == '__main__':
    socketio.run(app, host= '0.0.0.0', port=5000, debug=True)
