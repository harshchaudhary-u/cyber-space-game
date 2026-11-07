import pygame
import random
import math
import sys

# Pygame initialize
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CYBER-DODGE 2099 // NEON BLOW")
clock = pygame.time.Clock()

# High-contrast bright colors (Taaki black screen ka doubt hi na rahe)
BG_COLOR = (10, 10, 26)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 128)
YELLOW = (255, 230, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 100)

# Default safe font
game_font = pygame.font.Font(None, 32)
title_font = pygame.font.Font(None, 52)

# Stars Background
stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(2, 5)] for _ in range(60)]

# Player setup
player_x = WIDTH // 2
player_y = HEIGHT - 70
player_speed = 8
score = 0
lives = 3
game_over = False

# Lasers and Hazards
lasers = []
hazards = []
particles = []

def spawn_hazard():
    hx = random.randint(30, WIDTH - 30)
    speed = random.uniform(3.0, 6.0)
    size = random.randint(18, 30)
    color = random.choice([MAGENTA, YELLOW, (255, 100, 0)])
    return [hx, -30, speed, size, color]

# Initial hazards
for _ in range(5):
    hazards.append(spawn_hazard())

# Main Game Loop
while True:
    clock.tick(60)

    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_SPACE and not game_over:
                # Shoot laser
                lasers.append([player_x, player_y - 20])
            if event.key == pygame.K_r and game_over:
                # Restart
                player_x = WIDTH // 2
                lives = 3
                score = 0
                hazards = [spawn_hazard() for _ in range(5)]
                lasers.clear()
                particles.clear()
                game_over = False

    # 2. Controls & Movement
    if not game_over:
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_x > 30:
            player_x -= player_speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_x < WIDTH - 30:
            player_x += player_speed

        # Update Lasers
        for laser in lasers[:]:
            laser[1] -= 10
            if laser[1] < 0:
                lasers.remove(laser)

        # Update Hazards
        for h in hazards:
            h[1] += h[2]  # Move down
            
            # Laser Collision Check
            for laser in lasers[:]:
                dist = math.hypot(h[0] - laser[0], h[1] - laser[1])
                if dist < h[3] + 10:
                    # Explode
                    for _ in range(12):
                        particles.append([h[0], h[1], random.uniform(-4, 4), random.uniform(-4, 4), random.choice([YELLOW, MAGENTA, CYAN]), 20])
                    score += 50
                    if laser in lasers:
                        lasers.remove(laser)
                    # Reset hazard
                    h[0] = random.randint(30, WIDTH - 30)
                    h[1] = random.randint(-100, -20)
                    break

            # Player Collision Check
            p_dist = math.hypot(h[0] - player_x, h[1] - player_y)
            if p_dist < h[3] + 16:
                lives -= 1
                for _ in range(20):
                    particles.append([player_x, player_y, random.uniform(-5, 5), random.uniform(-5, 5), MAGENTA, 25])
                h[0] = random.randint(30, WIDTH - 30)
                h[1] = random.randint(-100, -20)
                if lives <= 0:
                    game_over = True

            # Screen bottom reset
            if h[1] > HEIGHT + 40:
                h[0] = random.randint(30, WIDTH - 30)
                h[1] = random.randint(-80, -20)

    # Update Particles
    for p in particles[:]:
        p[0] += p[2]
        p[1] += p[3]
        p[5] -= 1
        if p[5] <= 0:
            particles.remove(p)

    # 3. Drawing Elements
    screen.fill(BG_COLOR)

    # Draw moving stars
    for s in stars:
        s[1] += s[2]
        if s[1] > HEIGHT:
            s[1] = 0
            s[0] = random.randint(0, WIDTH)
        pygame.draw.circle(screen, (100, 150, 255), (s[0], s[1]), 2)

    # Draw Particles
    for p in particles:
        pygame.draw.circle(screen, p[4], (int(p[0]), int(p[1])), 4)

    # Draw Lasers
    for laser in lasers:
        pygame.draw.rect(screen, CYAN, (laser[0] - 3, laser[1], 6, 16))
        pygame.draw.circle(screen, WHITE, (laser[0], laser[1]), 4)

    # Draw Hazards (Glowing Rings & Core)
    for h in hazards:
        pygame.draw.circle(screen, h[4], (int(h[0]), int(h[1])), h[3])
        pygame.draw.circle(screen, BG_COLOR, (int(h[0]), int(h[1])), max(3, h[3] - 5))
        pygame.draw.circle(screen, WHITE, (int(h[0]), int(h[1])), 4)

    # Draw Player Spacecraft
    if not game_over:
        # Thruster fire
        flame_h = random.randint(8, 16)
        pygame.draw.polygon(screen, YELLOW, [(player_x - 6, player_y + 15), (player_x + 6, player_y + 15), (player_x, player_y + 15 + flame_h)])
        
        # Ship Triangle
        pts = [(player_x, player_y - 20), (player_x - 20, player_y + 15), (player_x + 20, player_y + 15)]
        pygame.draw.polygon(screen, CYAN, pts)
        pygame.draw.polygon(screen, WHITE, pts, 2)
        pygame.draw.circle(screen, MAGENTA, (player_x, player_y), 5)

    # 4. HUD / Text Display
    score_txt = game_font.render(f"SCORE: {score}", True, WHITE)
    screen.blit(score_txt, (20, 20))

    lives_txt = game_font.render(f"LIVES: {'❤️ ' * lives}", True, MAGENTA)
    screen.blit(lives_txt, (WIDTH - 180, 20))

    # Controls hint at bottom
    tip_txt = game_font.render("A/D or Arrows: Move | SPACE: Shoot", True, (120, 140, 180))
    screen.blit(tip_txt, (WIDTH // 2 - tip_txt.get_width() // 2, HEIGHT - 30))

    # Game Over Overlay
    if game_over:
        over_surf = title_font.render("GAME OVER", True, MAGENTA)
        screen.blit(over_surf, (WIDTH // 2 - over_surf.get_width() // 2, HEIGHT // 2 - 40))
        restart_surf = game_font.render("Press 'R' to Restart", True, CYAN)
        screen.blit(restart_surf, (WIDTH // 2 - restart_surf.get_width() // 2, HEIGHT // 2 + 20))

    pygame.display.flip()
