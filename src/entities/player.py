import os
import pygame
from ..game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, BLUE

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.facing_right = True
        
        try:
            # Chemin vers le dossier assets
            assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets')
            player_path = os.path.join(assets_dir, 'sprites', 'Frame_0.png')
            
            # Charger l'image simple du joueur
            original_image = pygame.image.load(player_path).convert_alpha()
            # Agrandir l'image (x2)
            self.image = pygame.transform.scale(original_image, (48, 48))
            self.rect = self.image.get_rect()
        except Exception as e:
            print(f"Error loading player image: {e}")
            self.image = pygame.Surface((48, 48))
            self.image.fill(BLUE)
            self.rect = self.image.get_rect()
            
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.velocity_y = 0
        self.velocity_x = 0
        
        # Power-ups
        self.jump_boost = 0  # Bonus de saut
        self.double_jump_active = False  # Double saut activé
        self.double_jump_time = 0  # Temps restant pour le double saut
        self.can_double_jump = False  # Pour suivre si on peut faire un double saut
        
    def update(self):
        current_time = pygame.time.get_ticks()
        
        # Gestion du double saut
        if self.double_jump_active and current_time - self.double_jump_time > 10000:  # 10 secondes
            self.double_jump_active = False
            self.can_double_jump = False
        
        # Apply gravity
        self.velocity_y += 0.8
        
        # Handle continuous keyboard input
        keys = pygame.key.get_pressed()
        self.velocity_x = 0
        if keys[pygame.K_LEFT]:
            self.velocity_x = -5
        if keys[pygame.K_RIGHT]:
            self.velocity_x = 5
        
        # Double saut avec la touche haut
        if keys[pygame.K_UP] and self.double_jump_active and self.can_double_jump:
            self.velocity_y = -18 - self.jump_boost  # Force du saut + bonus
            self.can_double_jump = False  # Utilise le double saut
        
        # Update position
        self.rect.y += self.velocity_y
        self.rect.x += self.velocity_x

        # Retourner l'image selon la direction
        if self.velocity_x < 0 and self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
            self.facing_right = False
        elif self.velocity_x > 0 and not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
            self.facing_right = True

        # Screen wrapping
        if self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
