import pygame
import random
import os
import sys

# --- EXE RESOURCE FINDER ---
def get_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

pygame.init()

# --- Window Setup ---
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Starship Voyager: Ultimate Edition")

# --- Set Window Icon ---
try:
    # This makes the little icon in the corner of the window match your ship
    window_icon = pygame.image.load(get_path('logo.ico'))
    pygame.display.set_icon(window_icon)
except:
    pass

clock = pygame.time.Clock()

# --- Global Fonts (Defined here so all states can use them) ---
font_big = pygame.font.SysFont("Impact", 60)
font_med = pygame.font.SysFont("Impact", 50)
font_small = pygame.font.SysFont("Arial", 24)
ui_font = pygame.font.SysFont("Arial", 20)

# --- Image Loading ---
def load_sprite(filename, size):
    try:
        img = pygame.image.load(get_path(filename)).convert()
        img.set_colorkey((255, 255, 255)) 
        return pygame.transform.scale(img, size)
    except:
        return None

player_img = load_sprite('plane.png', (60, 40))
enemy_img = load_sprite('enemy.png', (45, 45))

# --- Game Variables ---
stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(2, 5)] for _ in range(50)]
player_pos = [WIDTH // 2, HEIGHT - 70]
enemy_pos = [random.randint(0, WIDTH - 45), -50]
enemy_speed = 4
bullets = []
score = 0
level = 1
bg_colors = [(5, 5, 20), (25, 5, 40), (5, 30, 20), (40, 5, 5)]
current_bg = bg_colors[0]
game_state = "MENU"
triple_shot_timer = 0

def reset_game():
    global score, level, enemy_speed, player_pos, bullets, triple_shot_timer, current_bg, enemy_pos
    score = 0
    level = 1
    enemy_speed = 4
    player_pos = [WIDTH // 2, HEIGHT - 70]
    enemy_pos = [random.randint(0, WIDTH - 45), -50]
    bullets = []
    triple_shot_timer = 0
    current_bg = bg_colors[0]

# --- Main Game Loop ---
while True:
    screen.fill(current_bg)
    
    # 1. Background Stars
    for star in stars:
        star[1] += star[2]
        if star[1] > HEIGHT: star[1] = 0
        pygame.draw.circle(screen, (200, 200, 200), (star[0], star[1]), 1)

    # 2. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if game_state == "MENU" and event.key == pygame.K_SPACE:
                reset_game()
                game_state = "PLAYING"
            elif game_state == "GAMEOVER" and event.key == pygame.K_r:
                reset_game()
                game_state = "PLAYING"
            elif game_state == "PLAYING" and event.key == pygame.K_SPACE:
                if triple_shot_timer > 0:
                    bullets.append([player_pos[0] + 5, player_pos[1] + 10])
                    bullets.append([player_pos[0] + 28, player_pos[1]])
                    bullets.append([player_pos[0] + 50, player_pos[1] + 10])
                else:
                    bullets.append([player_pos[0] + 28, player_pos[1]])

    # 3. Game State Logic
    if game_state == "MENU":
        title = font_big.render("STARSHIP VOYAGER", True, (0, 255, 255))
        start = font_small.render("PRESS SPACE TO START", True, (255, 255, 255))
        screen.blit(title, (WIDTH//2 - 200, HEIGHT//2 - 60))
        screen.blit(start, (WIDTH//2 - 110, HEIGHT//2 + 20))

    elif game_state == "PLAYING":
        level = (score // 100) + 1
        enemy_speed = 4 + (level * 0.5)
        current_bg = bg_colors[(level - 1) % len(bg_colors)]

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0: player_pos[0] -= 7
        if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - 60: player_pos[0] += 7

        if triple_shot_timer > 0: triple_shot_timer -= 1
        for b in bullets[:]:
            b[1] -= 10
            color = (0, 255, 255) if triple_shot_timer > 0 else (255, 255, 0)
            pygame.draw.rect(screen, color, (b[0], b[1], 4, 10))
            if b[1] < 0: bullets.remove(b)

        enemy_pos[1] += enemy_speed
        enemy_rect = pygame.Rect(enemy_pos[0], enemy_pos[1], 45, 45)
        if enemy_pos[1] > HEIGHT:
            enemy_pos = [random.randint(0, WIDTH - 45), -50]

        for b in bullets[:]:
            if enemy_rect.collidepoint(b[0], b[1]):
                if b in bullets: bullets.remove(b)
                enemy_pos = [random.randint(0, WIDTH - 45), -50]
                score += 10
                if score % 100 == 0: triple_shot_timer = 300 

        if player_img: screen.blit(player_img, (player_pos[0], player_pos[1]))
        if enemy_img: screen.blit(enemy_img, (enemy_pos[0], enemy_pos[1]))
        
        player_rect = pygame.Rect(player_pos[0], player_pos[1], 60, 40)
        if player_rect.colliderect(enemy_rect):
            game_state = "GAMEOVER"

        info = ui_font.render(f"Score: {score}  |  Level: {level}", True, (255, 255, 255))
        screen.blit(info, (10, 10))

    elif game_state == "GAMEOVER":
        msg = font_med.render(f"FINAL SCORE: {score}", True, (255, 50, 50))
        retry = font_small.render("PRESS R TO RETRY", True, (255, 255, 255))
        screen.blit(msg, (WIDTH//2 - 140, HEIGHT//2 - 30))
        screen.blit(retry, (WIDTH//2 - 80, HEIGHT//2 + 40))

    pygame.display.update()
    clock.tick(60)