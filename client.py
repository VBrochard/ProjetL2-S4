import socketio

sio = socketio.Client()
tirage = []


def contientBonnesLettres(mot, tirage):
    if mot == "":
        return True
        
    lettreDepart = mot[0]
    for elt in range(len(tirage)-1):
        if lettreDepart == tirage[elt]:
            tirage.pop(elt)
            return True and contientBonnesLettres(mot[1:],tirage)
    
    return False

print("***************************************\nBienvenue dans le jeu du mot le plus long\n***************************************")
print(contientBonnesLettres("AAC",["A","C","B","A"]))
nomJoueur = input("Entrez votre nom pour rejoindre: ")


@sio.event
def connect():
    sio.emit('message',nomJoueur)
    print("Bienvenue",nomJoueur)



try:
    sio.connect('http://localhost:5000')
except Exception as e:
    print("Impossible de se connecter")




#@sio.event
def tirageLettres(data):
    tirage = data
    affichage = ""
    for lettre in tirage:
        affichage+=lettre+" "
    print("Lettres disponibles:",affichage)
    propositionMot = input("Ecrivez votre mot grâce aux lettres du tirage: ")
    propositionMot = propositionMot.upper()
    if contientBonnesLettres(propositionMot,tirage):
        sio.emit("envoiMot",propositionMot)
    else:
        while contientBonnesLettres(propositionMot,tirage) == False:
            propositionMot = input("Veuillez utiliser seulement les lettres du tirage et au plus une fois chacune: ")
            propositionMot = propositionMot.upper()
        sio.emit("envoiMot",propositionMot)




sio.wait()


