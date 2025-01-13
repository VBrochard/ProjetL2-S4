from random import *
from itertools import permutations

lettres_regime = {"A": 14, "B": 3, "C": 4, "D":4, "E":21, "F":3, "G": 2, "H": 2, "I":12,"J":1, "K":1, "L":7, "M":4, "N":9, "O":9, "P":3, "Q":1, "R":9, "S":9, "T":9, "U":9,
"V": 3, "W": 1, "X": 1, "Z": 2}

cartes_regime = [carte for carte, freq in lettres_regime.items() for i in range(freq)]

def sommeDesFreq(cartes):
    return len(cartes)

def genererUnDeck(cartes, nombre):
    deck = []
    for i in range(nombre):
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

def eniemeCarte(n, tabCartes):
    return tabCartes[n - 1]

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
    
    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
    
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

def ouvrirDico():
    trie = Trie()
    with open("Ressources/Dico.txt", 'r', encoding='utf-8') as fichier:
        for ligne in fichier:
            trie.insert(ligne.strip().upper())  # Ajouter chaque mot au Trie
    return trie

dico = ouvrirDico()  # Charger le Trie

def motExiste(mot):
    return dico.search(mot.upper())  # Utiliser search pour vérifier si le mot existe

def motLePlusLong(s):
    s = ''.join(sorted(s.upper(), reverse=True))  # Trier les lettres par ordre décroissant
    max_mot = ""

    def backtrack(prefix, remaining_letters):
        nonlocal max_mot
        # Si un mot valide est trouvé et est plus long que le précédent
        if len(prefix) > len(max_mot) and motExiste(prefix):
            max_mot = prefix
        
        # Si plus de lettres à traiter, on arrête
        if not remaining_letters:
            return
        
        for i in range(len(remaining_letters)):
            # Si ajouter cette lettre ne crée pas une chaîne invalide
            if dico.starts_with(prefix + remaining_letters[i]):
                # Recurse avec cette lettre ajoutée à prefix
                backtrack(prefix + remaining_letters[i], remaining_letters[:i] + remaining_letters[i+1:])
    
    # Démarrer le backtracking avec une chaîne vide et toutes les lettres
    backtrack("", s)

    return max_mot



def solvHonrizontal(motLong, listeLettresRestantes):
    if(len(listeLettresRestantes) != 0):
        for i in range(len(motLong)):
            if(motLong[i] in listeLettresRestantes):
                listeLettresRestantes.append(motLong[i])
                a = ''.join(listeLettresRestantes)
                b = motLePlusLong(a)
    return b
                
def coupage(motLong, a):
    for i in range(len(motLong)):
        if(motLong[i] in a):
            for j in range(len(a)):
                if motLong[i] == a[j]:
                    nb = j
                    break
    return j

print(coupage("menir", "veroler"))


print(solvHonrizontal("menir", ["r","o", "l","e", "v"]))

lplm = "MENIR"
tirage = ["R","O","L","E","V"]
deuxMot = solvHonrizontal(lplm, tirage)
lenHor = len(lplm)
coupe = coupage(lplm, deuxMot)
lenVerAv = coupe - 1
lenVerAp = len(deuxMot) - coupe
grille = []
liste_caracteres = liste_caracteres = [f"'{c}'" for c in lplm]

for i in range(lenVerAv):
    grille.append([])
grille.append(liste_caracteres)
for i in range(lenVerAp):
    grille.append([])
for liste in grille:
    if(liste == []):
        for i in range(lenHor):
            liste.append("'.'")
for i, liste in enumerate(grille):
    print(f"[{', '.join(liste)}]")

