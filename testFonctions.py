from random import *

def motExiste(mot):
    with open("Ressources/Dico.txt", 'r', encoding='utf-8') as fichier:
        mots_dictionnaire = {ligne.strip().upper() for ligne in fichier}
        if mot.upper() in mots_dictionnaire:
            return True
        else:
            return False

def genererToutesLesCombis(s):
    result = []
    def permuter(prefixe, remaining):
        if motExiste(prefixe):
            result.append(prefixe)
        for i in range(len(remaining)):
            permuter(prefixe + remaining[i], remaining[:i] + remaining[i+1:])
    permuter("", s)
    return result

def plusLongDansUneListe(l):
    return max(l, key=len)

def motLePlusLong(s):
    b = genererToutesLesCombis(s)
    a = plusLongDansUneListe(b)
    return f"Le mot le plus long avec ces lettres est '{a}'"

lettres_freq = {"A": 9, "B": 2, "C": 2, "D":3, "E":15, "F":2, "G": 2, "H": 2, "I":8,"J":1, "K":1, "L":5, "M":3, "N":6, "O":6, "P":2, "Q":1, "R":6, "S":6, "T":6, "U":6,
"V": 2, "W": 1, "X": 1, "Z": 2}

cartes_freq = [carte for carte, freq in lettres_freq.items() for _ in range(freq)]

taille_deck = 7

def sommeDesFreq():
    b = 0
    for lettre, freq in lettres_freq.items():
        b+= freq
    return b

def eniemeCarte(n):
    return cartes_freq[n - 1]

def genererUnDeck():
    deck = []
    for i in range(taille_deck):
        a = randint(0, sommeDesFreq())
        deck.append(eniemeCarte(a))
    return deck

print(genererUnDeck())

print(motLePlusLong("abc"))