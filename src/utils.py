import pygame
import random
from asteroid import Asteroid
from coin import Coin
from health_pack import HealthPack
from nebula import Nebula

def display_title_screen(screen, startup_screen_images, button_image):
    startup_screen_image = random.choice(startup_screen_images)  # Randomly choose a startup screen image
    screen.blit(startup_screen_image, (0, 0))  # Draw the startup screen image
    button_rect = button_image.get_rect(center=(400, 500))  # Center the button
    screen.blit(button_image, button_rect.topleft)  # Draw the button
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False

def display_start_screen(screen, background, asteroids, coins, player, nebulas, health_packs):
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))  # Draw the background image
    draw_asteroids(screen, asteroids)
    draw_coins(screen, coins)
    draw_nebulas(screen, nebulas)
    draw_health_packs(screen, health_packs)
    player.draw(screen)
    font = pygame.font.Font(None, 74)
    text = font.render("Press any key to start", True, (0, 255, 0))
    text_rect = text.get_rect(center=(400, 300))
    screen.blit(text, text_rect)
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def display_game_over_screen(screen, game_over_screen_image, game_over_sound):
    screen.blit(game_over_screen_image, (0, 0))  # Draw the game over screen image
    game_over_sound.play()  # Play game over sound
    pygame.display.update()
    pygame.time.wait(2000)
    game_over_sound.stop()  # Stop game over sound

def draw_health_bar(screen, x, y, health, max_health):
    bar_width = 200
    bar_height = 20
    fill = (health / max_health) * bar_width
    border_color = (255, 255, 255)
    fill_color = (0, 255, 0)
    pygame.draw.rect(screen, border_color, (x, y, bar_width, bar_height), 2)
    pygame.draw.rect(screen, fill_color, (x, y, fill, bar_height))

def draw_asteroids(screen, asteroids):
    for asteroid in asteroids:
        asteroid.draw(screen)

def draw_coins(screen, coins):
    for coin in coins:
        coin.draw(screen)

def draw_nebulas(screen, nebulas):
    for nebula in nebulas:
        nebula.draw(screen)

def draw_health_packs(screen, health_packs):
    for health_pack in health_packs:
        health_pack.draw(screen)

def check_coin_collision(player, coins, coin_sound):
    collected_coins = 0
    for coin in coins[:]:
        if player.get_rect().colliderect(coin.collision_rect):
            coins.remove(coin)
            collected_coins += 1
            coin_sound.play()  # Play coin sound
    return collected_coins

def check_nebula_collision(player, nebulas):
    for nebula in nebulas:
        if player.get_rect().colliderect(nebula.collision_rect):
            return True
    return False

def check_asteroid_collision(player, asteroids):
    for asteroid in asteroids:
        if player.get_rect().colliderect(asteroid.collision_rect):
            asteroid.push_player_away(player)
            return True
    return False

def check_health_pack_collision(player, health_packs, health_pack_sound):
    for health_pack in health_packs[:]:
        if player.get_rect().colliderect(health_pack.collision_rect):
            health_packs.remove(health_pack)
            player.health = min(player.health + 20, player.max_health)  # Increase health but not above max health
            health_pack_sound.play()  # Play health pack sound

def random_asteroid_generation(speed_factor=0.01):
    asteroids = []
    for _ in range(10):
        x = random.randint(0, 750)
        y = random.randint(0, 550)
        size = random.randint(30, 60)
        sprite = pygame.image.load("assets/images/asteroid image.png") if random.random() < 0.5 else pygame.image.load("assets/images/debris sprite.png")
        sprite = pygame.transform.scale(sprite, (size, size))
        asteroids.append(Asteroid(x, y, size, speed_factor, sprite))
    return asteroids

def generate_coins(num_coins, asteroids, nebulas):
    coins = []
    for _ in range(num_coins):
        while True:
            x = random.randint(10, 755)
            y = random.randint(10, 570)
            coin = Coin(x, y, 35, 30)
            if not any(coin.collision_rect.colliderect(asteroid.collision_rect) for asteroid in asteroids) and not any(coin.collision_rect.colliderect(nebula.collision_rect) for nebula in nebulas):
                coins.append(coin)
                break
    return coins

def generate_nebulas(num_nebulas, asteroids):
    nebulas = []
    for _ in range(num_nebulas):
        while True:
            x = random.randint(0, 760)
            y = random.randint(0, 560)
            nebula = Nebula(x, y, 80)
            if not any(nebula.collision_rect.colliderect(a.collision_rect) for a in asteroids):
                nebulas.append(nebula)
                break
    return nebulas

def generate_health_packs(num_health_packs):
    health_packs = []
    for _ in range(num_health_packs):
        while True:
            x = random.randint(10, 755)
            y = random.randint(10, 570)
            health_pack = HealthPack(x, y, 35, 35)
            health_packs.append(health_pack)
            break
    return health_packs