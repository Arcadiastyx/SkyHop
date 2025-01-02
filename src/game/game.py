import pygame
import random
from ..game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BACKGROUND, WHITE
from ..entities.player import Player
from ..entities.platform import Platform
from ..entities.powerup import PowerUp

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
        self.powerups = pygame.sprite.Group()
        self.player = Player()
        
        # Add player to sprite group
        self.all_sprites.add(self.player)
        
        # Create ground platform
        ground = Platform(0, SCREEN_HEIGHT - 20, "ground")
        self.all_sprites.add(ground)
        self.platforms.add(ground)
        
        # Create initial platforms
        for _ in range(10):
            self.create_platform()

    def create_platform(self):
        # Randomly choose platform type
        platform_type = random.choice(["normal", "moving", "fragile"])
        x = random.randint(0, SCREEN_WIDTH - 100)
        y = random.randint(0, SCREEN_HEIGHT - 100)
        
        # Check if platform would overlap with existing platforms
        new_rect = pygame.Rect(x, y, 100, 20)
        for platform in self.platforms:
            if platform.rect.colliderect(new_rect):
                return
        
        platform = Platform(x, y, platform_type)
        self.all_sprites.add(platform)
        self.platforms.add(platform)
        
        # 10% de chance de créer un power-up au-dessus de la plateforme
        if random.random() < 0.1:
            powerup_type = random.choice(["high_jump", "double_jump", "boost"])
            powerup = PowerUp(x + 40, y - 30, powerup_type)  # Centré au-dessus de la plateforme
            self.all_sprites.add(powerup)
            self.powerups.add(powerup)

    def handle_collisions(self):
        # Check platform collisions only when moving down
        if self.player.velocity_y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                
                if self.player.rect.bottom < lowest.rect.bottom:
                    self.player.rect.bottom = lowest.rect.top
                    self.player.velocity_y = -18 - self.player.jump_boost  # Force du saut + bonus
                    
                    if self.player.double_jump_active:
                        self.player.can_double_jump = True
                    
                    # Handle fragile platforms
                    if lowest.type == "fragile":
                        self.all_sprites.remove(lowest)
                        self.platforms.remove(lowest)
        
        # Check power-up collisions
        hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for powerup in hits:
            if powerup.type == "high_jump":
                self.player.jump_boost = 3
            elif powerup.type == "double_jump":
                self.player.double_jump_active = True
                self.player.double_jump_time = pygame.time.get_ticks()
                self.player.can_double_jump = True
            elif powerup.type == "boost":
                self.player.velocity_y = -28  # Super boost vers le haut

    def update(self):
        # Update all sprites
        self.all_sprites.update()
        
        # Handle collisions
        self.handle_collisions()
        
        # Create new platforms as needed
        while len(self.platforms) < 10:
            self.create_platform()
        
        # Update score
        height = SCREEN_HEIGHT - self.player.rect.bottom
        self.score = max(self.score, int(height))
        self.high_score = max(self.high_score, self.score)
        
        # Check for game over
        if self.player.rect.top > SCREEN_HEIGHT:
            self.game_over = True
        
        # Check for win condition (example: reach height of 1000)
        if self.score >= 1000:
            self.game_won = True

    def draw(self):
        # Draw background
        self.screen.blit(BACKGROUND, (0, 0))
        
        # Draw all sprites
        for sprite in self.all_sprites:
            if isinstance(sprite, Platform) and sprite.type != "ground":
                self.screen.blit(sprite.image, sprite.image_rect)
            else:
                self.screen.blit(sprite.image, sprite.rect)
        
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Afficher les power-ups actifs en haut à droite
        x_offset = SCREEN_WIDTH - 100
        if self.player.jump_boost > 0:
            pygame.draw.circle(self.screen, (255, 165, 0), (x_offset, 20), 10)
            x_offset -= 30
        if self.player.double_jump_active:
            pygame.draw.circle(self.screen, (255, 0, 255), (x_offset, 20), 10)
        
        if self.game_over:
            game_over_text = font.render('Game Over! Press SPACE to restart', True, WHITE)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            self.screen.blit(game_over_text, text_rect)
        elif self.game_won:
            win_text = font.render('You Win! Press SPACE to restart', True, WHITE)
            text_rect = win_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            self.screen.blit(win_text, text_rect)
        
        # Update display
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif (event.key == pygame.K_SPACE and 
                      (self.game_over or self.game_won)):
                    self.__init__()  # Reset the game
            elif (event.type == pygame.MOUSEBUTTONDOWN and 
                  (self.game_over or self.game_won)):
                self.__init__()  # Reset the game

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            if not (self.game_over or self.game_won):
                self.update()
            self.draw()
