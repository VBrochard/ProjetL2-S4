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
    print(Fore.GREEN+"--------------------------------------------------------------------------")
    print(Style.RESET_ALL)
    print("Joueurs:")
    for joueur in data:
        print("-"+ joueur[0], "Score :",joueur[1])
    time.sleep(2)


@sio.event
def résultat(data):
    
    print("Le gagnant est :", data.get("nom"))#Nom du vainqueur
    print("Il gagne", data.get("PointGagnée"), "points","avec le mot :", data.get("MotGagnant"))#Afficher le score retourné
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
    pret = input("Appuyer sur entrée pour le prochain tour")
    sio.emit('nouveauTour')



#@sio.event
def recommencerPartie():
    rejouer = input("Voulez-vous refaire une partie ? [y/n] : ")
    if rejouer == "n":
        print("Au revoir")
        sio.disconnect()
    
@sio.event
def choixLettre(data):
    
    if data == nomJoueur:
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
        



@sio.event
def tirageLettres(data):
    tirage = data.get("deck")
    affichage = ""
    for lettre in tirage:
        affichage+=lettre+" "

    if data.get("TokenComplet") == 0:
        print(Fore.GREEN+"--------------------------------------------------------------------------")
        print(Style.RESET_ALL)
        print(Fore.GREEN+"Lettres disponibles:",Fore.CYAN+affichage,end="\r")
        print(Style.RESET_ALL)
        
    if data.get("TokenComplet") == 1:
        propositionMot = input("Ecrivez votre mot grâce aux lettres du tirage: ")
        propositionMot = propositionMot.upper()
        if contientBonnesLettres(propositionMot,tirage):
            sio.emit("envoiMot",{"nom" : nomJoueur , "mot" : propositionMot})
        else:
            while contientBonnesLettres(propositionMot,tirage) == False:
                propositionMot = input("Veuillez utiliser seulement les lettres du tirage et au plus une fois chacune: ")
                propositionMot = propositionMot.upper()
            sio.emit("envoiMot",{"nom" : nomJoueur , "mot" : propositionMot})

@sio.event
def victoire(data):
    if len(data.get("nomsVainqueurs"))>1:
        print("Les vainqueurs sont",data.get("nomsVainqueurs"))
    else:
        print("Le vainqueur est",data.get("nomsVainqueurs"))
    recommencerPartie()


sio.wait()


#METTRE UN WAIT A LAFFICHAGE DES JOUEURS

