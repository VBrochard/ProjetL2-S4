from random import *
from itertools import permutations
import time
import requests
from bs4 import BeautifulSoup
import re
import math
import random

def ouvrirDico():
    with open("Ressources/Dico.txt", 'r', encoding='utf-8') as fichier:
        return {ligne.strip().upper() for ligne in fichier}

dico = ouvrirDico()


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


def sommeDesFreq(cartes):
    return len(cartes)

def eniemeCarte(n, tabCartes):
    return tabCartes[n - 1]

def motMax(listeMots):
    mots_valides = [mot for mot in listeMots if motExiste(mot)]
    return len(max(mots_valides, key=len))

lettres_points_1 = ["A","E","I","L","N","O","R","S","T","U"]
lettres_points_2 = ["D","G","M"]
lettres_points_3 = ["B","C","P"]
lettres_points_4 = ["F","H","V"]
lettres_points_8 = ["J","Q"]
lettres_points_10 = ["K","W","X","Y","Z"]

def calculScore(mot):
    score =0
    motUp = mot.upper()
    for lettre in motUp:
        if lettre in lettres_points_1:
            score +=1
        if lettre in lettres_points_2:
            score +=2
        if lettre in lettres_points_3:
            score +=3
        if lettre in lettres_points_4:
            score +=4
        if lettre in lettres_points_8:
            score +=8
        if lettre in lettres_points_10:
            score +=10
    return score

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



#NE PAS TOUCHER 
'''
if len(listeJoueurs) == 2:
        print("Entrez y pour démarrer la partie")
        while True:
            demarrer = inputNonBloquant()
            if demarrer == "y":
                sys.stdin = sys.__stdin__
                sio.emit('Declancheur')
                break
    elif len(listeJoueurs) > 2 and nomJoueur == listeJoueurs[len(listeJoueurs)-1]:
        print("Entrez y pour démarrer la partie")
        while True:
            demarrer = inputNonBloquant()
            if demarrer == "y":
                sys.stdin = sys.__stdin__
                sio.emit('Declancheur')
                break
'''

def motMax(listeMots):
    motsValides = [mot for mot in listeMots if motExiste(mot)]
    return len(max(motsValides, key=len))


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
            

    
      
def construitMotsHorizontaux(listeIndices):
    listeIndices.sort()
    listeTemp = []
    res = []
    for elt in listeIndices:
        if elt+1 in listeIndices:
            listeTemp.append(elt)
        else:
            listeTemp.append(elt)
            if len(listeTemp) > 1:
                res.append(listeTemp)
            listeTemp = []
    return res
        
def construitMotsVerticaux(listeIndices):
    listeIndices.sort()
    i = 0
    res = []
    dejaVu = []
    while i < len(listeIndices):
        aVisiter = listeIndices[i]
        dejaVu.append(aVisiter)
        listeTemp = []
        
        while (aVisiter in listeIndices) and (aVisiter+32 not in dejaVu):
            listeTemp.append(aVisiter)
            aVisiter += 32
            dejaVu.append(aVisiter)
            
        if len(listeTemp) > 1:
            res.append(listeTemp)

        i+=1

    return res

def voisins(point):
    return [point+1,point-1,point+32,point-32]

def parcours(pointDepart,tab):
    aTraiter = []
    chemin = []
    aTraiter.append(pointDepart)
    while len(aTraiter) > 0:
        elt = aTraiter.pop(0)
        for v in voisins(elt):
            if not(v in chemin) and v in tab:
                chemin.append(v)
                aTraiter.append(v)
    
    return chemin



def creerListeNombres():
    return [1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,25,50,75,100]

def construireMainNombres(lstNombres):
    main = []
    while len(main) < 6:
        indiceRandom = randint(0,(len(lstNombres)-1))
        main.append(lstNombres[indiceRandom])
        lstNombres.pop(indiceRandom)
    main += ["*","*","*","*","-","-","-","-","+","+","+","+","/","/","/","/"]
    return main

def construitOperation(calcul):
    return math.floor(eval(calcul))

def toutIndex(lst,cible):
    res = []
    for i in range(len(lst)):
        if lst[i] == cible:
            res.append(i)
    return res



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

print(envoiGagnants([['P2', 152], ['P1', 152]]))