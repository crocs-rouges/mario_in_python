# Jeu de plateforme en Python

## Lancer le jeu

Depuis ce dossier, installez les dépendances puis lancez le point d'entrée :

```powershell
python -m pip install -r requirements.txt
python mario_in_python.py
```

Le jeu charge ses ressources dans `images/`, à côté du script. Les chemins sont
résolus à partir de l'emplacement du script : il peut donc être lancé depuis un
autre dossier.

Le code est organisé dans `game/` et les tests dans `tests/`. Le fichier
`mario_in_python.py` à la racine reste le lanceur du jeu.

Le jeu commence directement au premier niveau. Atteins le drapeau pour passer
automatiquement au niveau suivant ; après le dernier niveau, appuie sur `R`
pour recommencer ou sur `Échap` pour quitter.

## Dépendances

- Python 3.7 ou supérieur
- Pygame
- NumPy
- Pillow

## Contenu

- `mario_in_python.py` : lanceur du jeu
- `game/main.py` : initialisation et boucle principale
- `game/player.py` : déplacements, sauts, gravité et animation de Mario
- `game/enemies.py` : déplacement et collisions des Goombas et Koopas
- `game/progression.py` : progression linéaire des niveaux et fin de partie
- `tests/` : tests unitaires du joueur et des ennemis
- `images/` : sprites, blocs, décors, cartes et son
- `requirements.txt` : dépendances Python
- `mario in python.sln` et `mario in python.pyproj` : solution Visual Studio

Les anciens scripts de sauvegarde et résultats générés ne sont pas nécessaires
au lancement du jeu.

## Tests

Lancez les tests avec la bibliothèque intégrée à Python :

```powershell
python -m unittest discover -v
```
