from flask import *
from flask_socketio import *
from random import *
from itertools import permutations
import sys
import time
import requests
from bs4 import BeautifulSoup
import math
import re
import random



app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

TokenReponse = int(0)
ListeJoueurs = []

#Variables Serveur
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
nbrBananaSpeed = 0
difficulteRand=[]




if len(sys.argv) != 3:
    print("Veuillez spécifier en argument le nombre de joueurs et la taille du deck")
    sys.exit(1)

if len(sys.argv) == 3:
    try:
        nbrJoueur = int(sys.argv[1])
        nbrJoueurCL = int(sys.argv[1])
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
    if motsValides == []:
        return 0
    return len(max(motsValides, key=len))

def retireDoublon(liste):
    listeRes = []
    for elt in liste:
        if elt not in listeRes:
            listeRes.append(elt)
    return listeRes

def motLePlusLong(s):
    #Recherche le mot le plus long qu'il est possible d'écrire avec la string s
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

def splitUpper(txt):
    ajout = False
    res = ""
    
    for i in range(len(txt)):
        if ((txt[i].isupper() or txt[i] == "(") and ajout==False ):
            res+=txt[i]
            ajout = True
            
        elif txt[i] == "<":
            ajout=False
            
        else:
            if ajout:
                res+=txt[i]
    return res

def recupInfoMot(mot):
    #Récupère touts les types d'indices pour un mot donné:
    #Longueur, nature, première lettre, définition
    mot = mot.lower()
    nature = ""
    definition = ""
    nb_lettres = len(mot)
    premiereLettre = mot[0]
    listeTerminaisons = ["er","ir","re"]
    url = "https://fr.wikwik.org/"+mot
    response = requests.get(url)
    if response.status_code == 200:

        soup = BeautifulSoup(response.content,"html.parser")
        ligne = soup.find_all("li")[:1]

        if " art." in str(ligne[0]):
            nature = "Article"
        
        elif " n." in str(ligne[0]):
            nature = "Nom"
        
        elif " conj. " in str(ligne[0]):
            nature = "Conjonction"
        
        elif " v. " in str(ligne[0]):
            nature = "Verbe"
        
        elif " adj. " in str(ligne[0]):
            nature = "Adjectif"
        
        elif " pron." in str(ligne[0]):
            nature = "Pronom"
        
        elif " adv." in str(ligne[0]):
            nature = "Adverbe"

        elif " interj." in str(ligne[0]) or " ono. " in str(ligne[0]):
            nature = "Interjection"
        
        elif " prép." in str(ligne[0]):
            nature = "Préposition"

        definition=splitUpper(str(ligne[0]))
        if nature == "Verbe" and not(mot[:(len(mot)-2)] in listeTerminaisons):
            coupe = definition.split()
            definition = ""
            for i in range(len(coupe)-2):
                if i<len(coupe)-2:
                    definition+=coupe[i]+" "
                else:
                    definition+=coupe[i]
        
        return ["Longueur du mot: "+str(len(mot)), "Nature du mot: "+nature , "Première lettre du mot: "+mot[0], "Définition du mot: "+definition]
    else:
        print("Chargement de la page impossible")
        return   

@app.route('/Ressources/<path:filename>')
def ressources(filename):
    return send_from_directory('Ressources', filename)

@app.route('/')
def Arrivée():
    socketio.emit('connecté')
    return render_template('index.html')

@app.route('/index.html')
def returnMenu():
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

@app.route('/le_compte_est_bon.html')
def Le_Compte_est_Bon():
    return render_template('le_compte_est_bon.html')

@app.route('/banana_speed.html')
def Banana_Speed():
    return render_template('banana_speed.html')

@app.route('/BananaGramms.html')
def BananaGramms():
    return render_template('BananaGramms.html')

@app.route('/chiffre_lettre.html')
def Des_Chiffres_et_des_Lettres():
    return render_template('chiffre_lettre.html')

@app.route('/menu_chiffre_lettre')
def MenuChiffreLettre():
    return render_template('menu_chiffre_lettre.html')

#Réception du nom du joueur qui vient de se connecter
@socketio.on('AnnonceJoueur')
def handle_AnnonceJoueur(data):
    global ListeJoueurs
    ListeJoueurs.append([str(data),0]) #Ajout du joueur à la liste et initialisation de son score à 0
    print(data, "Rejoint la partie")
    if len(ListeJoueurs) == nbrJoueur: #Lancement de la partie si nombre de joueurs max atteint
        socketio.emit('Lancement',ListeJoueurs)
        time.sleep(0.5)
        socketio.emit('choixLettre',{"deck":deck,"joueur":ListeJoueurs[jetonTourTirage][0]})
    else:
        socketio.emit('ListePresence',ListeJoueurs) #Envoi de la possibilité de démarrer la partie avant le nombre de joueurs max atteint

#Début de la partie déclenchée par le maître du jeu
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

#Ajout d'une voyelle au deck
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

#Ajout d'une consonne au deck
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


#Démarre le nouveau tour dès que tous les joueurs ont appuyé sur le bouton prêt
@socketio.on('nouveauTour')
def handle_nouveauTour():
    global jetonPret
    global deck
    deck = []
    
    jetonPret+=1
    if jetonPret == nbrJoueur:
        socketio.emit('choixLettre',{"deck":deck,"joueur":ListeJoueurs[jetonTourTirage][0]})
        jetonPret = 0

#Récupération des propositions de mots des joueurs et recherche du/des mots vainqueur(s)
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
    if TokenReponse == nbrJoueur: #Si tous les joueurs ont envoyé leur réponse
        tailleMotPlusGrand = motMax(listeMots) #Récupère la longueur du plus long mot qui existe dans les propositions

        for reponse in listePropositions: #Recherche de tous les mots de même longueur que tailleMotPlusGrand
            if len(reponse[1]) == tailleMotPlusGrand and motExiste(reponse[1]):
                MeilleurMotsJoueur.append(reponse[1])
                NomMeilleursJoueurs.append(reponse[0])

        for i in range(len(ListeJoueurs)): #Mise à jour des scores
            if ListeJoueurs[i][0] in NomMeilleursJoueurs: 
                ListeJoueurs[i][1] += tailleMotPlusGrand 
                if ListeJoueurs[i][1]<0:
                    ListeJoueurs[i][1] = 0

        for joueur in ListeJoueurs: #Vérification de présence de vainqueur(s) ayant atteint la limite de score
            if joueur[1]>=limiteScore:
                nomsVainqueurs.append(joueur[0])
                scoresVainqueurs.append(joueur[1])

        if len(nomsVainqueurs)>0: #S'il existe un vainqueur, fin de partie
            socketio.emit('victoire',{"nomsVainqueurs":nomsVainqueurs,"tableauScores":ListeJoueurs})
        else: #Aucun vainqueur donc début du nouveau tour
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

#Demande d'indice d'un joueur
@socketio.on('indice')
def handle_demandeIndice(data):
    global deck
    global ListeJoueurs
    for joueur in ListeJoueurs:
        if joueur[0] == data.get("nomJoueur"):
            joueur[1] -= 1
            if joueur[1] < 0:
                joueur[1] = 0
    listeIndices = recupInfoMot(motLePlusLong(deck))
    socketio.emit('retourIndice',{"indice":listeIndices[data.get("nbIndices")], "nomJoueur":data.get("nomJoueur")})

#Réinitialisation des variables pour démarrer une nouvelle partie
@socketio.on('recommencerPartie')
def handle_recommencerPartioe():
    global ListeJoueurs 
    global voyelles
    global consonnes
    global deck
    global jetonTourTirage

    jetonTourTirage = 0
    deck = []
    ListeJoueurs = []
    voyelles = [carte for carte, freq in lettres_freq.items() if carte in "AEIOUY" for i in range(freq)]
    consonnes = [carte for carte, freq in lettres_freq.items() if carte not in "AEIOUY" for i in range(freq)]
    socketio.emit("retourAccueil")


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

#Génération du deck du nombre de cartes demandé par le joueur
@socketio.on('connexionBSolitaire')
def handle_connexionBSolitaire(data):
    mainDepart = genererUnDeck(cartes_regime,int(data))
    socketio.emit('MainDepartBSolitaire', mainDepart)

#Ajout d'une carte de la pioche au deck du joueur
@socketio.on('DemandePiocheSolitaire')
def handle_DemandePioche():
    carte = genererUnDeck(cartes_regime,1)[0]
    socketio.emit('RetourPiocheSolitaire', carte )

#Vérifiaction de la validité de tous les mots de la grille
@socketio.on('verifierMotsSolitaire')
def verifier_mots(mots):
    # Valider tous les mots
    tous_valides = all(motExiste(mot) for mot in mots)
    emit('resultatValidationMotsSolitaire', tous_valides)

#Regénération des cartes du régime
@socketio.on('ResetPartieSolitaire')
def ResetPartieSolitaire():
    global cartes_regime
    cartes_regime = [carte for carte, freq in lettres_regime.items() for i in range(freq)]

###############################################################################
# Nécessaire Banana Speed

lettres_regime_speed = {"A": 14, "B": 3, "C": 4, "D":4, "E":21, "F":3, "G": 2, "H": 2, "I":12,"J":1, "K":1, "L":7, "M":4, "N":9, "O":9, "P":3, "Q":1, "R":9, "S":9, "T":9, "U":9,
"V": 3, "W": 1, "X": 1, "Z": 2}

cartes_regime_speed = [carte for carte, freq in lettres_regime_speed.items() for i in range(freq)]


nbrJoueurSpeed = 0
listeJoueursSpeed = []

def genererUnDeckSpeed(cartes, taille):
    deck = []
    for i in range(taille):
        a = randint(0, sommeDesFreq(cartes))
        lettre = eniemeCarte(a, cartes)
        deck.append(lettre)
        cartes.remove(lettre)
    return deck

#Connexion d'un nouveau joueur
@socketio.on('connexionSpeed')
def handle_connexionBSpeed(data):
    global nbrJoueurSpeed
    global listeJoueursSpeed
    global nbrBananaSpeed
    global difficulteRand
    nbrJoueurSpeed += 1
    listeJoueursSpeed.append(data.get("joueur"))
    difficulteRand.append(data.get("difficulté"))
    if(nbrJoueurSpeed == 2):
        nbrBananaSpeed = int(difficulteRand[random.randint(0, 1)])
        mainDepart = genererUnDeckSpeed(cartes_regime_speed,nbrBananaSpeed)
        socketio.emit('MainDepartSpeed', mainDepart)

#Ajout d'une carte au deck du joueur qui pioche
@socketio.on('DemandePiocheSpeed')
def handle_DemandePioche(data):
    carte = genererUnDeck(cartes_regime_speed,1)[0]
    socketio.emit('RetourPiocheSpeed', {"carte" : carte,"Joueur" : data} )

#Vérification des mots de la grille
@socketio.on('verifierMotsSpeed')
def verifier_mots(mots):
    # Valider tous les mots
    tous_valides = all(motExiste(mot) for mot in mots)
    emit('resultatValidationMotsSpeed', tous_valides)

#Réinitialisation des variables pour recommencer une partie
@socketio.on('ResetPartieSpeed')
def ResetPartieSpeed():
    global cartes_regime_speed
    global nbrJoueurSpeed
    global listeJoueursSpeed
    global nbrBananaSpeed
    nbrBananaSpeed = 0
    nbrJoueurSpeed = 0
    listeJoueursSpeed = []
    cartes_regime_speed = [carte for carte, freq in lettres_regime_speed.items() for i in range(freq)]
    socketio.emit('ResetOrdreSpeed')

#Envoi de l'alerte de fin de partie en cas de victoire d'un joueur
@socketio.on('AlerteVictoireSolitaire')
def AlerteVictoire(data):
    socketio.emit('AlerteAutreJoueurSolitaire',data)

#####################################################################
#Le compte est bon

def creerListeNombres():
    return [1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,25,50,75,100]

listeJoueursCB = []
deckCB = []
listeGlobale = creerListeNombres()
objectif = 0
listeProp = []
listeVainqueurs = []
jetonPretCB = 0


def construireMainNombres(lstNombres):
    main = []
    while len(main) < 6:
        indiceRandom = randint(0,(len(lstNombres)-1))
        main.append(lstNombres[indiceRandom])
    return main

def construitOperation(calcul): 
    #Prends en paramètre un string d'une opération arithmétique valide et évalue son résultat
    if calcul == '':
        calcul ='0'
    return math.floor(eval(calcul))

def toutIndex(lst,cible): 
    #Renvoie tous les indices de la cible dans la liste
    res = []
    for i in range(len(lst)):
        if lst[i] == cible:
            res.append(i)
    return res


#Vérifie les propositions des joueurs et renvoie le(s) vainqueur(s) avec leur score

def vainqueurs(listeProposition,objectif):
    lstVainqueurs = []
    lstScores = []
    score = 0
    score = 7
    for i in range(len(listeProposition)):
        if listeProposition[i][1] == objectif:
            lstVainqueurs.append(listeProposition[i])
            score = 10
        else:
            lstScores.append(abs(objectif - listeProposition[i][1]))
    if lstVainqueurs != []:
        return lstVainqueurs,score
    
    for elt in toutIndex(lstScores,min(lstScores)):
        lstVainqueurs.append(listeProposition[elt])
    
    return lstVainqueurs,score
  
def retireEspaceVide(liste):
    return [element for element in liste if element!=""]

#Connexion d'un joueur
@socketio.on('AnnonceJoueurCB')
def handle_AnnonceJoueur(data):
    global listeJoueursCB
    global deckCB
    global objectif
    listeJoueursCB.append([str(data),0])
    print(data, "Rejoint la partie")
    if len(listeJoueursCB) == nbrJoueur:
        #Construction du deck et génération aléatoire de l'objectif à atteindre
        socketio.emit('Lancement',listeJoueursCB)
        deckCB = construireMainNombres(listeGlobale)
        objectif = randint(101,999)
        time.sleep(0.5)
        socketio.emit('debut',{"deck":deckCB,"objectif":objectif})
    else:
        socketio.emit('ListePresence',listeJoueursCB)

#Début de partie demandée par le maître du jeu
@socketio.on('DeclancheurCB')
def handle_declancheur():
        global nbrJoueur
        deck = construireMainNombres(listeGlobale)
        objectif = randint(101,999)
        nbrJoueur = len(listeJoueursCB)
        socketio.emit('Lancement',listeJoueursCB)
        time.sleep(0.5)
        socketio.emit('debut',{"deck":deck,"objectif":objectif})

#Récupère les propositions des joueurs et vérifie qui a remporté cette manche
@socketio.on('verificationCB')
def handle_verificationCB(data):
    global objectif
    global nbrJoueur
    global listeProp
    global listeVainqueurs
    global deck
    global listeJoueursCB
    
    resultat = construitOperation(data.get('proposition'))
    listeProp.append([data.get("nom"),resultat])
    print("ListeProp",listeProp)
    if len(listeProp) == nbrJoueur:
        listeVainqueurs,points = vainqueurs(listeProp,objectif)

        noms = []
        scoreVainqueur = listeVainqueurs[0][1]
        for elt in listeVainqueurs:
            noms.append(elt[0])
        
        for elt in listeJoueursCB:
            if elt[0] in noms:
                elt[1]+=points


        socketio.emit('resultat',{"noms":noms,"scoreVainqueur":scoreVainqueur,"tableau":listeJoueursCB})
        listeVainqueurs = []
        listeProp = []
        deck = []

#Début du nouveau tour quand tous les joueurs sont prêts
@socketio.on('nouveauTourCB')
def handle_nouveauTourCB():
    global jetonPretCB
    global deck

    jetonPretCB+=1
    if jetonPretCB == nbrJoueur:
        deck = construireMainNombres(listeGlobale)
        objectif = randint(101,999)
        socketio.emit('debut',{"deck":deck, "objectif":objectif})
        jetonPretCB = 0

#Renvoie le résultat du calcul intermédiaire fait par un joueur
@socketio.on('calculer')
def handle_calculer(data):
    print(data.get("expression"))
    listeNombres = re.split('[+ \- * /]+',data.get('expression'))
    listeNombres=retireEspaceVide(listeNombres)
    resultat = construitOperation(data.get("expression"))
    print(data)
    socketio.emit("retourCalcul",{"expression" :resultat,"Joueurs" : data.get("Joueurs"), "listeNombres":listeNombres})

###############################################################################
#Des chiffres et des lettres

listeJoueursCL = []
deckLettres = []
deckNombres = []
deckCL = []
jetonTourTirageCL = 0
jetonPretCL = 0
MeilleurMotsJoueurCL = []
NomMeilleursJoueursCL = []
MeilleurPossibleCL = ""
listePropositionsCL = []
listeMotsCL = []
listeVainqueursCL = []
TokenReponseCL = 0
nbPartiesLPLM = 1
nbRounds = 0
objectifCL = 0
listeCoups = []

def envoiGagnants(listeScores):
    res = []
    max = 0
    for elt in listeScores:
        if elt[1] > max:
            max = elt[1]
            res = []
            res.append(elt)
        elif elt[1] == max:
            res.append(elt)
    return res


def inverseListe(liste):
    liste[0],liste[1] = liste[1],liste[0]
    return liste

#Connexion d'un joueur
@socketio.on('AnnonceJoueurCL')
def handle_AnnonceJoueurCL(data):
    global listeJoueursCL
    global listeCoups
    listeJoueursCL.append([str(data),0])
    listeCoups.append([str(data)])
    print(data, "Rejoint la partie")
    print(len(ListeJoueurs),nbrJoueurCL)
    if len(listeJoueursCL) == nbrJoueurCL:
        socketio.emit('LancementCL',ListeJoueurs)
        time.sleep(0.5)
        socketio.emit('choixLettreCL',{"deck":deckCL,"joueur":listeJoueursCL[jetonTourTirageCL][0]})
    else:
        socketio.emit('ListePresenceCL',listeJoueursCL)

#Début de partie demandé par le maître du jeu
@socketio.on('DeclancheurCL')
def handle_declancheurCL():
        global nbrJoueur
        nbrJoueurCL = len(listeJoueursCL)
        socketio.emit('LancementCL',listeJoueursCL)
        time.sleep(0.5)
        socketio.emit('afficheLettresCL',deckCL)
        time.sleep(0.5)
        socketio.emit('choixLettreCL',{"deck":deckCL,"joueur":listeJoueursCL[jetonTourTirageCL][0]})


@socketio.on('DemandeTailleDeckCL')
def handle_DemandeTailleDeckCL():
    socketio.emit('EnvoieTailleDeckCL',taille_deck)

#Ajout d'une voyelle au dekc
@socketio.on('voyelleCL')
def handle_voyelle():
    global deckCL
    global listeJoueursCL
    global jetonTourTirageCL
    global nbrJoueurCL
    b = tirageCarteVoyelle()
    deckCL += b
    retireUneVoyelle_lplm(b)
    jetonTourTirageCL += 1
    if jetonTourTirageCL == nbrJoueurCL:
        jetonTourTirageCL = 0
    if len(deckCL) == taille_deck:
        socketio.emit('tirageLettresCL',{"deck" : deckCL, "TokenComplet" : len(deckCL)== taille_deck})
    else:
        socketio.emit('choixLettreCL',{"deck":deckCL,"joueur":listeJoueursCL[jetonTourTirageCL][0]})

#Ajout d'une consonne au deck
@socketio.on('consonneCL')
def handle_consonneCL():
    global deckCL
    global listeJoueursCL
    global jetonTourTirageCL
    a = tirageCarteConsonne()
    deckCL += a
    retireUneConsonne_lplm(a)
    jetonTourTirageCL += 1
    if jetonTourTirageCL == nbrJoueurCL:
        jetonTourTirageCL = 0
    if len(deckCL) == taille_deck:
        socketio.emit('tirageLettresCL',{"deck" : deckCL, "TokenComplet" : len(deckCL)== taille_deck})
    else:
        socketio.emit('choixLettreCL',{"deck":deckCL,"joueur":listeJoueursCL[jetonTourTirageCL][0]})


#Nouveau tour quand tous les joueurs sont prêts
@socketio.on('nouveauTourCL')
def handle_nouveauTourCL():
    global jetonPretCL
    global deckCL
    global nbPartiesLPLM
    global objectifCL
    deckCL = []
    jetonPretCL+=1
    if jetonPretCL == nbrJoueurCL:
        if nbPartiesLPLM < 2: #Si 2 rounds du "mot le plus long" n'ont pas encore été joués, on reste sur ce jeu
            nbPartiesLPLM+=1
            socketio.emit('choixLettreCL',{"deck":deckCL,"joueur":listeJoueursCL[jetonTourTirageCL][0]})
            jetonPretCL = 0
        else: #Si 2 rounds du "mot le plus long" ont été joués, on lance un round du "compte est bon"
            deckCL = construireMainNombres(creerListeNombres())
            objectifCL = randint(101,999)
            print(deckCL,objectifCL)
            socketio.emit('debutPartieLCB',{"deck":deckCL, "objectif":objectifCL})
            jetonPretCL = 0
            nbPartiesLPLM = 0
            

#Vérification des propositions de mots des joueurs
@socketio.on('envoiMotCL')
def handle_envoiMotCL(data):
    global deckCL
    global TokenReponseCL
    global MeilleurMotsJoueurCL
    global NomMeilleursJoueursCL
    global listeJoueursCL
    global MeilleurPossibleCL
    global listePropositionsCL
    global listeMotsCL
    global nbrJoueurCL

    listePropositionsCL.append([data.get("nom"),data.get("mot"),data.get("nbIndices")])
    listeMotsCL.append(data.get("mot"))
    TokenReponseCL += 1
    MeilleurPossibleCL = motLePlusLong(deckCL)
    nomsVainqueurs = []
    scoresVainqueurs = []
    malusApplique = 0
    if TokenReponseCL == nbrJoueurCL:
        print("ListeCL",listeJoueursCL)
        tailleMotPlusGrand = motMax(listeMotsCL)
        for reponse in listePropositionsCL:
            if len(reponse[1]) == tailleMotPlusGrand and motExiste(reponse[1]):
                MeilleurMotsJoueurCL.append(reponse[1])
                NomMeilleursJoueursCL.append(reponse[0])

        for i in range(len(listeJoueursCL)):
            if listeJoueursCL[i][0] in NomMeilleursJoueursCL: 
                listeJoueursCL[i][1] += tailleMotPlusGrand 
                if listeJoueursCL[i][1]<0:
                    listeJoueursCL[i][1] = 0

        print(ListeJoueurs)
        socketio.emit('résultatCL', {
            "nom" : retireDoublon(NomMeilleursJoueursCL),
            "ListeScore" : listeJoueursCL,
            "PointGagnée" : tailleMotPlusGrand,
            "meilleurPossible" : MeilleurPossibleCL,
            "MotGagnant" : retireDoublon(MeilleurMotsJoueurCL)
            })

        TokenReponseCL = 0
        NomMeilleursJoueursCL = []
        MeilleurMotsJoueurCL = []
        listePropositionsCL = []
        listeMotsCL = []

#Envoi d'un indice au joueur qui le demande et baisse de son score
@socketio.on('indiceCL')
def handle_demandeIndiceCL(data):
    global deckCL
    global listeJoueursCL
    for joueur in listeJoueursCL:
        if joueur[0] == data.get("nomJoueur"):
            joueur[1] -= 1
            if joueur[1] < 0:
                joueur[1] = 0
    listeIndices = recupInfoMot(motLePlusLong(deckCL))
    socketio.emit('retourIndiceCL',{"indice":listeIndices[data.get("nbIndices")], "nomJoueur":data.get("nomJoueur")})

#Vérification des propositions de nombre des joueurs
@socketio.on('verificationCL')
def handle_verificationCL(data):
    global objectifCL
    global nbrJoueur
    global listePropositionsCL
    global listeVainqueursCL
    global deckCL
    global listeJoueursCL
    global nbRounds
    
    resultat = construitOperation(data.get('proposition'))
    listePropositionsCL.append([data.get("nom"),resultat])
    print("ListeProp",listePropositionsCL, nbrJoueurCL)
    if len(listePropositionsCL) == nbrJoueurCL:
        listeVainqueursCL,points = vainqueurs(listePropositionsCL,objectifCL)

        noms = []
        scoreVainqueur = listeVainqueursCL[0][1]
        for elt in listeVainqueursCL:
            noms.append(elt[0])
        
        for elt in listeJoueursCL:
            if elt[0] in noms:
                elt[1]+=points

        #Limite du nombre de rounds
        if nbRounds == 1:
            gagnants = envoiGagnants(listeJoueursCL)
            socketio.emit("victoirePartie",gagnants)
            nbRounds = 0
        else:
            nbRounds+=1
            socketio.emit('resultatLCB',{"noms":noms,"scoreVainqueur":scoreVainqueur,"tableau":listeJoueursCL})
            
        listeVainqueurs = []
        listeProp = []
        deckCL = []
        listePropositionsCL = []
        
        objectifCL = 0

#Envoi du résultat d'un calcul intermédiaire demandé par le joueur
@socketio.on("calculerCL")
def handle_calculerCL(data):
    global listeCoups
    listeNombres = re.split('[+ \- * /]+',data.get('expression'))
    listeNombres=retireEspaceVide(listeNombres)
    for elt in listeCoups:
        if elt[0] == data.get("Joueurs"):
            print(elt[0])
            elt.append(listeNombres)
    resultat = construitOperation(data.get("expression"))
    socketio.emit('retourCalculCL',{"expression" :resultat,"Joueurs" : data.get("Joueurs"), "listeNombres":listeNombres})

#Annule le dernier calcul intermédiaire fait et renvoie ses opérandes
@socketio.on('demandeDernierCoup')
def handle_dernierCoup(data):
    global listeCoups
    vide = False
    for elt in listeCoups:
        if elt[0] == data:
            aEnvoyer = elt.pop()
            print(aEnvoyer)
            if len(elt) == 1:
                vide = True
                socketio.emit("retourneDernierCoup",{"nom":data, "vide":vide, "tab":aEnvoyer})
            else:
                socketio.emit("retourneDernierCoup",{"nom":data, "vide":vide, "tab":aEnvoyer})

if __name__ == '__main__':
    socketio.run(app, host= '0.0.0.0', port=5000, debug=True)
