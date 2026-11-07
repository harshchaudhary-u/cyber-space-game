import pygame
import math
import random
import sys

# Pygame initialize
pygame.init()

# Screen Setup
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🔴 PROTOCOL X-101 // CYBERNETIC HUD")
clock = pygame.time.Clock()

# Neon Color Palette
BLACK = (5, 5, 10)
CYAN = (0, 255, 240)
NEON_GREEN = (57, 255, 20)
RED = (255, 0, 85)
DARK_BLUE = (10, 20, 45)
WHITE = (255, 255, 255)

# Fonts
font = pygame.font.SysFont("Courier New", 14, bold=True)
large_font = pygame.font.SysFont("Courier New", 22, bold=True)

# Particle System (Floating cyber dust)
class Particle:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed = random.uniform(0.6, 2.0)
        self.size = random.randint(1, 3)
        self.alpha = random.randint(80, 220)

    def update(self):
        self.y -= self.speed
        if self.y < 0:
            self.y = HEIGHT
            self.x = random.randint(0, WIDTH)

    def draw(self, surface):
        s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (0, 255, 240, self.alpha), (self.size, self.size), self.size)
        surface.blit(s, (self.x, self.y))

particles = [Particle() for _ in range(55)]
angle = 0
grid_offset = 0

def draw_cyber_grid(surface):
    """Dynamic background grid"""
    global grid_offset
    grid_offset = (grid_offset + 0.4) % 40
    for x in range(0, WIDTH, 40):
        pygame.draw.line(surface, (12, 28, 50), (x, 0), (x, HEIGHT), 1)
    for y in range(int(grid_offset), HEIGHT, 40):
        pygame.draw.line(surface, (12, 28, 50), (0, y), (WIDTH, y), 1)

def draw_hud(surface, center, angle_offset):
    """Spinning concentric HUD rings"""
    # Outer dashed ring
    for i in range(0, 360, 15):
        rad = math.radians(i + angle_offset)
        sx = center[0] + 165 * math.cos(rad)
        sy = center[1] + 165 * math.sin(rad)
        ex = center[0] + 180 * math.cos(rad)
        ey = center[1] + 180 * math.sin(rad)
        pygame.draw.line(surface, CYAN, (sx, sy), (ex, ey), 2)

    # Middle circular bracket
    pygame.draw.circle(surface, DARK_BLUE, center, 140, 6)
    pygame.draw.circle(surface, RED, center, 140, 1)

    # Inner reverse rotating nodes
    for i in range(0, 360, 45):
        rad = math.radians(i - angle_offset * 1.6)
        x = center[0] + 100 * math.cos(rad)
        y = center[1] + 100 * math.sin(rad)
        pygame.draw.circle(surface, NEON_GREEN, (int(x), int(y)), 4)

    # Glowing center core
    pygame.draw.circle(surface, RED, center, 9)
    pygame.draw.circle(surface, WHITE, center, 3)

def render_diagnostics(surface):
    """Side diagnostic stats"""
    stats = [
        "SYS_STATUS: ONLINE",
        "KERNEL: v3.12-x64",
        f"CORE_TEMP: {random.randint(42, 47)}C",
        f"RUN_TIME: {pygame.time.get_ticks() // 1000}s",
        "NEURAL_LINK: SYNCED",
        f"LATENCY: {random.randint(11, 18)}ms"
    ]
    for idx, text in enumerate(stats):
        surface.blit(font.render(text, True, NEON_GREEN), (35, 50 + idx * 26))

    # Blinking Warning Header
    if (pygame.time.get_ticks() // 500) % 2 == 0:
        surface.blit(large_font.render("SYSTEM LOCKDOWN // ACTIVE", True, RED), (WIDTH // 2 - 165, 45))

# Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    screen.fill(BLACK)

    # 1. Background Grid & Particles
    draw_cyber_grid(screen)
    for p in particles:
        p.update()
        p.draw(screen)

    # 2. Main Center HUD
    angle += 1
    center = (WIDTH // 2, HEIGHT // 2 + 35)
    draw_hud(screen, center, angle)

    # 3. Corner Sci-Fi Brackets
    pygame.draw.lines(screen, CYAN, False, [(25, 95), (25, 25), (95, 25)], 3)
    pygame.draw.lines(screen, CYAN, False, [(WIDTH - 95, HEIGHT - 25), (WIDTH - 25, HEIGHT - 25), (WIDTH - 25, HEIGHT - 95)], 3)

    # 4. Text Overlay
    render_diagnostics(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
