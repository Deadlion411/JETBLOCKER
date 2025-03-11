import pygame
import random

class Asteroid:
    def __init__(self, x, y, size, speed_factor, sprite):
        self.rect = pygame.Rect(x, y, size, size)
        self.size = size
        self.speed_factor = speed_factor
        self.sprite = sprite
        # Define a smaller collision rectangle
        self.collision_rect = pygame.Rect(x + size * 0.1, y + size * 0.1, size * 0.8, size * 0.8)

    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.y += self.speed_factor
        if self.rect.y > 600:  # Reset position if it goes off screen
            self.rect.y = -self.size
            self.rect.x = random.randint(0, 800 - self.size)
        # Update the collision rectangle position
        self.collision_rect.topleft = (self.rect.x + self.size * 0.1, self.rect.y + self.size * 0.1)

    def push_player_away(self, player):
        # Logic to push the player away from the asteroid
        player.rect.x += 10  # Example push value