import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PINK = (255, 192, 203)

# Load background image
BACKGROUND = pygame.image.load('assets/sky.jpg')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.facing_right = True
        
        try:
            # Charger l'image simple du joueur
            original_image = pygame.image.load('assets/sprites/Frame_0.png').convert_alpha()
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

    def update(self):
        # Apply gravity
        self.velocity_y += 0.8
        
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

        # Wrap around screen
        if self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH

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

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Doodle Jump Clone")
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.high_score = 0
        self.game_won = False
        self.game_over = False
        self.countdown_active = False
        self.countdown_start = 0
        self.countdown_duration = 3  # secondes
        
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        
        # Create ground platform
        self.ground_platform = Platform(0, SCREEN_HEIGHT - 20, "ground")
        self.platforms.add(self.ground_platform)
        self.all_sprites.add(self.ground_platform)
        
        # Generate initial platforms
        self.generate_platforms()

    def generate_platforms(self):
        for i in range(10):
            platform_type = random.choice(["normal", "moving", "fragile"])
            platform = Platform(
                random.randint(0, SCREEN_WIDTH - 100),  # Ajusté pour la nouvelle largeur
                i * (SCREEN_HEIGHT // 10),
                platform_type
            )
            self.platforms.add(platform)
            self.all_sprites.add(platform)

    def handle_events(self):
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if (self.game_won or self.game_over) and not self.countdown_active:
                    self.countdown_active = True
                    self.countdown_start = current_time
            
        # Handle continuous keyboard input
        if not self.game_won and not self.game_over and not self.countdown_active:
            keys = pygame.key.get_pressed()
            self.player.velocity_x = 0
            if keys[pygame.K_LEFT]:
                self.player.velocity_x = -5
            if keys[pygame.K_RIGHT]:
                self.player.velocity_x = 5

    def update(self):
        current_time = pygame.time.get_ticks()
        
        # Gestion du décompte
        if self.countdown_active:
            elapsed = (current_time - self.countdown_start) // 1000
            if elapsed >= self.countdown_duration:
                self.countdown_active = False
                self.reset_game()
            return
            
        if not self.game_won and not self.game_over:
            self.all_sprites.update()

            # Check for platform collisions
            if self.player.velocity_y > 0:
                hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
                if hits:
                    lowest = hits[0]
                    for hit in hits:
                        if hit.rect.bottom > lowest.rect.bottom:
                            lowest = hit
                    
                    if self.player.rect.bottom <= lowest.rect.centery:
                        self.player.rect.bottom = lowest.rect.top
                        self.player.velocity_y = -18  # Augmentation de la force du saut de -15 à -18
                        
                        # Seules les plateformes fragiles disparaissent
                        if lowest.type == "fragile":
                            lowest.kill()

            # Move screen down when player reaches upper third
            if self.player.rect.top <= SCREEN_HEIGHT // 3:
                scroll_speed = 5
                self.player.rect.y += scroll_speed
                
                # Mettre à jour la position de toutes les plateformes
                for platform in self.platforms:
                    platform.rect.y += scroll_speed
                    if hasattr(platform, 'image_rect'):  # Vérifier si la plateforme a un image_rect
                        platform.image_rect.y += scroll_speed
                    
                    # Le sol disparaît quand il sort de l'écran
                    if platform.rect.top >= SCREEN_HEIGHT:
                        if platform == self.ground_platform:
                            platform.kill()
                        else:
                            platform.kill()
                            # Create new platform at the top
                            platform_type = random.choice(["normal", "moving", "fragile"])
                            new_platform = Platform(
                                random.randint(0, SCREEN_WIDTH - 100),  # Ajusté pour la nouvelle largeur
                                random.randint(-50, 0),
                                platform_type
                            )
                            self.platforms.add(new_platform)
                            self.all_sprites.add(new_platform)
                            self.score += 1

            # Check for game over
            if self.player.rect.top > SCREEN_HEIGHT:
                self.high_score = max(self.score, self.high_score)
                self.game_over = True
                self.countdown_active = True
                self.countdown_start = current_time

    def reset_game(self):
        self.score = 0
        self.game_won = False
        self.game_over = False
        self.countdown_active = False
        self.all_sprites.empty()
        self.platforms.empty()
        self.player = Player()
        self.all_sprites.add(self.player)
        
        # Create ground platform
        self.ground_platform = Platform(0, SCREEN_HEIGHT - 20, "ground")
        self.platforms.add(self.ground_platform)
        self.all_sprites.add(self.ground_platform)
        
        self.generate_platforms()

    def draw(self):
        self.screen.blit(BACKGROUND, (0, 0))
        
        # Dessiner toutes les sprites
        for sprite in self.all_sprites:
            if hasattr(sprite, 'image_rect') and isinstance(sprite, Platform) and sprite.type != "ground":
                # Pour les plateformes normales, mobiles et fragiles
                self.screen.blit(sprite.image, sprite.image_rect)
            else:
                # Pour le joueur et le sol
                self.screen.blit(sprite.image, sprite.rect)
        
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        high_score_text = font.render(f'High Score: {self.high_score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(high_score_text, (10, 40))
        
        # Draw win/game over message
        if self.game_won or self.game_over:
            big_font = pygame.font.Font(None, 72)
            if self.game_won:
                message = 'YOU WIN!'
                color = YELLOW
            else:
                message = 'GAME OVER'
                color = RED
            
            message_text = big_font.render(message, True, color)
            message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(message_text, message_rect)
            
            if self.countdown_active:
                current_time = pygame.time.get_ticks()
                remaining = self.countdown_duration - (current_time - self.countdown_start) // 1000
                countdown_text = font.render(f'Nouvelle partie dans {remaining}...', True, WHITE)
                countdown_rect = countdown_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
                self.screen.blit(countdown_text, countdown_rect)
            else:
                restart_text = font.render('Press SPACE to play again', True, WHITE)
                restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
                self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
