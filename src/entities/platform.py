import pygame
from ..game.constants import SCREEN_WIDTH, BLACK, GREEN, RED, YELLOW

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, platform_type):
        super().__init__()
        self.type = platform_type
        
        # Dimensions standard pour toutes les plateformes (sauf le sol)
        self.PLATFORM_WIDTH = 100
        self.PLATFORM_HEIGHT = 50
        # Dimensions de la boîte de collision (plus petite que le sprite)
        self.COLLISION_HEIGHT = 20
        self.COLLISION_Y_OFFSET = 15
        
        if platform_type == "ground":
            self.image = pygame.Surface((SCREEN_WIDTH, 20))
            self.image.fill(BLACK)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        else:
            if platform_type == "normal":
                try:
                    # Charger et redimensionner l'image pour les plateformes normales
                    original = pygame.image.load('assets/platforms/Green.png').convert_alpha()
                    self.image = pygame.transform.scale(original, (self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                except Exception as e:
                    print(f"Error loading platform image: {e}")
                    self.image = pygame.Surface((self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                    self.image.fill(GREEN)
            elif platform_type == "moving":
                try:
                    # Charger et redimensionner l'image pour les plateformes mobiles
                    original = pygame.image.load('assets/platforms/neon.png').convert_alpha()
                    self.image = pygame.transform.scale(original, (self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                except Exception as e:
                    print(f"Error loading platform image: {e}")
                    self.image = pygame.Surface((self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                    self.image.fill(RED)
                self.direction = 1
                self.speed = 2
            elif platform_type == "fragile":
                try:
                    # Charger et redimensionner l'image pour les plateformes fragiles
                    original = pygame.image.load('assets/platforms/Hell2.png').convert_alpha()
                    self.image = pygame.transform.scale(original, (self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                except Exception as e:
                    print(f"Error loading platform image: {e}")
                    self.image = pygame.Surface((self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                    self.image.fill(YELLOW)
                self.broken = False
            
            # Créer le rectangle de l'image et de collision pour les plateformes non-sol
            self.image_rect = self.image.get_rect()
            self.image_rect.x = x
            self.image_rect.y = y
            self.rect = pygame.Rect(x, y + self.COLLISION_Y_OFFSET, 
                                  self.PLATFORM_WIDTH, self.COLLISION_HEIGHT)

    def update(self):
        if self.type == "moving":
            self.rect.x += self.speed * self.direction
            self.image_rect.x = self.rect.x
            if self.rect.right > SCREEN_WIDTH or self.rect.left < 0:
                self.direction *= -1
