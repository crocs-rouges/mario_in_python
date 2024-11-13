# les importations obligatoire pour faire marcher le projet
import pygame
from pygame import mixer
from typing import List
from PIL import Image
import numpy as np
from typing import Tuple

# Initialisation de Pygame
pygame.init()
mixer.init()
horloge = pygame.time.Clock()

#constante du projet
player=100
air=0
eau=65
e=65
sol=1
bloc=2
blocus=23
bloc_casse=22
piece=3
player_coord=0
drapeau=25
mist=333
buisson1=17
buisson2=18
buisson3=19
cloud=33
cloud1=34
cloud2=35
montabne1=73
montabne2=74
goomba=50
koopa=55
bowser= 666

#valeur non contante du projet
PV_joueur=3
intervalle=0
k_g=-1
score=0

# tous les chemins d'accès au images
background_path : str = "images/Background/"
bloc_path : str = "images/Bloc/"
ennemi_path : str = "images/Ennemi/"
mario_path : str =  "images/Mario/"
map_path : str = "images/Map/"

#ces images sont les images qui vont etre prise pour etre comparer avec l'image et générer le tableau
    #il est recommandé de prendre les images directement depuis l'image du niveau 
    # 16 pixel par 16 pixel est la taille d'une image qui va etre comparé avec le niveau
sol_comp = np.asarray(Image.open(bloc_path+'sol.png'))
blocus_comp = np.asarray(Image.open(bloc_path+'blocus.png'))
drapeau_comp = np.asarray(Image.open(bloc_path+'drapeau.png'))
air_comp = np.asarray(Image.open(bloc_path+'air.png'))
bloc_comp = np.asarray(Image.open(bloc_path+'bloc.png'))
tete_tuyau_comp = np.asarray(Image.open(bloc_path+'tete_tuyau.png'))
tuyau_comp = np.asarray(Image.open(bloc_path+'tuyau.png'))
mist_comp = np.asarray(Image.open(bloc_path+'pointmist.png'))

# image to change to generate a new 2Dlist from this image
W1_1 = np.asarray(Image.open(map_path+'SMB_NES_World_1-1_Map.png')) 


def compare_and_mark_chunks(W1_1: np.ndarray) -> np.ndarray:
    """
    Compare each 16x16 chunk of W1_1 with air_comp and mark matches in a 2D array.

    Args:
        W1_1 (np.ndarray): The larger array to be divided into chunks.
        air_comp (np.ndarray): The array to compare each chunk with.
        sol_comp (np.ndarray): The array to compare each chunk with.
        mist_comp (np.ndarray): The array to compare each chunk with.
        bloc_comp (np.ndarray): The array to compare each chunk with.
        blocus_comp (np.ndarray): The array to compare each chunk with.
        tuyau_comp (np.ndarray): The array to compare each chunk with.

    Returns:
        np.ndarray: A 2D array with different strings marking the top-left corner of matching chunks.
    """
    chunk_size = air_comp.shape  # Assumes air_comp is 16x16
    rows, cols, hu = W1_1.shape
    chunk_rows, chunk_cols, _ = chunk_size
    
    # Initialize the result array with 'e'
    result = np.full((rows, cols), 'e', dtype='<U10')

    for i in range(0, rows - chunk_rows + 1, chunk_rows):
        for j in range(0, cols - chunk_cols + 1, chunk_cols):
            chunk = W1_1[i:i + chunk_rows, j:j + chunk_cols, :]
            if np.array_equal(chunk, air_comp):
                result[i, j] = 'air'
            if np.array_equal(chunk, sol_comp):
                result[i, j] = 'sol'
            if np.array_equal(chunk, mist_comp):
                result[i, j] = 'mist'
            if np.array_equal(chunk, bloc_comp):
                result[i, j] = 'bloc'
            if np.array_equal(chunk, blocus_comp):
                result[i, j] = 'blocus'
            if np.array_equal(chunk, tuyau_comp):
                result[i, j] = 'tuyau'

    # Filter out to keep only every 16th line and every 16th column
    final_result = result[::16, ::16]
    print(result)
    return final_result

def format_result(result: np.ndarray) -> str:
    """
    Format the result array to a specific string format.

    Args:
        result (np.ndarray): The array with marked chunks.

    Returns:
        str: The formatted string representation of the array.
    """
    formatted_lines = []
    for row in result:
        formatted_row = ', '.join(row)
        formatted_lines.append(f"[{formatted_row}],")
    return '\n'.join(formatted_lines)

instance=False
if instance==True: #sert à créer un fichier texte qui contient le tableau généré à partir de l'image choisit
    if air_comp.shape != (16, 16, 4):
        raise ValueError("air_comp doit être de 16x16 pixels")
    matching = compare_and_mark_chunks(W1_1)
    matching_array = format_result(matching)
    np.set_printoptions(threshold=np.inf)
    np.save('resultats.npy', matching_array)
    resultats = np.load('resultats.npy', allow_pickle=True)
    resultats_str = np.array_str(resultats)
    # Afficher la chaîne de caractères ou l'écrire dans un fichier texte
    print(resultats_str)
    # Écrire la chaîne de caractères dans un fichier texte
    with open('resultats.txt', 'w') as f:
        f.write(resultats_str)



# Chargement des images obligatoires pour le jeu 
#images de mario avec les animations 
mario1 = pygame.transform.scale(pygame.image.load(mario_path+'mario1.png'), (30,50))
mario2 = pygame.transform.scale(pygame.image.load(mario_path+'mario2.png'), (30,50))
mario3 = pygame.transform.scale(pygame.image.load(mario_path+'mario3.png'), (30,50))
mario_saut = pygame.transform.scale(pygame.image.load(mario_path+'mario_saut.png'), (30,50))

#images pour les boss du jeu 
bowser1 = pygame.transform.scale(pygame.image.load(ennemi_path+'bowser1.gif'), (100,100))
bowser2 = pygame.transform.scale(pygame.image.load(ennemi_path+'bowser2.gif'), (100,100))
bowser3 = pygame.transform.scale(pygame.image.load(ennemi_path+'bowser3.gif'), (100,100))
bowser4 = pygame.transform.scale(pygame.image.load(ennemi_path+'bowser4.png'), (100,100))
bowser5 = pygame.transform.scale(pygame.image.load(ennemi_path+'bowser5.png'), (100,100))
bowser_atk_1 = pygame.transform.scale(pygame.image.load(ennemi_path+'bowser_atk_1.png'), (100,100))
bowser_atk_2 = pygame.transform.scale(pygame.image.load(ennemi_path+'bowser_atk_2.png'), (100,100))
bowser_atk_3 = pygame.transform.scale(pygame.image.load(ennemi_path+'bowser_atk_3.png'), (100,100))

# images pour les ennemis du jeu
goomba = pygame.transform.scale(pygame.image.load(ennemi_path+'goomba.png'), (50,50))
koopa = pygame.transform.scale(pygame.image.load(ennemi_path+'koopa.png'), (50,50))

#images pour le background du jeu
cloud= pygame.transform.scale(pygame.image.load(background_path+'cloud.png'), (64,50))
cloud1= pygame.transform.scale(pygame.image.load(background_path+'cloud1.png'), (50,50))
cloud2= pygame.transform.scale(pygame.image.load(background_path+'cloud2.png'), (50,50))

# images pour les textures de bloc des niveaux
tuyau= pygame.transform.scale(pygame.image.load(bloc_path+'tuyau.png'), (50,50))
mist = pygame.transform.scale(pygame.image.load(bloc_path+'pointmist.png'), (50,50))
bloc = pygame.transform.scale(pygame.image.load(bloc_path+'bloc.png'), (50,50))
blocus = pygame.transform.scale(pygame.image.load(bloc_path+'blocus.png'), (50,50))
sol = pygame.transform.scale(pygame.image.load(bloc_path+'sol.png'), (50,50))
air = pygame.transform.scale(pygame.image.load(bloc_path+'air.png'), (50,50))
drapeau = pygame.transform.scale(pygame.image.load(bloc_path+'drapeau.png'), (50,200))
Level_1 = pygame.transform.scale(pygame.image.load(bloc_path+'tuyau.png'), (50,50))
Level_2 = pygame.transform.scale(pygame.image.load(bloc_path+'tuyau.png'), (50,50))
piece = pygame.transform.scale(pygame.image.load(bloc_path+'piece.png'), (50,50))

coeur = pygame.transform.scale(pygame.image.load('images/coeur.png'), (50,50))


#configuration du son du jeu et des effets sonores
pygame.mixer.music.load("images/jump.mp3")
jump_sound = mixer.Sound("images/jump.mp3")
pygame.mixer.music.set_volume(0.03)


# Liste des images pour l'animation de mario
images = [mario1,mario1,mario1,mario1,mario1, mario2, mario2, mario2, mario2, mario2, mario3, mario3, mario3, mario3, mario3,mario_saut,]
nombre_images = len(images)
images_bowser = [bowser1,bowser1,bowser1,bowser1,bowser1,bowser2,bowser2,bowser2,bowser2,bowser2,bowser3,bowser3,bowser3,bowser3,bowser3,bowser4,bowser4,bowser4,bowser5,bowser5,bowser5,bowser_atk_1,bowser_atk_2,bowser_atk_3,]
compteur_images = 0
compteur_bowser = 0
compteur_images_bowser = 0

# Intervalle de temps (en millisecondes)
intervalle_temps = 1500 
TIMER_EVENT_mario = pygame.USEREVENT + 1  # Declenche l'evenement toutes les 1000 ms (1 seconde)
compteur = 1
TIMER_EVENT = pygame.USEREVENT + 1  # Declenche l'evenement toutes les 1000 ms (1 seconde)


#configuration des polices d'écriture pour pygame
font = pygame.font.Font(None, 36)  # Choisissez une police et une taille
font2 = pygame.font.Font(None, 360)  # Choisissez une police et une taille

# Configuration de la fenetre du jeu qui sera adapté à la taille de l'écran du joueur
infoObject = pygame.display.Info() #prend les infos de l'ecran
fenetre = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN) # met en tant que resolution de la fenetre celle de l'ecran de l'utilisateur
pygame.display.set_caption("mario in python tab2D") # donne le nom de la fenetre et du projet



# tout les mondes du jeu sous formes de tableau 2D
world_map=[
        [air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, ],
        [air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, ],
        [air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, ],
        [air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, ],
        [air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, ],
        [air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, ],
        [air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, ],
        [air, air, air, air, air, air, air, air, air, Level_1, air, air, air, air, air, air, air, Level_2, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, ],
        [air, air, air, air, air, air, air, sol, sol, sol, air, air, air, air, air, sol, sol, sol, air, air, air, air, sol, sol, sol, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, ],
        [air, player, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, ],
        [sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol,sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, ],
        [sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol,sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, ],
    ]# lobby du jeu pour choisir son niveau


jeu_map_update=[
        [air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air,],
        [air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air,],
        [air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air,],
        [air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air,],
        [air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air,],
        [air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air,],
        [air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air,],
        [air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air,],
        [air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air,],
        [air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air,],
        [air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air,],
        [air, air, air, air, air, air, air, air, air, air, air, air, air, air, mist, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air,],
        [air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, sol, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air,],
        [air, air, air, air, air, air, air, air, air, mist, air, mist, bloc, mist, bloc, bloc, air, air, air, sol, air, air, air, air, air, air, air, air, air, sol, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, sol, air, air, air, air, air, air, air, air, air, sol, sol, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air,],
        [air, player, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, sol, sol, sol, air, air, bowser, air, air, air, air, sol, air, air, air, air, air, air, air, air, air, air, air, goomba, air, air, air, air, sol, air, air, air, koopa, air, air, air, air, air, air, air, air, air, air, air, air, air, sol, air, air, air, air, air, air, air, air, sol, sol, air, air, air, air, air, air, air, sol, sol, sol, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, drapeau, air, air, air, air, air, air, air, air, air, air, air,],
        [sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol,sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol,sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol,], 
        [sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol,sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol,sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol,],
   ]# map 1 du jeu dans lequel le joueur se déplacera et fera ses interractions avec le monde


jeu_map_2 = [
    [air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air],
    [air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air],
    [air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, cloud1, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, cloud, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, cloud, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, cloud1, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, cloud1, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, cloud, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, cloud, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, cloud2, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air],
    [air, air, air, air, air, air, air, air, cloud, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, cloud2, air, air, air, cloud, air, air, air, air, air, air, air, cloud2, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, cloud1, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, cloud2, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, cloud, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, cloud1, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, cloud1, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air],
    [air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, cloud, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, cloud, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, cloud, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air],
    [air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, bloc, air, mist, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, mist, bloc, mist, bloc, bloc, bloc, bloc, bloc, air, air, air, bloc, bloc, bloc, mist, air, air, air, air, air, air, air, air, air, air, air, air, air, air, mist, air, air, air, air, air, air, air, air, air, air, air, bloc, bloc, bloc, air, air, air, air, bloc, mist, mist, bloc, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, blocus, blocus, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air],
    [air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, bloc, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, bloc, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, blocus, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, blocus, blocus, blocus, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air],
    [air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, bloc, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, bloc, air, air, air, air, air, mist, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, blocus, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, blocus, blocus, air, blocus, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, blocus, blocus, blocus, blocus, blocus, blocus, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air],
    [air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, mist, air, air, air, bloc, mist, bloc, mist, bloc, air, air, air, air, blocus, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, tuyau, tuyau, air, air, air, air, air, air, air, air, bloc, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, bloc, mist, bloc, air, air, air, air, air, air, air, air, air, air, air, air, air, air, blocus, air, air, air, air, air, bloc, mist, air, air, air, air, mist, air, air, mist, air, air, mist, air, air, air, air, air, bloc, air, air, air, air, air, air, air, air, air, air, bloc, bloc, air, air, air, air, air, blocus, blocus, air, air, blocus, air, air, air, air, air, air, air, air, air, blocus, blocus, blocus, air, air, blocus, blocus, air, air, air, air, air, air, air, air, air, air, air, bloc, bloc, mist, bloc, air, air, air, air, air, air, air, air, air, air, air, blocus, blocus, blocus, blocus, blocus, blocus, blocus, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air],
    [air, player, air, air, air, air, air, air, air, air, air, air, air, air, goomba, air, air, air, air, air, koopa, air, air, air, air, goomba, blocus, blocus, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, tuyau, air, air, koopa, tuyau, tuyau, air, air, goomba, air, air, air, air, air, air, air, air, air, air, air, air, air, sol, sol, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, blocus, blocus, blocus, blocus, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, blocus, blocus, blocus, blocus, air, air, blocus, blocus, blocus, blocus, air, air, air, air, blocus, blocus, blocus, blocus, blocus, air, air, blocus, blocus, blocus, blocus, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, air, blocus, blocus, blocus, blocus, blocus, blocus, blocus, blocus, blocus, air, air, air, air, air, drapeau, air, air, air, air, air, air, air, air, air, air, air, air],
    [sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, air, air, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, air, air, air, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, air, air, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol],
    [sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, air, air, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, air, air, air, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, air, air, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol, sol],
]# map 2 du jeu qui reprend le premier niveau iconique du mario sur nes 


longueur2 = 0 #valeur qui s'agrandit si on arrive au bout de l'écran
longueur = infoObject.current_w/50 #taille de l'écran divisé par la taille d'un bloc pour savoir combien de bloc sont affichés à l'écran 
world=0 #valeur qui choisit dans quelle monde nous sommes
reset_niveau=0


def afficher_labyrinthe(labyrinthe):
    #Dessine le labyrinthe sur 'fenetre'.
    block_size = 50
    largeur = infoObject.current_h/block_size
    global longueur
    global longueur2
    global reset_niveau
    i_p,j_p,labyrinthe = choix_monde()
    if labyrinthe[i_p][int(longueur)-2]==player: #si le joueur arrive à la fin de l'écran on change l'affichage pour changer de scène et pouvoir continuer dans le niveau 
        longueur2+= infoObject.current_w/block_size #s'augmente de longueur pour pemettre d'afficher la suite du niveau sur l'écran
        labyrinthe[i_p][j_p]=air #supprime le joueur
        labyrinthe[i_p][int(longueur)+1]=player #place le joueur à gauche de l'écran
        if longueur + infoObject.current_w/block_size < len(labyrinthe[1]):
            longueur +=infoObject.current_w/block_size #s'agrandit de la taille de l'écran pour montrer la suite du niveau
        else:
            longueur=len(labyrinthe[1]) #si la suite du niveau est plus petite que la taille de l'écran on affiche juste la fin du niveau

    if labyrinthe[i_p][int(longueur2)-3]==player: #si le joueur arrive à la fin de l'écran on change l'affichage pour changer de scène et pouvoir continuer dans le niveau 
        if longueur2-infoObject.current_w/block_size>0:
            longueur2-= infoObject.current_w/block_size #s'augmente de longueur pour pemettre d'afficher la suite du niveau sur l'écran
            labyrinthe[i_p][j_p]=air #supprime le joueur
            labyrinthe[i_p][int(longueur2)]=player #place le joueur à gauche de l'écran
            if longueur - infoObject.current_w/block_size < len(labyrinthe[1]):
                longueur -=infoObject.current_w/block_size #s'agrandit de la taille de l'écran pour montrer la suite du niveau
        else:
            longueur=infoObject.current_w/block_size #si la suite du niveau est plus petite que la taille de l'écran on affiche juste la fin du niveau
            longueur2=0
    if reset_niveau >= 1: #lors d'un changement de monde on remet à zéro toute les valeurs pour que tout remarche bien
        longueur2 = 0
        longueur = infoObject.current_w/50
        reset_niveau=0
        

    fenetre.fill((0,0,0))
    for i in range(len(labyrinthe)): #va lire cahque valeur présente dans le tableau 
        for j in range(int(longueur2), int(longueur)):
            dessine_rectangle((119, 181, 254), (j-int(longueur2)) * block_size, i * block_size, block_size, block_size) #dessine des carés bleu pour faire le ciel
            if labyrinthe[i][j] == sol:
                fenetre.blit(sol,( (j-int(longueur2)) * block_size, i * block_size,)) #affiche la texture du sol si dans le tableau le mot aux coordonnées est sol 
            if labyrinthe[i][j] == eau:
                dessine_rectangle((255, 0, 0), (j-int(longueur2)) * block_size, i * block_size, block_size, block_size)
            elif labyrinthe[i][j] == drapeau:
                dessine_rectangle((119, 181, 254), (j-int(longueur2)) * block_size, i * block_size, block_size, block_size)
                if labyrinthe[i+1][j] == sol:
                    fenetre.blit(drapeau,( (j-int(longueur2)) * block_size, i * block_size- 3*block_size,))

            #fonction à rajouter pour rajouter un niveau supplémentaire
            if labyrinthe[i][j] == Level_1:
                fenetre.blit(Level_1,( (j-int(longueur2)) * block_size, i * block_size,))
            if labyrinthe[i][j] == Level_2:
                fenetre.blit(Level_2,( (j-int(longueur2)) * block_size, i * block_size,))

            if labyrinthe[i][j] == cloud:
                fenetre.blit(cloud,( (j-int(longueur2)) * block_size, i * block_size,))
            if labyrinthe[i][j] == cloud1:
                fenetre.blit(cloud1,( (j-int(longueur2)) * block_size, i * block_size,))
            if labyrinthe[i][j] == cloud2:
                fenetre.blit(cloud2,( (j-int(longueur2)) * block_size, i * block_size,))
            if labyrinthe[i][j] == tuyau:
                fenetre.blit(tuyau,( (j-int(longueur2)) * block_size, i * block_size,))
            if labyrinthe[i][j] == player:
                fenetre.blit(images[compteur_images],( (j-int(longueur2)) * block_size, i * block_size,))
            if labyrinthe[i][j] == bowser:
                fenetre.blit(images_bowser[compteur_images_bowser],( (j-int(longueur2)) * block_size - block_size, i * block_size - block_size,))
            if labyrinthe[i][j] == goomba:
                fenetre.blit(goomba,( (j-int(longueur2)) * block_size, i * block_size,))
            if labyrinthe[i][j] == koopa:
                fenetre.blit(koopa,( (j-int(longueur2)) * block_size, i * block_size,))
            if labyrinthe[i][j] == piece:
                fenetre.blit(piece,( (j-int(longueur2)) * block_size, i * block_size,))
            if labyrinthe[i][j] == bloc:
                fenetre.blit(bloc,( (j-int(longueur2)) * block_size, i * block_size,))
            if labyrinthe[i][j] == blocus:
                fenetre.blit(blocus,( (j-int(longueur2)) * block_size, i * block_size,))
            if labyrinthe[i][j] == mist:
                fenetre.blit(mist,( (j-int(longueur2)) * block_size, i * block_size,))


def dessine_rectangle(color, x, y, largeur, hauteur):
    # Dessine un rectangle sur la surface globale 'fenetre'.
    pygame.draw.rect(fenetre, color, (int(x), int(y), int(largeur), int(hauteur)))

def dessine_disque(color: tuple, x: int, y: int, rayon: int):
    #Dessine un rectangle sur la surface globale 'fenetre'.
    global fenetre
    pygame.draw.circle(fenetre, color, (int(x), int(y)), int(rayon))
    
    
    
    

def trouver_coordonnees(tableau, valeur):# trouve dans le tableau l'emplacement de la valeur indiqué pour la ressortir en tuple avec 2 valeurs et un dictionnaire qui possèdent les coordonnées du joueur
    """
    trouve dans le tableau l'emplacement de la valeur indiqué 
    
    

    args:
        tableau:le niveau dans lequel on va chercher la valeur
        valeur: le mot ou la valeur que l'on cherche dans le tableau  

    returns:
        la ressortir en tuple avec 2 valeurs et un dictionnaire qui possèdent les coordonnées du joueur
    """
    
    dico_valeur={}
    renvoi_i=None
    renvoi_j=None
    for i in range(len(tableau)):
        for j in range(len(tableau[i])):
            if tableau[i][j] == valeur:
                # Ajoutez les coordonnées au dictionnaire
                renvoi_i=i
                renvoi_j=j
                dico_valeur[len(dico_valeur) + 1] = renvoi_i,renvoi_j,k_g #met dans un dictionnaire toutes les coordonnées trouver pour une valeur qui se trouverait en plusieurs exemplaires dans le tableau
    return renvoi_i,renvoi_j, dico_valeur


dico_goomba={}
dico_koopa={}
dico_bloc={}
dico_valeur={}
def choix_monde(): #définit l'emplacement du joueur et des enemis au moment ou le joueur change de monde 
    global dico_goomba
    global dico_koopa
    global dico_bloc
    if world == 0:
        i=trouver_coordonnees(world_map, player)[0]
        j=trouver_coordonnees(world_map, player)[1]
        dico_goomba={}
        dico_koopa={}
        dico_bloc={}
        return i,j, world_map

    elif world == 1:
        i=trouver_coordonnees(jeu_map_update, player)[0]
        j=trouver_coordonnees(jeu_map_update, player)[1]
        if dico_goomba == {}:
            dico_goomba=trouver_coordonnees(jeu_map_update, goomba)[2]
            dico_koopa=trouver_coordonnees(jeu_map_update, koopa)[2]
            dico_bloc=trouver_coordonnees(jeu_map_update, bloc)[2]
        return i,j, jeu_map_update

    
    #fonction à rajouter pour rajouter un niveau supplémentaire en changeant les valeurs
    elif world == 2:
        i=trouver_coordonnees(jeu_map_2, player)[0]
        j=trouver_coordonnees(jeu_map_2, player)[1]
        if dico_goomba == {}:
            dico_goomba=trouver_coordonnees(jeu_map_2, goomba)[2]
            dico_koopa=trouver_coordonnees(jeu_map_2, koopa)[2]
            dico_bloc=trouver_coordonnees(jeu_map_2, bloc)[2]
        return i,j, jeu_map_2


def score_joueur(): # gere l'affichage du score du joueur 
    global score
    texte = font.render(f"score total : {score}", True, (255, 255, 255))
    fenetre.blit(texte, (10 + PV_joueur * 50 + 20, 15))

def vie_joueur(): # gere l'affichage de la vie du joueur et sa mort si sa vie tombe à zéro
    global PV_joueur
    global world
    texte = font.render(f"vie : {PV_joueur}", True, (255, 255, 255))
    fenetre.blit(texte, (infoObject.current_w/3,len((choix_monde()[2]))*50+10))
    for i in range(PV_joueur):
        fenetre.blit(coeur, (10 + i * 50, 10))
    if PV_joueur<= 0:
        fenetre.fill((0,0,0))
        texte = font2.render("GAME OVER", True, (255, 0, 0))
        fenetre.blit(texte, (infoObject.current_w/2, infoObject.current_h/2))
        pygame.time.wait(1000)
        PV_joueur=3
        world=0
              
#ne fait pas changer la texture du bloc
def block(): 
    i_p,j_p,jeu_map_update = choix_monde()
    global dico_bloc
    global bloc
    for cle in dico_bloc:
        i, j ,k_g= dico_bloc[cle] # Récupere les valeur (i, j,k_g) associées à la clé dans le dico
        if jeu_map_update[i+1][j]==player:
            jeu_map_update[i][j]==bloc_casse
            fenetre.fill((0,0,0))
            afficher_labyrinthe()

start_counter = False
def start_timer(): # creer un timer qui sert à gerer la mecanique de saut du joueur 
    global start_counter
    start_counter = True
    pygame.time.set_timer(TIMER_EVENT, 700)  # déclenche le TIMER_EVENT toutes les 0.7 secondes

def stop_timer(): #arrete le timer pour le saut du joueur
    global start_counter
    start_counter = False
    pygame.time.set_timer(TIMER_EVENT, 0)  # arrête le TIMER_EVENT





    
     



# PROBLEME si deux enemi du meme type se rencontre elle fusionne et ne forme plus qu'un
def enemi(): # fait déplacer les enemi et gere les dégats avec le joueur collision entre deux types d'enemis 
    # prise des variables du jeu
    i_p,j_p,jeu_map_update = choix_monde()
    global intervalle
    intervalle+=1
    tps_frames=20
    global score
    global PV_joueur
    global k_g 
    global k_k
    global dico_goomba
    global dico_koopa
    
    #mort des enemis si le joueur est dessus
    if jeu_map_update[i_p+1][j_p]==goomba or jeu_map_update[i_p+1][j_p]==koopa: #si le joueur se trouve au dessus d'un enemi alors il remplace et gagne des points au score
        jeu_map_update[i_p+1][j_p]=air
        jeu_map_update[i_p+1][j_p]=player
        jeu_map_update[i_p][j_p]=air
        score+=100 # rajoute des points au score du joueur
        fenetre.fill((0, 0, 0)) # fait un écran noir pour que le score se mette à jour à l'écran
        
    else:
        for cle in dico_goomba:
            i, j,k_g= dico_goomba[cle] # Récupere les valeur (i, j,k_g) associées à la clé dans le dico
            if jeu_map_update[i][j]==goomba:
                if jeu_map_update[i][j+dico_goomba[cle][2]]==player or jeu_map_update[i][j-dico_goomba[cle][2]]==player:
                    jeu_map_update[i][j] = air
                    PV_joueur-= 1 # baisse les PV du joueur si celui ci touche un goomba
                    fenetre.fill((0, 0, 0))
        for cle in dico_koopa:
                i, j,k_k = dico_koopa[cle] # Récupere les valeur (i, j,k_g) associées à la clé dans le dico
                if jeu_map_update[i][j]==koopa:
                    if jeu_map_update[i][j+dico_koopa[cle][2]]==player  or jeu_map_update[i][j-dico_koopa[cle][2]]==player:
                        jeu_map_update[i][j] = air
                        PV_joueur-= 1 # baisse les PV du joueur si celui ci touche un koopa
                        fenetre.fill((0, 0, 0))

        if intervalle%tps_frames==0: # deplace les monstres seulement toutes les 20 images pour un deplacement plus lent
            for cle in dico_goomba:
                i, j,k_g= dico_goomba[cle] # Récupere les valeur (i, j,k_g) associées à la clé dans le dico
                if jeu_map_update[i][j]==goomba:
                    if jeu_map_update[i][j+dico_goomba[cle][2]] not in (sol,bloc,blocus,tuyau): #on regarde si la destination est un sol
                        jeu_map_update[i][j + dico_goomba[cle][2]] = goomba  # on deplace le koopa et on met à jour ses coordonnees dans le dicotionnaire associe
                        jeu_map_update[i][j] = air
                        dico_goomba[cle]= (i,j+ dico_goomba[cle][2],k_g)

                    elif jeu_map_update[i][j-1] in (sol,bloc,blocus,tuyau):
                        dico_goomba[cle]= (i,j+ 1, 1) # change la valeur interne du goomba qui fait que celui ci avance ou recule
                        jeu_map_update[i][j] = air
                        jeu_map_update[i][j + dico_goomba[cle][2]] = goomba  
                        jeu_map_update[i][j] = air

                    elif jeu_map_update[i][j+1] in (sol,bloc,blocus,tuyau):
                        dico_goomba[cle]= (i,j- 1, -1)
                        jeu_map_update[i][j] = air
                        jeu_map_update[i][j + dico_goomba[cle][2]] = goomba
                        jeu_map_update[i][j] = air

            for cle in dico_koopa:
                i, j,k_k = dico_koopa[cle] # Récupere les valeur (i, j,k_g) associées à la clé dans le dico
                if jeu_map_update[i][j]==koopa:    
                    if jeu_map_update[i][j+dico_koopa[cle][2]] not in (sol,bloc,blocus,tuyau): # on regarde si la destination est un sol
                        jeu_map_update[i][j + dico_koopa[cle][2]] = koopa # on deplace le koopa et on met à jour ses coordonnees dans le dicotionnaire associe
                        jeu_map_update[i][j] = air
                        dico_koopa[cle]= (i,j+ dico_koopa[cle][2],k_k)

                    elif jeu_map_update[i][j-1] in (sol,bloc,blocus,tuyau): #fait avancer le koopa dans l'autre sens si un mur est devant lui
                        dico_koopa[cle]= (i,j+ 1, 1) #change la valeur interne de la koopa qui fait que celle ci avance ou recule
                        jeu_map_update[i][j] = air
                        jeu_map_update[i][j + dico_koopa[cle][2]] = koopa  
                        jeu_map_update[i][j] = air

                    elif jeu_map_update[i][j+1] in (sol,bloc,blocus,tuyau):
                        dico_koopa[cle]= (i,j- 1, -1)
                        jeu_map_update[i][j] = air
                        jeu_map_update[i][j + dico_koopa[cle][2]] = koopa
                        jeu_map_update[i][j] = air
    return jeu_map_update ,dico_goomba, dico_koopa




def move(deplacement): # gère le déplacement du joueur sur tous les axes 
    """
    fait déplacer le joueur dans le niveau et dans le tableau 

    args:
        prend la touche sur laquelle le joueur à appuyé pour la retranscire dans le tableau et faire bouger le joueur

    returns:
        le tableau du niveau dans lequel le joueur aura bougé 

    """
    i,j,jeu_map_update = choix_monde()
    global score
    global compteur
    if deplacement=="gauche": # si la flèche de gauche est pressée alors on fait avancer le joueur vers la gauche
        if jeu_map_update[i][j-1]!=sol and jeu_map_update[i][j-1]!=bloc and jeu_map_update[i][j-1]!=mist and jeu_map_update[i][j-1]!=tuyau and jeu_map_update[i][j-1]!=blocus: # on regarde si il y a un bloc à la destination que l'on souhaite
            if jeu_map_update[i][j-1]==piece:
                score+=3
                fenetre.fill((0, 0, 0))
            jeu_map_update[i][j-1]=player # on déplace le joueur dans la direction voulue
            jeu_map_update[i][j]=air # on remplace son ancienne position par de l'air
        elif jeu_map_update[i][j-1] in (sol,bloc,blocus,tuyau):
            if jeu_map_update[i+1][j]!=sol and jeu_map_update[i+1][j]!=mist and jeu_map_update[i+1][j]!=bloc and jeu_map_update[i+1][j]!=blocus and jeu_map_update[i+1][j]!=tuyau:
                jeu_map_update[i-2][j]=player #on déplace le joueur dans la direction voulue
                jeu_map_update[i][j]=air
        return jeu_map_update # on update la map du jeu
    elif deplacement=="droite": # si la flèche de droite est pressée alors on fait avancer le joueur vers la droite
        if jeu_map_update[i][j+1]!=sol and jeu_map_update[i][j+1]!=bloc and jeu_map_update[i][j+1]!=mist and jeu_map_update[i][j+1]!=tuyau and jeu_map_update[i][j+1]!=blocus:
            if jeu_map_update[i][j+1]==piece:
                score+= 3
                fenetre.fill((0, 0, 0))
            jeu_map_update[i][j+1]=player
            jeu_map_update[i][j]=air
        elif jeu_map_update[i][j+1] in (sol,bloc,blocus,tuyau):
            if jeu_map_update[i+1][j]!=sol:
                jeu_map_update[i-2][j]=player #on déplace le joueur dans la direction voulue
                jeu_map_update[i][j]=air
        return jeu_map_update

    elif deplacement=="haut": # si la flèche du haut est pressée alors on fait monter le joueur
        if jeu_map_update[i+1][j] in (sol,bloc,blocus,tuyau,mist): # on regarde si le joueur à du sol sous les pieds pour pouvoir sauter
            if jeu_map_update[i-1][j]==sol and jeu_map_update[i-1][j]!=Level_1 and jeu_map_update[i-1][j]!=Level_2: # on regarde si il y a un bloc au dessus de sa tête pour passer au dessus de ce bloc
                jeu_map_update[i-2][j]=player
                jeu_map_update[i][j]=air
                return jeu_map_update
            else:
                if jeu_map_update[i-1][j]!=bloc and jeu_map_update[i-1][j]!=mist and jeu_map_update[i-1][j]!=blocus and jeu_map_update[i-1][j]!=tuyau: # si il n'y a pas de bloc au dessus alors on saute de un bloc
                    if jeu_map_update[i-1][j]==piece:
                        score+=3
                        block()
                        fenetre.fill((0, 0, 0))
                    jeu_map_update[i-1][j]=player #on déplace le joueur dans la direction voulue
                    jeu_map_update[i][j]=air
                else:
                    score+=1
                    fenetre.fill((0, 0, 0))
        jump_sound.play()
        compteur=0
        start_timer()
        return jeu_map_update

def in_the_air(): #déplace le joueur jusqu'au sol si celui ci est dans les air
    i,j,jeu_map_update = choix_monde()
    if jeu_map_update[i+1][j]==air:
        jeu_map_update[i+1][j]=player
        jeu_map_update[i][j]=air
        return jeu_map_update
    else:
        return False

def choix_niveau(): #gère l'affichage de la carte au moment ou le joueur passe dans un tuyau pour accéder à un niveau
    global world
    global reset_niveau
    i,j,jeu_map_update = choix_monde()
    if jeu_map_update[i][j+1]==drapeau: #gere le système de retour au hub principale 
        reset_niveau+=1
        world=0
        fenetre.fill((0, 0, 0))
        i,j,jeu_map_update = choix_monde()
        jeu_map_update[i][j]=air
        jeu_map_update[i][j+1]=player
    elif jeu_map_update[i+1][j]==Level_1:
        world=1

    #fonction à rajouter pour rajouter un niveau supplémentaire en changeant les valeurs
    elif jeu_map_update[i+1][j]==Level_2:
        world=2
    return world
    
def anim_saut(): #fait le changement d'animation du joueur en fonction de si il est au sol ou dans les air 
    global compteur_images
    i,j,jeu_map_update = choix_monde()
    if jeu_map_update[i+1][j]!=air:
        if compteur_images>= nombre_images-2:
            compteur_images=0
        elif compteur_images>= nombre_images-2:
            compteur_images=0
        elif jeu_map_update[i+1][j]!=air:
            compteur_images+=1 
    elif jeu_map_update[i+1][j]==air:
            compteur_images= nombre_images-1
    return compteur_images

def boss():# gère les animations du boss comme ses pas ou ses attaques 
    global compteur_images_bowser
    global compteur_bowser
    if compteur_bowser< 1000:
        if compteur_images_bowser>= (len(images_bowser)-4):
            compteur_images_bowser=0
            compteur_bowser+=1
        else:
            compteur_images_bowser+=1
            compteur_bowser+=1
    if compteur_bowser > 1000 and compteur_bowser < 1200:
        compteur_images_bowser+=1
        if compteur_images_bowser>= (len(images_bowser)-1):
            compteur_images_bowser = (len(images_bowser)-4)
    if compteur_bowser > 1000 and compteur_bowser < 1001:
        compteur_images_bowser = (len(images_bowser)-4)
        if compteur_images_bowser>= (len(images_bowser)-1):
            compteur_images_bowser = (len(images_bowser)-4)
    if compteur_bowser> 1200:
        compteur_images_bowser=0
    fenetre.fill((0,0,0))
    texte = font.render(f"score total : {compteur_bowser}", True, (255, 255, 255))
    fenetre.blit(texte, (50, 60))
    return compteur_images_bowser




# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == TIMER_EVENT and start_counter:
                compteur += 1
        elif event.type == TIMER_EVENT_mario :
                compteur_images += 1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_z:
                if compteur==1:
                    move("haut")
                    
            elif event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()
            elif event.key == pygame.K_LEFT or event.key == pygame.K_q:
                move("gauche")
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                move("droite")
            
        choix_niveau()
        choix_monde()

    afficher_labyrinthe(choix_monde()[2])
    enemi()
    vie_joueur()
    score_joueur()
    pygame.display.flip()
    if compteur>=1:
                in_the_air()
                stop_timer()
    anim_saut()
    boss()
    horloge.tick(60)

pygame.quit()

# piste d'amélioration du jeu

# les blocs ? sont cassé par le joueur
# flip les ennemi lors du changement de direction 
# LV1= tuto de base du jeu mario
# LV2= niveau dans la grotte
# LV3= niveau dans le désert
# faire un sytème de sol différent pour chaque niveau
# faire un système de wall jump
# faire un meilleur fond pour les niveaux nuages, désert, neige, lave
# créer un niveau complet mario 
# faire un deuxième niveau 
# faire un champignon pour mario
# faire un système de grandissment pour mario 
# faire un système de ckeckpoint 
# faire un système de bloc cassable 
# faire un petit boss bowser 
# faire des plantes élémentaires et des pouvoir élémentaire, fleur de feu de glace 