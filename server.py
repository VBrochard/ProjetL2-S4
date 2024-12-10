def motExiste(mot):
    with open('Ressources/Dico.txt', 'r', encoding='utf-8') as fichier:
        mots_dictionnaire = {ligne.strip().upper() for ligne in fichier}
        if mot.upper() in mots_dictionnaire:
            return True
        else:
            return False

mot = "marcreghons"
if motExiste(mot):
    print(f"Le mot '{mot}' appartient au dictionnaire.")
else:
    print(f"Le mot '{mot}' n'appartient pas au dictionnaire.")