import pygame

class Nebula:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)
        self.size = size
        self.sprite = pygame.transform.scale(pygame.image.load("assets/images/nebula sprite.png"), (size, size))
        # Define a smaller collision rectangle
        self.collision_rect = pygame.Rect(x + size * 0.1, y + size * 0.1, size * 0.8, size * 0.8)

    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.x, self.rect.y))

    def update(self):
        # Update logic for the nebula
        pass