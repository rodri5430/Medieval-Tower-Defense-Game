import pygame
import math
import time

sprite_size = 70
towersData = [
    {"range": 170, "cooldown": 0, "cost": 50},
    {"range": 150, "cooldown": 700, "cost": 150},
    {"range": 180, "cooldown": 500, "cost": 300},
]

class Towers(pygame.sprite.Sprite):
    def __init__(self, images, pos):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y = pos
        self.images = images
        self.frame = 0
        self.lastUpgrade = time.time()
        self.target = None
        
        self.upgradeLvl = 0     
        self.towerCost = towersData[self.upgradeLvl]["cost"]
        self.range = towersData[self.upgradeLvl]["range"]
        self.cooldown = towersData[self.upgradeLvl]["cooldown"]
        
        self.anime = [self.slicing(image) for image in self.images]
        self.frame = 0
        self.image = self.anime[self.upgradeLvl][self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
    def slicing(self, image):
        anime = []
        for i in range(0, 4):
            x = i * 70
            anime.append(image.subsurface((x, 0, sprite_size, sprite_size)))
        return anime
    
    def update(self): #Here we only can do the tower animation and not call the upgradeLevel function, because that its just called when the player clicks upgrade button
            now = time.time()
            if now - self.lastUpgrade > 0.2:
                self.frame += 1
            if self.frame >= len(self.anime[self.upgradeLvl]):
                return
            self.image = self.anime[self.upgradeLvl][self.frame]
            self.lastUpgrade = now
                  
    def upgradeLevel(self): 
        #Here we update the Tower's range and cooldown that are taken from towersData
        if self.upgradeLvl + 1 < len(towersData):
            self.upgradeLvl += 1
            print(self.upgradeLvl)
            self.range = towersData[self.upgradeLvl]["range"]
            self.cooldown = towersData[self.upgradeLvl]["cooldown"]
            self.towerCost = towersData[self.upgradeLvl]["cost"]
 
    def pick_target(self, enemy_group):
        x_dist = 0
        y_dist = 0
        for enemy in enemy_group:
            x_dist = enemy.pos.x - self.x
            y_dist = enemy.pos.y - self.y
            dist = math.sqrt(x_dist ** 2 + y_dist ** 2) #In thins calcule we use Pythagorean Theorem in the Cartasian plane to calculate the distance between the tower and the enemy
            if dist < self.range:
                self.target = enemy