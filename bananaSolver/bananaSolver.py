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
    infile = open('Dico.txt', 'r')
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
    mot = mot.upper()
    key = ''.join(sorted(mot))
    return key in dico

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

def remplirVertical(grille, mot, a, b):
    for i, lettre in enumerate(mot):
        ligne = a + i
        if ligne < len(grille): 
            grille[ligne][b] = f"'{lettre}'"

def remplirVertical2(grille, mot, ligne, colonne):
    if(ligne<0):
        for j in range(-ligne):
            creerUneListeEnPlusEnHaut(grille)
        remplirVertical(grille, mot, 0, colonne)
    elif(len(mot)> len(grille)-ligne):
        for m in range(len(mot) - (len(grille) - ligne)):
            creerUneListeEnPlusEnBas(grille)
        remplirVertical(grille, mot, ligne, colonne)
    else:
        remplirVertical(grille, mot, ligne, colonne)

def remplirHorizontal(grille, mot, a, b):
    for i, lettre in enumerate(mot):
        colonne = b + i  
        if colonne < len(grille[a]):  
            grille[a][colonne] = f"'{lettre}'"

def remplirHorizontal2(grille, mot, ligne, colonne):
    if(colonne < 0):
        for i in range(-colonne):
            creerUneColoneAGauche(grille)
        remplirHorizontal(grille, mot, ligne, 0) 
    elif(len(mot) > len(grille[0]) - colonne):
        for m in range(len(mot) - (len(grille[0]) - colonne)):
            creerUneColonneADroite(grille)
        remplirHorizontal(grille, mot, ligne, colonne)
    else:
        remplirHorizontal(grille, mot, ligne, colonne)
    
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

def lettresDispoCoord(grille):
    disponible = []
    lignes = len(grille)
    colonnes = len(grille[0]) if lignes > 0 else 0
    for i in range(lignes):
        for j in range(colonnes):
            if grille[i][j] != "'.'": 
                voisins = 0
                voisin_haut = i > 0 and grille[i-1][j] != "'.'"
                voisin_bas = i < lignes - 1 and grille[i+1][j] != "'.'"
                voisin_gauche = j > 0 and grille[i][j-1] != "'.'"
                voisin_droite = j < colonnes - 1 and grille[i][j+1] != "'.'"
                voisin_haut_gauche = i > 0 and j > 0 and grille[i-1][j-1] != "'.'"
                voisin_haut_droite = i > 0 and j < colonnes - 1 and grille[i-1][j+1] != "'.'"
                voisin_bas_gauche = i < lignes - 1 and j > 0 and grille[i+1][j-1] != "'.'"
                voisin_bas_droite = i < lignes - 1 and j < colonnes - 1 and grille[i+1][j+1] != "'.'"
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
                if voisins == 1:
                    disponible.append((grille[i][j], (i, j)))
                elif voisins == 2:
                    if (voisin_haut and voisin_bas) or (voisin_gauche and voisin_droite) or \
                    (voisin_haut_gauche and voisin_bas_droite) or (voisin_haut_droite and voisin_bas_gauche):
                        disponible.append((grille[i][j], (i, j)))
    return enlever_apostrophes2(disponible)

def lettresDispo(grille):
    disponible = []
    lignes = len(grille)
    colonnes = len(grille[0]) if lignes > 0 else 0
    for i in range(lignes):
        for j in range(colonnes):
            if grille[i][j] != "'.'":  
                voisins = 0
                voisin_haut = i > 0 and grille[i-1][j] != "'.'"
                voisin_bas = i < lignes - 1 and grille[i+1][j] != "'.'"
                voisin_gauche = j > 0 and grille[i][j-1] != "'.'"
                voisin_droite = j < colonnes - 1 and grille[i][j+1] != "'.'"
                voisin_haut_gauche = i > 0 and j > 0 and grille[i-1][j-1] != "'.'"
                voisin_haut_droite = i > 0 and j < colonnes - 1 and grille[i-1][j+1] != "'.'"
                voisin_bas_gauche = i < lignes - 1 and j > 0 and grille[i+1][j-1] != "'.'"
                voisin_bas_droite = i < lignes - 1 and j < colonnes - 1 and grille[i+1][j+1] != "'.'"
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
                if voisins == 1:
                    disponible.append(grille[i][j])
                elif voisins == 2:
                    if (voisin_haut and voisin_bas) or (voisin_gauche and voisin_droite) or \
                    (voisin_haut_gauche and voisin_bas_droite) or (voisin_haut_droite and voisin_bas_gauche):
                        disponible.append(grille[i][j])
    return enlever_apostrophes(disponible)

def enlever_apostrophes(liste):
    return [lettre.replace("'", "") for lettre in liste]

def enlever_apostrophes2(liste):
    return [(lettre.replace("'", ""), coord) for lettre, coord in liste]

def appartientAUnMotHor(grille, ligne, colonne):
    if colonne > 0 and colonne < len(grille[0]) - 1:  
        if grille[ligne][colonne - 1] != "'.'" or grille[ligne][colonne + 1] != "'.'":
            return True
    return False

def appartientAUnMotVer(grille, ligne, colonne):
    if ligne > 0 and ligne < len(grille) - 1:  
        if grille[ligne - 1][colonne] != "'.'" or grille[ligne + 1][colonne] != "'.'":
            return True
    return False

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

def creerUneColoneAGauche(grille):
    for liste in grille:
        liste.insert(0, "'.'")

def creerUneColonneADroite(grille):
    for liste in grille:
        liste.insert(len(grille[0]), "'.'")

def coupage2(lettre, mot):
    return mot.find(lettre)

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
    remplirVertical(grille, motMax, 0, coupeHor)
    return [grille, listeLettresRestantes]

def bananaSolver(s):
    print("Construction en cours ! \n")
    grille, listeLettresRestantes = bananaSolveurPremierCoupage(s)
    compteur = 0
    while(len(listeLettresRestantes) != 0 and compteur < 1000):
        listeLettresDispoCoord = lettresDispoCoord(grille)
        motMax = ""
        for lettre, coord in listeLettresDispoCoord:
            compteur +=1
            if(appartientAUnMotHor(grille, coord[0], coord[1])):
                maxMot = motMaxx(lettre, listeLettresRestantes)
                if((maxMot is not None) and (len(maxMot) > len(motMax)) and (lettre in maxMot)):
                    motMax = maxMot
                    coupe = coord[0] - coupage2(lettre, motMax)
                    d = [lettre, coord, motMax, "ver", coupe]
            elif(appartientAUnMotVer(grille, coord[0], coord[1])):
                maxMot = motMaxx(lettre, listeLettresRestantes)
                if((maxMot is not None) and (len(maxMot) > len(motMax)) and (lettre in maxMot)):
                    motMax = maxMot
                    coupe = coord[1] - coupage2(lettre, motMax)
                    d = [lettre, coord, motMax, "hor", coupe]
        if(d[3] == "ver"):
            remplirVertical2(grille, d[2], coupe, d[1][1])
            enleverLettresDansListeLettresRest(d[2], listeLettresRestantes)
        elif(d[3] == "hor"):
            remplirHorizontal2(grille, d[2], d[1][0], d[4])
            enleverLettresDansListeLettresRest(d[2], listeLettresRestantes)  
    afficherGrille(grille)
    return grille


bananaSolver("STAVNEQSMGUSAHCIFLIUNVMEE")