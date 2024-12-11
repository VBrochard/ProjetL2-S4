import socketio
import time
from colorama import Fore, Back, Style

sio = socketio.Client()
tirage = []
score = 0

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

print(Fore.GREEN+"*************************************************\n")
print("** Bienvenue dans le jeu du mot le plus long **\n")
print(Fore.GREEN+"*************************************************")
print(Style.RESET_ALL)
nomJoueur = input("Entrez votre nom pour rejoindre: ")


@sio.event
def connect():
    sio.emit('AnnonceJoueur',nomJoueur)
    print("Bienvenue",nomJoueur, "\n")



try:
    sio.connect('http://localhost:5000')
except Exception as e:
    print("Impossible de se connecter")

@sio.event
def Lancement(data):
    print("La partie commence !")
    print("Joueurs:")
    for joueur in data:
        print("-"+ joueur[0], "Score :",joueur[1])



@sio.event
def résultat(data):
    print("Le gagnant est :", data.get("nom"))#Nom du vainqueur
    print("Il gagne", data.get("PointGagnée"), "points","avec le mot :", data.get("MotGagnant"))#Afficher le score retourné
    print("Le meilleur mot possible était :",data.get("meilleurPossible"))
    ListeScore = data.get("ListeScore")
    for joueur in ListeScore:
        print("-"+ joueur[0], "Score :",joueur[1])
    recommencerPartie()



#@sio.event
def recommencerPartie():
    rejouer = input("Voulez-vous refaire une partie ? [y/n] : ")
    if rejouer == "n":
        print("Au revoir")
        sio.disconnect()



@sio.event
def tirageLettres(data):
    tirage = data
    affichage = ""
    for lettre in tirage:
        affichage+=lettre+" "
    print(Fore.GREEN+"Lettres disponibles:",Fore.RED+affichage)
    print(Style.RESET_ALL)
    propositionMot = input("Ecrivez votre mot grâce aux lettres du tirage: ")
    propositionMot = propositionMot.upper()
    if contientBonnesLettres(propositionMot,tirage):
        sio.emit("envoiMot",{"nom" : nomJoueur , "mot" : propositionMot})
    else:
        while contientBonnesLettres(propositionMot,tirage) == False:
            propositionMot = input("Veuillez utiliser seulement les lettres du tirage et au plus une fois chacune: ")
            propositionMot = propositionMot.upper()
        sio.emit("envoiMot",propositionMot)


sio.wait()


#METTRE UN WAIT A LAFFICHAGE DES JOUEURS

