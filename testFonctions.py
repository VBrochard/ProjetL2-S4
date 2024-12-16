from random import *
from itertools import permutations
import time

def ouvrirDico():
    with open("Ressources/Dico.txt", 'r', encoding='utf-8') as fichier:
        return {ligne.strip().upper() for ligne in fichier}

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

lettres_freq_lplm = {"A": 9, "B": 2, "C": 2, "D":3, "E":15, "F":2, "G": 2, "H": 2, "I":8,"J":1, "K":1, "L":5, "M":3, "N":6, "O":6, "P":2, "Q":1, "R":6, "S":6, "T":6, "U":6,
"V": 2, "W": 1, "X": 1, "Z": 2}

lettres_freq_opti = {"A": 5, "B": 1, "C": 2, "D":2, "E":9, "F":2, "G": 1, "H": 1, "I":5,"J":1, "K":1, "L":3, "M":3, "N":3, "O":3, "P":2, "Q":1, "R":3, "S":4, "T":3, "U":3,
"V": 2, "W": 1, "X": 1, "Z": 1}

cartes_freq_lplm = [carte for carte, freq in lettres_freq_lplm.items() for i in range(freq)]
cartes_freq_opti = [carte for carte, freq in lettres_freq_opti.items() for i in range(freq)]

taille_deck_lplm = 7
taille_deck_opti = 10

def sommeDesFreq(cartes):
    return len(cartes)

def eniemeCarte(n, tabCartes):
    return tabCartes[n - 1]

def genererUnDeck(cartes, taille):
    deck = []
    for i in range(taille):
        a = randint(0, sommeDesFreq(cartes))
        deck.append(eniemeCarte(a, cartes))
    return deck

voyelles_lplm = [carte for carte, freq in lettres_freq_lplm.items() if carte in "AEIOUY" for i in range(freq)]
consonnes_lplm = [carte for carte, freq in lettres_freq_lplm.items() if carte not in "AEIOUY" for i in range(freq)]
voyelles_opti = [carte for carte, freq in lettres_freq_opti.items() if carte in "AEIOUY" for i in range(freq)]
consonnes_opti = [carte for carte, freq in lettres_freq_opti.items() if carte not in "AEIOUY" for i in range(freq)]

def tirageCarteVoyelle(voyelles):
    a = randint(0, len(voyelles))
    return eniemeCarte(a, voyelles)

def tirageCarteConsonne(consonnes):
    a = randint(0, len(consonnes))
    return eniemeCarte(a, consonnes)

def retireUneVoyelle_lplm(lettre):
    voyelles_lplm.remove(lettre)

def retireUneConsonne_lplm(lettre):
    consonnes_lplm.remove(lettre)

def retireUneVoyelle_opti(lettre):
    voyelles_opti.remove(lettre)

def retireUneConsonne_opti(lettre):
    consonnes_opti.remove(lettre)

def retireDoublon(liste):
    listeRes = []
    for elt in liste:
        if elt not in listeRes:
            listeRes.append(elt)
    return listeRes

def barreChargement(secondes):
    affichage = ""
    for i in range(secondes):
        mil = i*"-"
        espace = (secondes-i)*" "
        print("|"+mil+espace+"|",end="\r")
        time.sleep(1)
    print("\nTemps écoulé")

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
