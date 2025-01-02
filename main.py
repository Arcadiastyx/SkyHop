import pygame
import random
import sys

# Initialize Pygame
pygame.init()

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
        
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()  # Nouveau groupe pour les power-ups
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
                random.randint(0, SCREEN_WIDTH - 100),
                i * (SCREEN_HEIGHT // 10),
                platform_type
            )
            self.platforms.add(platform)
            self.all_sprites.add(platform)
            
            # 10% de chance de générer un power-up au-dessus de la plateforme
            if random.random() < 0.10:
                powerup_type = random.choice(["high_jump", "double_jump", "boost"])
                powerup = PowerUp(
                    platform.rect.centerx,
                    platform.rect.top - 30,
                    powerup_type
                )
                self.powerups.add(powerup)
                self.all_sprites.add(powerup)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE and (self.game_over or self.game_won):
                    self.reset_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Vérifier si le bouton restart est cliqué
                if self.game_over or self.game_won:
                    mouse_pos = pygame.mouse.get_pos()
                    restart_rect = pygame.Rect(SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT//2 + 50, 100, 40)
                    if restart_rect.collidepoint(mouse_pos):
                        self.reset_game()

    def update(self):
        current_time = pygame.time.get_ticks()
        
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
                        base_jump = -18 - self.player.jump_boost
                        self.player.velocity_y = base_jump
                        
                        # Réactiver le double saut si disponible
                        if self.player.double_jump_active:
                            self.player.can_double_jump = True
                        
                        # Seules les plateformes fragiles disparaissent
                        if lowest.type == "fragile":
                            lowest.kill()

            # Vérifier les collisions avec les power-ups
            powerup_hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
            for powerup in powerup_hits:
                if powerup.type == "high_jump":
                    self.player.jump_boost = 3
                elif powerup.type == "double_jump":
                    self.player.double_jump_active = True
                    self.player.double_jump_time = pygame.time.get_ticks()
                    self.player.can_double_jump = True
                elif powerup.type == "boost":
                    self.player.velocity_y = -28  # Super boost vers le haut

            # Move screen down when player reaches upper third
            if self.player.rect.top <= SCREEN_HEIGHT // 3:
                scroll_speed = 5
                self.player.rect.y += scroll_speed
                
                # Mettre à jour la position de toutes les plateformes et power-ups
                for sprite in self.all_sprites:
                    if sprite != self.player:  # Ne pas affecter le joueur
                        sprite.rect.y += scroll_speed
                        if hasattr(sprite, 'image_rect'):
                            sprite.image_rect.y += scroll_speed
                        
                        # Supprimer les sprites qui sortent de l'écran
                        if sprite.rect.top >= SCREEN_HEIGHT:
                            if sprite == self.ground_platform:
                                sprite.kill()
                            elif isinstance(sprite, Platform):
                                sprite.kill()
                                # Create new platform at the top
                                platform_type = random.choice(["normal", "moving", "fragile"])
                                new_platform = Platform(
                                    random.randint(0, SCREEN_WIDTH - 100),
                                    random.randint(-50, 0),
                                    platform_type
                                )
                                self.platforms.add(new_platform)
                                self.all_sprites.add(new_platform)
                                
                                # 10% de chance de générer un power-up
                                if random.random() < 0.10:
                                    powerup_type = random.choice(["high_jump", "double_jump", "boost"])
                                    powerup = PowerUp(
                                        new_platform.rect.centerx,
                                        new_platform.rect.top - 30,
                                        powerup_type
                                    )
                                    self.powerups.add(powerup)
                                    self.all_sprites.add(powerup)
                                
                                self.score += 1
                            elif isinstance(sprite, PowerUp):
                                sprite.kill()

            # Check for game over
            if self.player.rect.top > SCREEN_HEIGHT:
                self.high_score = max(self.score, self.high_score)
                self.game_over = True

    def reset_game(self):
        self.score = 0
        self.game_won = False
        self.game_over = False
        self.all_sprites.empty()
        self.platforms.empty()
        self.powerups.empty()
        self.player = Player()
        self.player.jump_boost = 0  # Réinitialiser les power-ups
        self.player.double_jump_active = False
        self.all_sprites.add(self.player)
        
        # Create ground platform
        self.ground_platform = Platform(0, SCREEN_HEIGHT - 20, "ground")
        self.platforms.add(self.ground_platform)
        self.all_sprites.add(self.ground_platform)
        
        # Generate initial platforms
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
        
        # Draw score à gauche
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        high_score_text = font.render(f'High Score: {self.high_score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(high_score_text, (10, 40))

        # Afficher les power-ups actifs en haut à droite
        x_position = SCREEN_WIDTH - 150  # Position X de départ pour les power-ups
        y_offset = 10  # Commencer en haut
        small_font = pygame.font.Font(None, 24)
        
        # Super Saut
        if self.player.jump_boost > 0:
            boost_icon = pygame.Surface((20, 20))
            boost_icon.fill(ORANGE)
            self.screen.blit(boost_icon, (x_position, y_offset))
            boost_text = small_font.render("Super Saut", True, WHITE)
            self.screen.blit(boost_text, (x_position + 30, y_offset))
            y_offset += 30

        # Double Saut
        if self.player.double_jump_active:
            double_jump_icon = pygame.Surface((20, 20))
            double_jump_icon.fill(PURPLE)
            self.screen.blit(double_jump_icon, (x_position, y_offset))
            time_left = max(0, 10 - (pygame.time.get_ticks() - self.player.double_jump_time) // 1000)
            double_jump_text = small_font.render(f"Double Saut ({time_left}s)", True, WHITE)
            self.screen.blit(double_jump_text, (x_position + 30, y_offset))
            y_offset += 30
        
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
            
            restart_text = font.render('Appuyez sur ESPACE pour recommencer', True, WHITE)
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
