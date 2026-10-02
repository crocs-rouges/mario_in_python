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

## Dépendances

- Python 3.7 ou supérieur
- Pygame
- NumPy
- Pillow

## Contenu

- `mario_in_python.py` : jeu et point d'entrée
- `images/` : sprites, blocs, décors, cartes et son
- `requirements.txt` : dépendances Python
- `mario in python.sln` et `mario in python.pyproj` : solution Visual Studio

Les anciens scripts de sauvegarde et résultats générés ne sont pas nécessaires
au lancement du jeu.
