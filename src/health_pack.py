import pygame

class HealthPack:
    def __init__(self, x, y, width, height):
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.sprite = pygame.transform.scale(pygame.image.load("assets/images/health pack.png"), (width, height))
        self.collision_rect = pygame.rect.Rect(x + width * 0.1, y + height * 0.1, width * 0.8, height * 0.8)

    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.x, self.rect.y))