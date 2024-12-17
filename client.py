import socketio
import time
import sys , select
import os
from colorama import Fore, Back, Style

sio = socketio.Client()
tirage = []
score = 0
tempsTour = 30

def supprimeUneOcuurence(elt, liste):
    for i in range(len(liste)):
        if liste[i] == elt:
            liste.pop(i)
            return liste
    

def contientBonnesLettres(mot, tirage):
    for lettre in mot:
        if lettre in tirage:
            tirage = supprimeUneOcuurence(lettre,tirage)
        else:
            return False
    return True


def affichageListe(liste):
    result = ""
    if len(liste) == 1:
        return liste[0]
    else:
        for i in range(len(liste)):
            if i == len(liste)-2:
                result += str(liste[i]) +" et "
            elif i<len(liste)-1:
                result += str(liste[i])+", "
            else:
                result += str(liste[i])
    return result



print(Fore.GREEN+"*************************************************\n")
print("** Bienvenue dans le jeu du mot le plus long **\n")
print(Fore.GREEN+"*************************************************")
print(Style.RESET_ALL)
nomJoueur = input("Entrez votre nom pour rejoindre: ")


@sio.event
def connect():
    sio.emit('AnnonceJoueur',nomJoueur)
    print("Bienvenue",nomJoueur, "\n")
    

@sio.event
def ListePresence(data):
    listeJoueurs = data
    if len(listeJoueurs)==2 and listeJoueurs[0][0] == nomJoueur:
        print("Vous êtes le maître du jeu, appuyez sur Entrée pour commencer la partie.")
        i,o,e = select.select([sys.stdin],[],[])
        if i:
            sys.stdin = sys.__stdin__
            sio.emit('Declancheur')

    elif listeJoueurs[0][0] != nomJoueur:
        print(listeJoueurs[0][0],"est le maître du jeu, il peur démarrer la partie à tout moment",end="\r")
   

try:
    sio.connect('http://localhost:5000')
except Exception as e:
    print("Impossible de se connecter")

@sio.event
def Lancement(data):
    print("La partie commence !")
    print(Fore.GREEN+"--------------------------------------------------------------------------")
    print(Style.RESET_ALL)
    print("Joueurs:")
    for joueur in data:
        print("-"+ joueur[0], "Score :",joueur[1])
    time.sleep(0.5)
    


@sio.event
def résultat(data):
    
    if len(data.get("nom")) == 0:
        print("Personne n'a marqué de points ce tour")

    else:
        print("Le(s) gagnant(s) de ce tour sont :", affichageListe(data.get("nom")))#Nom du vainqueur
        print("Il(s) gagne(nt)", data.get("PointGagnée"), "points","avec le(s) mot :", affichageListe(data.get("MotGagnant")))#Afficher le score retourné
        print(Fore.GREEN+"--------------------------------------------------------------------------")
        print(Style.RESET_ALL)

    print("Le meilleur mot possible était :",data.get("meilleurPossible"))
    print(Fore.GREEN+"--------------------------------------------------------------------------")
    print(Style.RESET_ALL)

    ListeScore = data.get("ListeScore")
    for joueur in ListeScore:
        print("-"+ joueur[0], "Score :",joueur[1])
    print(Fore.GREEN+"--------------------------------------------------------------------------")
    print(Style.RESET_ALL)
    pretProchainTour = input("Appuyer sur entrée pour le prochain tour")
    sio.emit('nouveauTour')
    
    
@sio.event
def choixLettre(data):
    time.sleep(0.5)
    tirage = data.get("deck")
    affichage = ""
    
    for lettre in tirage:
        affichage+=lettre+" "

    if len(tirage)>0:
        print(Fore.GREEN+"--------------------------------------------------------------------------")
        print(Style.RESET_ALL)
        print(Fore.GREEN+"Lettres disponibles:",Fore.CYAN+affichage)
        print(Style.RESET_ALL)

    if data.get("joueur") == nomJoueur:
        print(choixLettre)
        choixLettre = input("Voyelles ou consonnes ?[v/c]")
        if choixLettre == "v":
            sio.emit('voyelle')
            
        elif choixLettre == "c":
            sio.emit('consonne')

        else:
            while choixLettre != "v" and choixLettre != "c":
                choixLettre = input("Ecrivez v pour une voyelle ou c pour une consonne")
                if choixLettre == "v":
                    sio.emit('voyelle')
                elif choixLettre == "c":
                    sio.emit('consonne')
        choixLettre = ""
    else:
        print("En attente du choix de",data.get("joueur"))



@sio.event
def tirageLettres(data):
    tirage = data.get("deck")
    affichage = ""
    for lettre in tirage:
        affichage+=lettre+" "

    print(Fore.GREEN+"--------------------------------------------------------------------------")
    print(Style.RESET_ALL)
    print(Fore.GREEN+"Lettres finales:",Fore.CYAN+affichage)
    print(Style.RESET_ALL)
    time.sleep(0.1) 
    print("Vous avez 20s pour écrire votre mot: ")
    i, o, e = select.select([sys.stdin],[],[],tempsTour)
    if i:
        propositionMot = sys.stdin.readline().strip()
        propositionMot = propositionMot.upper()

    else:
        print("Vous n'avez pas répondu à temps.")
        propositionMot = ""

    if contientBonnesLettres(propositionMot,tirage):
        sio.emit("envoiMot",{"nom" : nomJoueur , "mot" : propositionMot})
        print("Mot envoyé !")
        
    else:
        while contientBonnesLettres(propositionMot,tirage) == False:
            print("Veuillez utiliser seulement les lettres du tirage et au plus une fois chacune: ")
            if i:
        
                propositionMot = sys.stdin.readline().strip()
                propositionMot = propositionMot.upper()
            else:
                print("Vous n'avez pas répondu à temps.")
                propositionMot = ""
            
        sio.emit("envoiMot",{"nom" : nomJoueur , "mot" : propositionMot})
        print("Mot envoyé !")


@sio.event
def victoire(data):
    vainqueurs = affichageListe(data.get("nomsVainqueurs"))
    if len(data.get("nomsVainqueurs"))>1:
        print("Les vainqueurs sont",vainqueurs)
    else:
        print("Le vainqueur est",vainqueurs)
    recommencerPartie()


sio.wait()

