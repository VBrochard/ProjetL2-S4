import socketio

sio = socketio.Client()
tirage = []


def contientBonnesLettres(mot, tirage):
    for lettre in mot:
        if lettre.upper() not in tirage:
            return False
    return True


print("***************************************\nBienvenue dans le jeu du mot le plus long\n***************************************")
nomJoueur = input("Entrez votre nom pour rejoindre: ")


@sio.event
def connect():
    sio.emit('connexionJoueur',{"nomJoueur":nomJoueur})
    print("Bienvenue",nomJoueur)

try:
    sio.connect('http://localhost:5000',transports=["websocket"])
except Exception as e:
    print("Impossible de se connecter")


sio.wait()


