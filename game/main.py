# les importations obligatoire pour faire marcher le projet
import os
import pygame
from pygame import mixer
from typing import List
from PIL import Image
import numpy as np
from typing import Tuple
from game.player import PlayerController, PlayerTiles
from game.enemies import EnemyController, EnemyTiles
from game.progression import LevelProgression

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
used_mystery_block = object()
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
k_g=-1
score=0

# tous les chemins d'accès aux images
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
background_path: str = os.path.join(project_path, "images", "Background") + os.sep
bloc_path: str = os.path.join(project_path, "images", "Bloc") + os.sep
ennemi_path: str = os.path.join(project_path, "images", "Ennemi") + os.sep
mario_path: str = os.path.join(project_path, "images", "Mario") + os.sep
map_path: str = os.path.join(project_path, "images", "Map") + os.sep

#ces images sont les images qui vont etre prise pour etre comparer avec l'image et générer le tableau
    #il est recommandé de prendre les images directement depuis l'image du niveau 
    # 16 pixel par 16 pixel est la taille d'une image qui va etre comparé avec le niveau
sol_comp = np.asarray(Image.open(bloc_path+'sol.png'))
blocus_comp = np.asarray(Image.open(bloc_path+'blocus.png'))
drapeau_comp = np.asarray(Image.open(bloc_path+'Drapeau.png'))
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
    np.save(os.path.join(project_path, 'resultats.npy'), matching_array)
    resultats = np.load(os.path.join(project_path, 'resultats.npy'), allow_pickle=True)
    resultats_str = np.array_str(resultats)
    # Afficher la chaîne de caractères ou l'écrire dans un fichier texte
    print(resultats_str)
    # Écrire la chaîne de caractères dans un fichier texte
    with open(os.path.join(project_path, 'resultats.txt'), 'w') as f:
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
drapeau = pygame.transform.scale(pygame.image.load(bloc_path+'Drapeau.png'), (50,200))
piece = pygame.transform.scale(pygame.image.load(bloc_path+'piece.png'), (50,50))

coeur = pygame.transform.scale(pygame.image.load(os.path.join(project_path, 'images', 'coeur.png')), (50,50))


#configuration du son du jeu et des effets sonores
pygame.mixer.music.load(os.path.join(project_path, "images", "jump.mp3"))
jump_sound = mixer.Sound(os.path.join(project_path, "images", "jump.mp3"))
pygame.mixer.music.set_volume(0.03)


# Liste des images pour l'animation de mario
images = [mario1,mario1,mario1,mario1,mario1, mario2, mario2, mario2, mario2, mario2, mario3, mario3, mario3, mario3, mario3,mario_saut,]
images_mario_grand = [
    pygame.transform.scale(image, (40, 65)) for image in images
]
mario_player = PlayerController(
    PlayerTiles(
        player=player,
        air=air,
        solid=sol,
        ground=(sol, bloc, blocus, tuyau, mist, used_mystery_block),
        horizontal_obstacles=(sol, bloc, mist, tuyau, blocus, used_mystery_block),
        jump_obstacles=(bloc, mist, blocus, tuyau, used_mystery_block),
        breakable=bloc,
        broken=bloc_casse,
        collectible=piece,
        finish=drapeau,
        mystery=mist,
        used_mystery=used_mystery_block,
    ),
    animation_frame_count=len(images),
)
enemy_controller = EnemyController(
    EnemyTiles(
        player=player,
        air=air,
        goomba=goomba,
        koopa=koopa,
        obstacles=(sol, bloc, blocus, tuyau),
        support=(sol, bloc, blocus, tuyau, mist),
    )
)
images_bowser = [bowser1,bowser1,bowser1,bowser1,bowser1,bowser2,bowser2,bowser2,bowser2,bowser2,bowser3,bowser3,bowser3,bowser3,bowser3,bowser4,bowser4,bowser4,bowser5,bowser5,bowser5,bowser_atk_1,bowser_atk_2,bowser_atk_3,]
compteur_bowser = 0
compteur_images_bowser = 0

# Intervalle de temps (en millisecondes)
intervalle_temps = 1500 
compteur = 1
TIMER_EVENT = pygame.USEREVENT + 1


#configuration des polices d'écriture pour pygame
font = pygame.font.Font(None, 36)  # Choisissez une police et une taille
font2 = pygame.font.Font(None, 360)  # Choisissez une police et une taille

# Configuration de la fenetre du jeu qui sera adapté à la taille de l'écran du joueur
infoObject = pygame.display.Info() #prend les infos de l'ecran
fenetre = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN) # met en tant que resolution de la fenetre celle de l'ecran de l'utilisateur
pygame.display.set_caption("mario in python tab2D") # donne le nom de la fenetre et du projet



# Niveaux jouables, parcourus dans leur ordre de d?claration.
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
reset_niveau=0
game_levels = [jeu_map_update, jeu_map_2]
level_templates = [[row[:] for row in level] for level in game_levels]
progression = LevelProgression(len(game_levels))
game_completed = False


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
            if labyrinthe[i][j] == cloud:
                fenetre.blit(cloud,( (j-int(longueur2)) * block_size, i * block_size,))
            if labyrinthe[i][j] == cloud1:
                fenetre.blit(cloud1,( (j-int(longueur2)) * block_size, i * block_size,))
            if labyrinthe[i][j] == cloud2:
                fenetre.blit(cloud2,( (j-int(longueur2)) * block_size, i * block_size,))
            if labyrinthe[i][j] == tuyau:
                fenetre.blit(tuyau,( (j-int(longueur2)) * block_size, i * block_size,))
            if labyrinthe[i][j] == player:
                player_image = (
                    images_mario_grand[mario_player.animation_frame]
                    if mario_player.grown
                    else images[mario_player.animation_frame]
                )
                player_y = i * block_size - (15 if mario_player.grown else 0)
                fenetre.blit(player_image, ((j-int(longueur2)) * block_size, player_y))
            if labyrinthe[i][j] == bloc_casse:
                x = (j-int(longueur2)) * block_size
                y = i * block_size
                pygame.draw.rect(fenetre, (139, 69, 19), (x + 4, y + 4, 19, 16))
                pygame.draw.rect(fenetre, (165, 92, 42), (x + 27, y + 7, 18, 12))
                pygame.draw.rect(fenetre, (165, 92, 42), (x + 9, y + 29, 16, 15))
                pygame.draw.rect(fenetre, (139, 69, 19), (x + 29, y + 27, 14, 18))
            if labyrinthe[i][j] == used_mystery_block:
                x = (j-int(longueur2)) * block_size
                y = i * block_size
                pygame.draw.rect(fenetre, (139, 91, 45), (x + 2, y + 2, 46, 46))
                pygame.draw.rect(fenetre, (91, 57, 31), (x + 2, y + 2, 46, 46), 4)
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


dico_valeur={}
def choix_monde():
    active_level = game_levels[progression.level_index]
    i,j,_ = trouver_coordonnees(active_level, player)
    if i is None or j is None:
        raise ValueError("player is missing from the active level")
    return i,j,active_level


def score_joueur(): # gere l'affichage du score du joueur 
    global score
    texte = font.render(f"score total : {score}", True, (255, 255, 255))
    fenetre.blit(texte, (10 + PV_joueur * 50 + 20, 15))

def vie_joueur(): # gere l'affichage de la vie du joueur et sa mort si sa vie tombe à zéro
    global PV_joueur
    texte = font.render(f"vie : {PV_joueur}", True, (255, 255, 255))
    fenetre.blit(texte, (infoObject.current_w/3,len((choix_monde()[2]))*50+10))
    for i in range(PV_joueur):
        fenetre.blit(coeur, (10 + i * 50, 10))
    if PV_joueur<= 0:
        fenetre.fill((0,0,0))
        texte = font2.render("GAME OVER", True, (255, 0, 0))
        fenetre.blit(texte, (infoObject.current_w/2, infoObject.current_h/2))
        pygame.time.wait(1000)
        restart_game()
              
start_counter = False
def start_timer(): # creer un timer qui sert à gerer la mecanique de saut du joueur 
    global start_counter
    start_counter = True
    pygame.time.set_timer(TIMER_EVENT, 700)  # déclenche le TIMER_EVENT toutes les 0.7 secondes

def stop_timer(): #arrete le timer pour le saut du joueur
    global start_counter
    start_counter = False
    pygame.time.set_timer(TIMER_EVENT, 0)  # arrête le TIMER_EVENT


def deplacer_joueur(direction: str) -> None:
    global score
    global compteur
    action = mario_player.move(choix_monde()[2], direction)
    score += action.score_delta
    if action.redraw:
        fenetre.fill((0, 0, 0))
    if action.jump_started:
        jump_sound.play()
        compteur = 0
        start_timer()
    if action.level_finished:
        terminer_niveau()



    
     



# Met à jour les ennemis et applique leurs effets à l'état du jeu.
def mettre_a_jour_ennemis() -> None:
    global score
    global PV_joueur
    action = enemy_controller.update(choix_monde()[2])
    score += action.score_delta
    for _ in range(action.damage):
        if not mario_player.take_hit():
            PV_joueur -= 1
    if action.redraw:
        fenetre.fill((0, 0, 0))




def terminer_niveau() -> None:
    global reset_niveau
    global game_completed
    global compteur
    if progression.advance():
        reset_niveau += 1
        mario_player.reset()
        enemy_controller.reset()
        compteur = 1
        stop_timer()
    else:
        game_completed = True


def restart_game() -> None:
    global jeu_map_update
    global jeu_map_2
    global score
    global PV_joueur
    global reset_niveau
    global longueur
    global longueur2
    global game_completed
    global compteur

    jeu_map_update = [row[:] for row in level_templates[0]]
    jeu_map_2 = [row[:] for row in level_templates[1]]
    game_levels[0] = jeu_map_update
    game_levels[1] = jeu_map_2
    progression.restart()
    enemy_controller.reset()
    mario_player.reset()
    score = 0
    PV_joueur = 3
    reset_niveau = 1
    longueur = infoObject.current_w / 50
    longueur2 = 0
    compteur = 1
    game_completed = False
    stop_timer()


def afficher_victoire() -> None:
    fenetre.fill((0, 0, 0))
    titre = font2.render("VICTOIRE !", True, (255, 255, 0))
    instruction = font.render("Appuie sur R pour recommencer ou Echap pour quitter", True, (255, 255, 255))
    fenetre.blit(titre, titre.get_rect(center=(infoObject.current_w / 2, infoObject.current_h / 2 - 40)))
    fenetre.blit(instruction, instruction.get_rect(center=(infoObject.current_w / 2, infoObject.current_h / 2 + 60)))
    
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
        elif event.type == pygame.KEYDOWN:
            if game_completed:
                if event.key == pygame.K_r:
                    restart_game()
                elif event.key == pygame.K_ESCAPE:
                    running = False
                continue
            if event.key == pygame.K_UP or event.key == pygame.K_z:
                if compteur==1:
                    deplacer_joueur("haut")
                    
            elif event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_LEFT or event.key == pygame.K_q:
                deplacer_joueur("gauche")
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                deplacer_joueur("droite")

    if game_completed:
        afficher_victoire()
        pygame.display.flip()
        horloge.tick(60)
        continue

    afficher_labyrinthe(choix_monde()[2])
    mettre_a_jour_ennemis()
    vie_joueur()
    score_joueur()
    pygame.display.flip()
    if compteur>=1:
        fall_action = mario_player.fall(choix_monde()[2])
        if fall_action.level_finished:
            terminer_niveau()
        if compteur >= 1:
            stop_timer()
    mario_player.update_animation(choix_monde()[2])
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