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
    
    return f"Le mot le plus long avec ces lettres est '{max_mot}'"



lettres_freq = {"A": 9, "B": 2, "C": 2, "D":3, "E":15, "F":2, "G": 2, "H": 2, "I":8,"J":1, "K":1, "L":5, "M":3, "N":6, "O":6, "P":2, "Q":1, "R":6, "S":6, "T":6, "U":6,
"V": 2, "W": 1, "X": 1, "Z": 2}

cartes_freq = [carte for carte, freq in lettres_freq.items() for i in range(freq)]

taille_deck = 7

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

import sys, select

print ("You have ten seconds to answer!")

i, o, e = select.select( [sys.stdin], [], [], 10 )

if (i):
  print ("You said", sys.stdin.readline().strip())
else:
  print ("You said nothing!")