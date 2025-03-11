import pygame
import random

class Player:
    def __init__(self, x, y, width, height, velocity, asteroids, health=100):
        self.rect = pygame.Rect(x, y, width, height)
        self.width = width
        self.height = height
        self.velocity = velocity
        self.gravity = 0.5
        self.y_velocity = 0
        self.on_ground = False
        self.rect = pygame.rect.Rect(x, y, self.width, self.height)
        self.idle_sprite = pygame.transform.scale(pygame.image.load("assets/images/idle square.png"), (self.width, self.height))
        self.moving_sprite = pygame.transform.scale(pygame.image.load("assets/images/player character.png"), (self.width, self.height))
        self.sprite = self.idle_sprite
        self.direction = "right"  # Initial direction
        self.health = health  # Initial health
        self.max_health = 100  # Maximum health
        
        # Define a smaller collision rectangle
        self.collision_rect = pygame.rect.Rect(x + 10, y + 10, self.width - 20, self.height - 20)
        
        # Ensure the player does not spawn into asteroids
        while any(self.rect.colliderect(asteroid.collision_rect) for asteroid in asteroids):
            x = random.randint(0, 800 - self.width)
            y = random.randint(0, 600 - self.height)
            self.rect.topleft = (x, y)
            self.collision_rect.topleft = (x + 10, y + 10)
        
        self.x = self.rect.x
        self.y = self.rect.y

    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.x, self.rect.y))

    def move(self, asteroids):
        keys = pygame.key.get_pressed()
        new_x = self.x
        new_y = self.y
        moving = False

        if keys[pygame.K_a] and self.x - self.velocity >= 0:
            new_x -= self.velocity
            moving = True
            self.direction = "left"
        if keys[pygame.K_d] and self.x + self.velocity + self.width <= 800:
            new_x += self.velocity
            moving = True
            self.direction = "right"
        if keys[pygame.K_w]:
            new_y -= self.velocity
            moving = True

        # Apply gravity only when not pressing W
        if not keys[pygame.K_w]:
            self.y_velocity += self.gravity
            new_y += self.y_velocity
        else:
            self.y_velocity = 0

        new_rect = pygame.rect.Rect(new_x, new_y, self.width, self.height)
        new_collision_rect = pygame.rect.Rect(new_x + 10, new_y + 10, self.width - 20, self.height - 20)
        
        # Check for collision with asteroids
        collision_index = new_collision_rect.collidelist([asteroid.collision_rect for asteroid in asteroids])
        if collision_index == -1:
            self.x = new_x
            self.y = new_y
            self.rect.topleft = (self.x, self.y)
            self.collision_rect.topleft = (self.x + 10, self.y + 10)

        # Ensure the player stays within the screen bounds
        if self.rect.y + self.rect.height >= 600:
            self.rect.y = 600 - self.rect.height
            self.y_velocity = 0
            self.on_ground = True
        else:
            self.on_ground = False

        self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height))
        self.collision_rect.topleft = (self.rect.x + 10, self.rect.y + 10)

        # Update sprite based on movement and direction
        if moving:
            self.sprite = self.moving_sprite
            if self.direction == "left":
                self.sprite = pygame.transform.flip(self.moving_sprite, True, False)
            else:
                self.sprite = self.moving_sprite
        else:
            self.sprite = self.idle_sprite
            if self.direction == "left":
                self.sprite = pygame.transform.flip(self.idle_sprite, True, False)
            else:
                self.sprite = self.idle_sprite

    def get_rect(self):
        return self.rect