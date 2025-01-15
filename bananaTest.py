from random import *
from itertools import permutations, combinations

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
            trie.insert(ligne.strip().upper()) 
    return trie

dico = ouvrirDico()  

def motExiste(mot):
    return dico.search(mot.upper())  

def motLePlusLong(s):
    s = ''.join(sorted(s.upper(), reverse=True))  
    max_mot = ""
    def backtrack(prefix, remaining_letters):
        nonlocal max_mot
        if len(prefix) > len(max_mot) and motExiste(prefix):
            max_mot = prefix
        if not remaining_letters:
            return
        for i in range(len(remaining_letters)):
            if dico.starts_with(prefix + remaining_letters[i]):
                backtrack(prefix + remaining_letters[i], remaining_letters[:i] + remaining_letters[i+1:])
    backtrack("", s)
    return max_mot


def motLePlusLongAvecPrefixeContenu(prefix, listeCaracateres):
    prefix = prefix.upper()  
    caracteres = ''.join(listeCaracateres)
    caracteres = caracteres.upper()
    max_mot = ""
    def essayer_permutations(lettres):
        nonlocal max_mot
        unique_permutations = set(permutations(lettres))
        for perm in unique_permutations:
            mot = ''.join(perm)  
            if motExiste(mot) and prefix in mot:
                if len(mot) > len(max_mot):
                    max_mot = mot 
    essayer_permutations(prefix + caracteres)
    for i in range(1, len(caracteres) + 1): 
        for comb in combinations(caracteres, len(caracteres) - i):
            essayer_permutations(prefix + ''.join(comb)) 
    return max_mot
'''
def coupageVer(mot1, mot2):
    j = -1  
    for i in range(len(mot1)):
        if mot1[i] in mot2:
            for j in range(len(mot2)):
                if mot1[i] == mot2[j]:
                    break  
            break  
    return j

def coupageHor(mot1, mot2):
    i = -1  # Initialisation à -1 pour gérer le cas où il n'y a pas de correspondance
    for j in range(len(mot2)):  # Parcours du mot vertical (mot2)
        if mot2[j] in mot1:  # Si la lettre de mot2 se trouve dans mot1
            for k in range(len(mot1)):  # Parcours du mot horizontal (mot1)
                if mot2[j] == mot1[k]:  # Si une lettre de mot2 correspond à mot1
                    i = k  # Enregistrer la position où la coupe se produit
                    break  # Sortir de la boucle interne une fois que la coupe est trouvée
            if i != -1:  # Si la coupe a été trouvée, on sort de la boucle externe
                break
    return i
'''
def coupage(mot1, mot2, lettre):
    indice_mot1 = -1
    if lettre in mot1:
        indice_mot1 = mot1.index(lettre)
    indice_mot2 = -1
    if lettre in mot2:
        indice_mot2 = mot2.index(lettre)
    if indice_mot1 != -1 and indice_mot2 != -1:
        return (indice_mot1, indice_mot2)
    return None

print(coupage("LIANESCENTES", "LEIZ", "I"))

def rempliVertical(grille, mot, a, b):
    for i, lettre in enumerate(mot):
        ligne = a + i
        if ligne < len(grille):
            grille[ligne][b] = f"'{lettre}'"

def rempliHorizontal(grille, mot, a, b):
    for i, lettre in enumerate(mot):
        colonne = b + i  
        if colonne < len(grille[a]):  
            grille[a][colonne] = f"'{lettre}'"

def afficherGrille(grille):
    for i, liste in enumerate(grille):
        print(f"[{', '.join(liste)}]")    

def enleverLettresDansListeLettresRest(mot, liste):
    for lettre in mot:
        if lettre in liste:
            liste.remove(lettre)

def bananaSolveurPremierCoupage(s):
    listeLettresRestantes = list(s)
    motLong = motLePlusLong(s)
    lenHor = len(motLong)
    motMax = ""
    enleverLettresDansListeLettresRest(motLong, listeLettresRestantes)
    for lettre in motLong:
        if(len(motLePlusLongAvecPrefixeContenu(lettre, listeLettresRestantes)) > len(motMax)):
            motMax = motLePlusLongAvecPrefixeContenu(lettre, listeLettresRestantes)
            lettreCoupe = lettre
    lenVer = len(motMax)
    enleverLettresDansListeLettresRest(motMax, listeLettresRestantes)
    coupeVer = coupage(motLong, motMax, lettreCoupe)[1]
    lenVerAv = coupeVer
    lenVerAp = lenVer - coupeVer -1
    grille = []
    coupeHor = coupage(motLong, motMax, lettreCoupe)[0]
    liste_car = [f"'{c}'" for c in motLong]
    for i in range(lenVerAv):
        grille.append([])
    grille.append(liste_car)
    for i in range(lenVerAp):
        grille.append([])
    for liste in grille:
        if(liste == []):
            for i in range(lenHor):
                liste.append("'.'")
    rempliVertical(grille, motMax, 0, coupeHor)
    afficherGrille(grille)
    print(listeLettresRestantes)


bananaSolveurPremierCoupage("MGANREELLE")
print("//////")
bananaSolveurPremierCoupage("LLEEESTINCNAZE")
print("/////")
bananaSolveurPremierCoupage("VAILLESSETUREOIZZZZZZ")

