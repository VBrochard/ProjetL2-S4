def motExiste(mot):
    with open('Ressources/Dico.txt', 'r', encoding='utf-8') as fichier:
        mots_dictionnaire = {ligne.strip().upper() for ligne in fichier}
        if mot.upper() in mots_dictionnaire:
            return True
        else:
            return False

def genererToutesLesCombis(s):
    result = []
    def permuter(prefixe, remaining):
        if prefixe:
            result.append(prefixe)
        for i in range(len(remaining)):
            permuter(prefixe + remaining[i], remaining[:i] + remaining[i+1:])
    permuter("", s)
    return result

def plusLongDansUneListe(l):
    return max(liste_mots, key=len)        

def motLePlusLong(s):
    genererToutesLesCombis(s)
    a = plusLongDansUneListe(result)
    print(f"Le mot le plus long avec ces lettres est {a}")

