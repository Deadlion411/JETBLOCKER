import pygame
import random
from player import Player
from asteroid import Asteroid
from nebula import Nebula
from utils import random_asteroid_generation, generate_coins, generate_nebulas, generate_health_packs, check_coin_collision, check_health_pack_collision, check_nebula_collision, check_asteroid_collision, draw_asteroids, draw_coins, draw_nebulas, draw_health_packs, draw_health_bar, display_title_screen, display_start_screen, display_game_over_screen
from coin import Coin
from health_pack import HealthPack
pygame.init()

screen = pygame.display.set_mode([800, 600])
clock = pygame.time.Clock()

# Initialize the mixer
pygame.mixer.init()

# Load and play the background music
pygame.mixer.music.load("assets/sounds/Bg music.mp3")
pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely
pygame.mixer.music.set_volume(0.5)

# Load the background image
background = pygame.image.load("assets/images/space background.png")
background = pygame.transform.scale(background, (800, 600))  # Resize background

# Load the player sprites
player_idle_sprite = pygame.image.load("assets/images/idle square.png")
player_moving_sprite = pygame.image.load("assets/images/player character.png")

# Load and resize the coin sprite
coin_sprite = pygame.image.load("assets/images/coin image.png")
coin_sprite = pygame.transform.scale(coin_sprite, (35, 30))  # Resize to 35x30 pixels

# Load the asteroid sprite
asteroid_sprite = pygame.image.load("assets/images/asteroid image.png")
asteroid_sprite = pygame.transform.scale(asteroid_sprite, (80, 80))  # Resize to 80x80 pixels

# Load and resize the debris sprite
debris_sprite = pygame.image.load("assets/images/debris sprite.png")
debris_sprite = pygame.transform.scale(debris_sprite, (125, 70))  # Resize to 125x70 pixels

# Load and resize the nebula sprite
nebula_sprite = pygame.image.load("assets/images/nebula sprite.png")
nebula_sprite = pygame.transform.scale(nebula_sprite, (80, 80))  # Resize to 80x80 pixels

# Load the startup screen images
startup_screen_images = [
    pygame.image.load("assets/images/start up screen 1.jpg"),
    pygame.image.load("assets/images/start up screen 2.png")
]
startup_screen_images = [pygame.transform.scale(img, (800, 600)) for img in startup_screen_images]  # Resize to fit the screen

# Load the button image
button_image = pygame.image.load("assets/images/button image.png")
button_image = pygame.transform.scale(button_image, (100, 100))  # Resize button image

# Load the health pack image
health_pack_image = pygame.image.load("assets/images/health pack.png")
health_pack_image = pygame.transform.scale(health_pack_image, (35, 35))  # Resize to 35x35 pixels

# Load the game over screen image
game_over_screen_image = pygame.image.load("assets/images/game over screen.jpg")
game_over_screen_image = pygame.transform.scale(game_over_screen_image, (800, 600))  # Resize to fit the screen

# Load sound effects
collision_sound = pygame.mixer.Sound("assets/sounds/collision sound.mp3")
game_over_sound = pygame.mixer.Sound("assets/sounds/game over sound.mp3")
coin_sound = pygame.mixer.Sound("assets/sounds/coin sound.mp3")
health_pack_sound = pygame.mixer.Sound("assets/sounds/health pack sound.mp3")

def reset_level(level):
    asteroids = random_asteroid_generation()
    coins = generate_coins(level, asteroids, [])
    nebulas = generate_nebulas(5, asteroids)
    health_packs = generate_health_packs(3)
    return asteroids, coins, nebulas, health_packs

def reset_game():
    global level, player, asteroids, coins, nebulas, health_packs
    level = 1
    asteroids, coins, nebulas, health_packs = reset_level(level)
    player = Player(400, 300, 50, 50, 5, asteroids)

def main():
    global keep_going, level, player, asteroids, coins, nebulas, health_packs
    keep_going = True
    reset_game()

    display_title_screen(screen, startup_screen_images, button_image)
    display_start_screen(screen, background, asteroids, coins, player, nebulas, health_packs)

    while keep_going:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False

        player.move(asteroids)
        collected_coins = check_coin_collision(player, coins, coin_sound)
        if collected_coins > 0 and len(coins) == 0:  # Win condition: all coins collected
            level += 1
            asteroids, coins, nebulas, health_packs = reset_level(level)

        check_health_pack_collision(player, health_packs, health_pack_sound)
        if check_nebula_collision(player, nebulas):
            player.health -= 1  # Decrease health on collision with nebulas
            collision_sound.play()  # Play collision sound
        if check_asteroid_collision(player, asteroids):
            player.health -= 1  # Decrease health on collision with asteroids
            collision_sound.play()  # Play collision sound

        if player.health <= 0:  # Game over condition
            display_game_over_screen(screen, game_over_screen_image, game_over_sound)
            reset_game()

        for asteroid in asteroids:
            asteroid.update()
        for nebula in nebulas:
            nebula.update()

        screen.blit(background, (0, 0))
        draw_asteroids(screen, asteroids)
        draw_coins(screen, coins)
        draw_nebulas(screen, nebulas)
        draw_health_packs(screen, health_packs)
        player.draw(screen)
        draw_health_bar(screen, 10, 10, player.health, player.max_health)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()