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
PINK = (255, 192, 203)  # Couleur rose pour le sol

# Player properties
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 40
PLAYER_SPEED = 5
JUMP_FORCE = -15
GRAVITY = 0.8

# Platform properties
PLATFORM_WIDTH = 60
PLATFORM_HEIGHT = 20
PLATFORM_COUNT = 10

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.velocity_y = 0
        self.velocity_x = 0

    def update(self):
        # Apply gravity
        self.velocity_y += GRAVITY
        
        # Update position
        self.rect.y += self.velocity_y
        self.rect.x += self.velocity_x

        # Screen wrapping
        if self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, platform_type="normal"):
        super().__init__()
        self.type = platform_type
        
        if platform_type == "ground":
            self.image = pygame.Surface((SCREEN_WIDTH, PLATFORM_HEIGHT))
            self.image.fill(PINK)
        else:
            self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
            if platform_type == "normal":
                self.image.fill(GREEN)
            elif platform_type == "moving":
                self.image.fill(RED)
                self.direction = 1
                self.speed = 2
            elif platform_type == "fragile":
                self.image.fill((200, 200, 0))
                self.broken = False
            
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.type == "moving":
            self.rect.x += self.speed * self.direction
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
        
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        
        # Create ground platform
        ground = Platform(0, SCREEN_HEIGHT - PLATFORM_HEIGHT, "ground")
        self.platforms.add(ground)
        self.all_sprites.add(ground)
        
        # Generate initial platforms
        self.generate_platforms()

    def generate_platforms(self):
        for i in range(PLATFORM_COUNT):
            platform_type = random.choice(["normal", "moving", "fragile"])
            platform = Platform(
                random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH),
                i * (SCREEN_HEIGHT // PLATFORM_COUNT),
                platform_type
            )
            self.platforms.add(platform)
            self.all_sprites.add(platform)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.game_won:
                self.reset_game()
            
        # Handle continuous keyboard input
        if not self.game_won:
            keys = pygame.key.get_pressed()
            self.player.velocity_x = 0
            if keys[pygame.K_LEFT]:
                self.player.velocity_x = -PLAYER_SPEED
            if keys[pygame.K_RIGHT]:
                self.player.velocity_x = PLAYER_SPEED

    def update(self):
        if not self.game_won:
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
                        self.player.velocity_y = JUMP_FORCE
                        
                        if lowest.type == "fragile":
                            lowest.kill()

            # Move screen down when player reaches upper third
            if self.player.rect.top <= SCREEN_HEIGHT // 3:
                self.player.rect.y += abs(self.player.velocity_y)
                for platform in self.platforms:
                    platform.rect.y += abs(self.player.velocity_y)
                    if platform.rect.top >= SCREEN_HEIGHT:
                        platform.kill()
                        self.score += 10
                        
                        # Check for win condition
                        if self.score >= 500:
                            self.game_won = True
                            return
                        
                        # Create new platform at the top
                        platform_type = random.choice(["normal", "moving", "fragile"])
                        new_platform = Platform(
                            random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH),
                            random.randint(-50, 0),
                            platform_type
                        )
                        self.platforms.add(new_platform)
                        self.all_sprites.add(new_platform)

            # Check for game over
            if self.player.rect.top > SCREEN_HEIGHT:
                self.high_score = max(self.score, self.high_score)
                self.reset_game()

    def reset_game(self):
        self.score = 0
        self.game_won = False
        self.all_sprites.empty()
        self.platforms.empty()
        self.player = Player()
        self.all_sprites.add(self.player)
        
        # Create ground platform
        ground = Platform(0, SCREEN_HEIGHT - PLATFORM_HEIGHT, "ground")
        self.platforms.add(ground)
        self.all_sprites.add(ground)
        
        self.generate_platforms()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        high_score_text = font.render(f'High Score: {self.high_score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(high_score_text, (10, 40))
        
        # Draw win message
        if self.game_won:
            win_font = pygame.font.Font(None, 72)
            win_text = win_font.render('YOU WIN!', True, YELLOW)
            win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(win_text, win_rect)
            
            restart_font = pygame.font.Font(None, 36)
            restart_text = restart_font.render('Press SPACE to play again', True, WHITE)
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
    game = Game()
    game.run()
