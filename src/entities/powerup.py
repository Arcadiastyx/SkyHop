import pygame
from ..game.constants import ORANGE, PURPLE, CYAN

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, powerup_type):
        super().__init__()
        self.type = powerup_type
        self.size = 20
        self.image = pygame.Surface((self.size, self.size))
        
        # Différentes couleurs selon le type de power-up
        if powerup_type == "high_jump":
            self.image.fill(ORANGE)
        elif powerup_type == "double_jump":
            self.image.fill(PURPLE)
        elif powerup_type == "boost":
            self.image.fill(CYAN)
            
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
