# Projet Mini-Jeux — L2 Informatique (Groupe 22)

Site web de mini-jeux de lettres et de chiffres, inspiré de l'émission *Des Chiffres et des Lettres*. Projet de fin de Licence 2.

## Lancement

```bash
python server.py <nb_joueurs> <taille_deck>
```

Puis ouvrir `http://127.0.0.1:5000/` dans le navigateur.

**Exemple :** `python server.py 2 9` — 2 joueurs, deck de 9 lettres.

Un client terminal alternatif est aussi disponible pour le mode "Le mot le plus long" :
```bash
python client.py
```

## Stack technique

| Composant | Technologie |
|-----------|-------------|
| Serveur | Python + Flask |
| Temps réel | Flask-SocketIO |
| Frontend | HTML / CSS vanilla + JavaScript |
| Dictionnaire | Fichier `Dico.txt` (~130 000 mots) |

## Jeux disponibles

### Des Chiffres et des Lettres
Mode complet qui enchaîne les deux épreuves ci-dessous sur plusieurs rounds.

### Le Mot le Plus Long
Les joueurs choisissent à tour de rôle des voyelles ou des consonnes pour constituer un tirage commun. Chacun a 30 secondes pour trouver le mot le plus long possible avec ces lettres. Le serveur valide les mots, calcule le meilleur mot possible et attribue les points. Un système d'**indices** (longueur, nature, première lettre, définition) est disponible contre une pénalité de score.

### Le Compte est Bon
Un tirage de 6 nombres et un objectif entre 101 et 999 sont générés aléatoirement. Les joueurs soumettent une expression arithmétique en utilisant les nombres du tirage. Le plus proche de l'objectif remporte le tour.

### BananaGramms
Variantes du jeu *Bananagrams* — placer des tuiles de lettres pour former un réseau de mots croisés valide.

- **Banana Solitaire** — mode solo, le joueur pioche ses lettres et construit sa grille à son rythme.
- **Banana Speed** — mode 2 joueurs, chacun choisit une difficulté et le premier à valider sa grille gagne.

### Opti'Mot
Mode multijoueur : chaque joueur reçoit une main de 10 lettres et un deck commun de 5 lettres. Les joueurs posent leurs lettres sur une grille partagée pour former des mots valides.

### Banana Solver
Outil utilitaire : à partir d'une chaîne de lettres, il génère automatiquement une grille de mots croisés valide en utilisant un algorithme glouton (DFS sur les lettres disponibles en bordure de grille).

```bash
# Exemple intégré dans bananaSolver.py
bananaSolver("STAVNEQSMGUSAHCIFLIUNVMEE")
```

## Structure du projet

```
projet/
├── server.py                  # Serveur Flask-SocketIO (toute la logique métier)
├── client.py                  # Client terminal pour "Le mot le plus long"
├── templates/
│   ├── index.html             # Menu principal
│   ├── menu_chiffre_lettre.html
│   ├── chiffre_lettre.html
│   ├── le_plus_long.html
│   ├── le_compte_est_bon.html
│   ├── BananaGramms.html
│   ├── banana_solitaire.html
│   ├── banana_speed.html
│   └── OptiMot.html
├── bananaSolver/
│   └── bananaSolver.py        # Algorithme de résolution automatique
├── Ressources/
│   └── Dico.txt               # Dictionnaire français
└── testFonctions.py
```

# Faiblesses
Quelque faiblesses : 
    - BananaSolver fonctionne totalement jusqu'a 60 lettres, comportement aléatoire avec plus.
    - Le client CLI a quelque soucis de synchronisation mais est fonctionnel.
    - Opti mot et les bananas sont assez bancales, la personne devant la developper ayant abbandonnée tôt le projet.

