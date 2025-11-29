import pygame
from pygame.math import Vector2

sprite_size = 96

pygame.init()

#------ Enemies ------
class Enemy(pygame.sprite.Sprite):
    def __init__(self,waypoints):
        pygame.sprite.Sprite.__init__(self)
        self.now = 0
        self.lastTimer = 0
        self.time = 80 #frame velocity
        self.waypoints = waypoints
        self.target_waypoints = 1
        
    def update(self):
        self.now = pygame.time.get_ticks()
        self.move()
    def move(self):
        '''
        Here we create an IA path follow 
        that calculates the Character movement from initial position (first Waypoint) to the next target waypoint
        then it moves the character to there
        '''
        if self.target_waypoints < len(self.waypoints):# If the rat hasn't reached the last waypoint yet, keep moving
            self.target = Vector2(self.waypoints[self.target_waypoints])
            self.movement = self.target - self.pos
            self.x = self.movement.x
            self.y = self.movement.y
            
            if self.now - self.lastTimer > self.time: #We Used This a lot in TAC 
                self.frame += 1
                if self.frame > 5:
                    self.frame = 0
                self.lastTimer = self.now
                    
            if abs(self.x) > abs(self.y): #if the movement on x is higher than horizontal movement
                if self.x > 0: #if x positive it means that the character is moving right
                    self.dir = "right" 
                else: #here is the oposite
                    self.dir = "left" 
            else: 
                if self.y > 0: #if y positive it means that the character is moving up
                    self.dir = "down" 
                else: #here is the oposite
                    self.dir = "up"
            self.image = self.anime[self.dir][self.frame]
            
        else: 
            self.kill() #The Enemy reached the final waypoint
          
        dist = self.movement.length()
        
        if dist >= self.speed:
            self.pos += self.movement.normalize() * self.speed #Here, normalize() is a Vector2 method that performs trigonometric calculations. If we print only self.movement, it will return a 2D vector representing the distance between waypoint 1 and waypoint 2. Then we need to move the character using that vector, and that’s why we use Vector2.
            self.movement.normalize()
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
                
            self.target_waypoints += 1 
        self.rect = self.image.get_rect(center = (self.pos.x, self.pos.y))

#------ Rat ------
class Rat(Enemy): 
    #Here i used Heritance that we students learned on Programação Lessons, but in Java. Here the dad function (Enemy Class), uses son Class (Rato, Cavaleiro and Mago)'s variables and methods
    def __init__(self, images, imagesDie, waypoints):
        super().__init__(waypoints)
        self.imageD = images[0]
        self.imageS = images[1]
        self.imageU = images[2]
        self.imageA = pygame.transform.flip(self.imageU, True, False)
        self.rect = self.imageD.get_rect()        
        
        self.anime = {} #creates a dictionary
        self.life = 15
        self.speed = 1
        self.dir = "up" # character directions starts up
        self.frame = 0
        
        self.anime["up"] = self.slicing(self.imageU, "up")
        self.anime["left"] = self.slicing(self.imageS, "left")
        self.anime["down"]  = self.slicing(self.imageD, "down")
        self.anime["right"] = [pygame.transform.flip(i, True, False) for i in self.anime["left"]]
        
        self.image = self.anime[self.dir][self.frame]
        self.pos = Vector2(waypoints[0][0], waypoints[0][1])
        self.rect = self.image.get_rect(center = (self.pos.x, self.pos.y))
        
    def slicing(self, image, direction):
        anime = []
        for i in range(0, 6):
            x = i * 96
            anime.append(image.subsurface((x, 0, sprite_size, sprite_size))) #This cuts the rat sprite in 96x96 pixels
        return anime

#------ Knight ------ 
class Knight(Enemy): #Heritance
    def __init__(self, images, imagesDeath, waypoints):
        super().__init__(waypoints)
        self.imageD = images[0]
        self.imageS = images[1]
        self.imageU = images[2]
        self.imageA = pygame.transform.flip(self.imageU, True, False)
        self.rect = self.imageD.get_rect()        
        
        self.anime = {}
        self.life = 30
        self.speed = 1.15
        self.dir = "up" 
        self.frame = 0
        
        self.anime["up"] = self.slicing(self.imageU, "up")
        self.anime["left"] = self.slicing(self.imageS, "left")
        self.anime["down"]  = self.slicing(self.imageD, "down")
        self.anime["right"] = [pygame.transform.flip(i, True, False) for i in self.anime["left"]]
        
        self.image = self.anime[self.dir][self.frame]
        '''
        Here, we have our character animationm where we use a dictionary to alocate our game sprites ....!!!!!!!!!!CONTINUE
        '''
        self.pos = Vector2(waypoints[0][0], waypoints[0][1])
        self.rect = self.image.get_rect(center = (self.pos.x, self.pos.y))
        #self.image.center = self.pos
    def slicing(self, image, direction):
        anime = []
        for i in range(0, 6):
            x = i * 96
            anime.append(image.subsurface((x, 0, sprite_size, sprite_size))) #This cuts the rat sprite in 96x96 pixels
        return anime
    
class Wizard(Enemy): #Heritance
    def __init__(self, images, imagesDeath, waypoints):
        super().__init__(waypoints)
        self.imageD = images[0]
        self.imageS = images[1]
        self.imageU = images[2]
        self.imageA = pygame.transform.flip(self.imageU, True, False)
        self.rect = self.imageD.get_rect() 
        
        self.imageDDeath = imagesDeath[0]
        self.imagesSDeath = imagesDeath[1]
        self.imagesUDeath = imagesDeath[2]
        self.imageADeath = pygame.transform.flip(self.imageUDie, True, False)
               
        
        self.anime = {}
        self.life = 50
        self.money = 12
        self.speed = 1.3
        self.dir = "right" 
        self.frame = 0
        
        self.anime["up"] = self.slicing(self.imageU, "up")
        self.anime["left"] = self.slicing(self.imageS, "left")
        self.anime["down"]  = self.slicing(self.imageD, "down")
        self.anime["right"] = [pygame.transform.flip(i, True, False) for i in self.anime["left"]]
        
        self.image = self.anime[self.dir][self.frame]
        self.pos = Vector2(waypoints[0][0], waypoints[0][1])
        self.rect = self.image.get_rect(center = (self.pos.x, self.pos.y))
        
    def slicing(self, image, direction):
        anime = []
        for i in range(0, 6):
            x = i * 96
            anime.append(image.subsurface((x, 0, sprite_size, sprite_size))) #This cuts the rat sprite in 96x96 pixels
        return anime
    
    def takeDamage(self, damage):
        self.life -= damage
        if self.life < 0: # life cannot be negative, so the value if negative is alaways 0 
            self.life = 0 
            die()
            
    def die(self):
        anime = []
        for i in range(0, 6):
            x = i * 96
            anime.append(self.imagesDie.subsurface((x, 0, sprite_size, sprite_size))) #This cuts the rat sprite in 96x96 pixels
        return anime