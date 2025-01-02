import os
import pygame

# Définition des couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)  # Pour le double saut
ORANGE = (255, 165, 0)  # Pour le super saut
CYAN = (0, 255, 255)    # Pour la propulsion
PINK = (255, 192, 203)

# Constantes du jeu
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

# Charger l'image de fond
try:
    BACKGROUND = pygame.image.load('assets/sky.jpg')
    BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
except Exception as e:
    print(f"Error loading background image: {e}")
    BACKGROUND = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    BACKGROUND.fill((50, 50, 50))
