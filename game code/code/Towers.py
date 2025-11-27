import pygame

class Towers(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image, 
        self.rect = self.image.get_rect()
        self.rect.center = pos
        
class TowerLevel1(Tower):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("game code/assets/images/Torres/Torre001.png"), 
        self.rect = self.image.get_rect()
        self.rect.center = pos
        
    def slicing(self, image, direction):
        anime = []
        for i in range(0, 6):
            x = i * 96
            anime.append(image.subsurface((x, 0, sprite_size, sprite_size))) #This cuts the rat sprite in 96x96 pixels
        return anime  