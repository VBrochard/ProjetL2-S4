from itertools import combinations, permutations
from collections import defaultdict

dico = defaultdict(list)

def search_for1(letters):
    ret = []
    for sz in range(len(letters), 0, -1):
        for _letters in combinations(letters, sz):
            key = ''.join(sorted(_letters))
            if key in dico:
                ret += dico[key]
        if ret != []:
            return sz, list(set(ret))
    return 0, []

def search_for2(letters):
    letters = sorted(letters)
    d = defaultdict(list)
    for key in dico.keys():
        i, j = 0, 0
        while j < len(key) and i < len(letters):
            if key[j] != letters[i]:
                i += 1
            else:
                i += 1
                j += 1
        if j == len(key):
            d[len(key)].extend(dico[key])
    best_len = max(d.keys())
    return best_len, d[best_len]

def search_for(letters):
    if 2 ** len(letters) > len(dico):
        return search_for2(letters)
    else:
        return search_for1(letters)

def load_dictionary():
    infile = open('Ressources/Dico.txt', 'r')
    wc = 0
    while True:
        line = infile.readline()
        if line == str(): break
        wc += 1
        line = line.strip('\n')
        key = ''.join(sorted(line)).replace('-', '')
        dico[key].append(line)
    infile.close()


def motLePlusLong(letters):
    sz, lst = search_for(letters)
    if lst:
        return max(lst, key=len)
    else:
        return None

load_dictionary() 

def motExiste(mot):
    key = ''.join(sorted(mot))
    return key in dico

def motLePlusLongAvecPrefixeContenu(prefix, listeCaracateres):
    prefix = prefix.upper() 
    caracteres = ''.join(listeCaracateres).upper()  
    prefix_len = len(prefix)
    max_mot = ""
    lettres_restantes = ''.join(sorted(caracteres))

    for key, mots in dico.items():
        for mot in mots:
            if len(mot) >= prefix_len and prefix in mot:
                temp_caract = lettres_restantes
                possible = True
                for lettre in mot:
                    if lettre in temp_caract:
                        temp_caract = temp_caract.replace(lettre, '', 1)
                    else:
                        possible = False
                        break
                if possible and len(mot) > len(max_mot):
                    max_mot = mot
    return max_mot

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

def rempliVertical(grille, mot, a, b):
    for i, lettre in enumerate(mot):
        ligne = a + i
        if ligne < len(grille): 
            grille[ligne][b] = f"'{lettre}'"

def rempliVertical2(grille, mot, a, b):
    if(a<0):
        for j in range(-a):
            creerUneListeEnPlusEnHaut(grille)
        rempliVertical(grille, mot, 0, b)
    if(len(mot)> len(grille)-a):
        for m in range(len(mot) - (len(grille) - a)):
            creerUneListeEnPlusEnBas(grille)
        rempliVertical(grille, mot, a, b)

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

def motMaxx(lettre, listeDeLettres):
    s = ''.join(listeDeLettres)
    b = lettre + s
    return motLePlusLong(b)

def lettresDispo(grille):
    disponible = []
    lignes = len(grille)
    colonnes = len(grille[0]) if lignes > 0 else 0
    
    # Parcourir chaque case de la grille
    for i in range(lignes):
        for j in range(colonnes):
            if grille[i][j] != "'.'":  # Si la case contient une lettre
                voisins = 0
                # Vérification des voisins dans les directions haut, bas, gauche, droite
                voisin_haut = i > 0 and grille[i-1][j] != "'.'"
                voisin_bas = i < lignes - 1 and grille[i+1][j] != "'.'"
                voisin_gauche = j > 0 and grille[i][j-1] != "'.'"
                voisin_droite = j < colonnes - 1 and grille[i][j+1] != "'.'"
                
                # Vérification des voisins diagonaux
                voisin_haut_gauche = i > 0 and j > 0 and grille[i-1][j-1] != "'.'"
                voisin_haut_droite = i > 0 and j < colonnes - 1 and grille[i-1][j+1] != "'.'"
                voisin_bas_gauche = i < lignes - 1 and j > 0 and grille[i+1][j-1] != "'.'"
                voisin_bas_droite = i < lignes - 1 and j < colonnes - 1 and grille[i+1][j+1] != "'.'"
                
                # Comptabilisation des voisins
                if voisin_haut:
                    voisins += 1
                if voisin_bas:
                    voisins += 1
                if voisin_gauche:
                    voisins += 1
                if voisin_droite:
                    voisins += 1
                if voisin_haut_gauche:
                    voisins += 1
                if voisin_haut_droite:
                    voisins += 1
                if voisin_bas_gauche:
                    voisins += 1
                if voisin_bas_droite:
                    voisins += 1
                
                # Condition 1 : Si la lettre a un seul voisin
                if voisins == 1:
                    disponible.append((grille[i][j], (i, j)))
                
                # Condition 2 : Si la lettre a exactement 2 voisins spécifiques (haut-bas ou gauche-droite ou diagonales)
                elif voisins == 2:
                    if (voisin_haut and voisin_bas) or (voisin_gauche and voisin_droite) or \
                       (voisin_haut_gauche and voisin_bas_droite) or (voisin_haut_droite and voisin_bas_gauche):
                        disponible.append((grille[i][j], (i, j)))
    
    # Afficher les lettres disponibles et leurs coordonnées
    for lettre, coord in disponible:
        print(f"Lettres disponibles : '{lettre}' à la position {coord}")
    
    return [lettre for lettre, _ in disponible]


def bananaSolveurPremierCoupage(s):
    listeLettresRestantes = list(s)
    motLong = motLePlusLong(s)
    lenHor = len(motLong)
    motMax = ""
    enleverLettresDansListeLettresRest(motLong, listeLettresRestantes)
    for lettre in motLong:
        if(len(motMaxx(lettre, listeLettresRestantes)) > len(motMax)):
            motMax = motMaxx(lettre, listeLettresRestantes)
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
    return grille


def creerUneListeEnPlusEnHaut(grille):
    lenHor = len(grille[0])
    points = []
    for i in range(lenHor):
        points.append("'.'")
    grille.insert(0, points)

def creerUneListeEnPlusEnBas(grille):
    lenHor = len(grille[0])
    points = []
    for i in range(lenHor):
        points.append("'.'")
    grille.insert(len(grille), points)


grille = bananaSolveurPremierCoupage("STAVNEQSMGUSAHCIFLIUNVMEE")
print(lettresDispo(grille))
rempliVertical2(grille, "AMENERE", 2, 0)
afficherGrille(grille)
print(lettresDispo(grille))
