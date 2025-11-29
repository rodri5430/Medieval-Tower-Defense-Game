import pygame
import sys
import csv
import threading
import numpy as np
import time
#from Towers import *
from Enemy import *
import random as rm

#------ Settings ------
screen_w = 1068
screen_h = 768
tile_size = 32 

path_csv = "game code/files/MapaTeste_Chao.csv"
path_menu = "game code/assets/images/MenuImagem.png"
gameName = "Medieval Tower Defense"
loadingBarBackGroundPath = "game code/assets/images/loading/Frames/LoadingBar02Frame_192x18.png"
loadingBarPath = "game code/assets/images/loading/Fill/LoadingBar02Fill_192x18.png"

state = "Loading"
running = True
FPS = 60
showPos = False
timer = time.time()
work = 100
loadingFinished = False
loadingProgress = 0
loadingBarWidth = 8
    
waveLvl1 = ["rat", "rat", "knight", "wizard"]

#------ Pygame Init ------
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

pygame.display.set_caption(gameName)

screen = pygame.display.set_mode((screen_w, screen_h))

font = pygame.font.Font('game code/files/Fonte.ttf', 72)
buttonsFont = pygame.font.Font('game code/files/Fonte.ttf', 60)
loadingFont = pygame.font.Font('game code/files/Fonte.ttf', 60)

title = font.render(gameName, True, (0,0,0))

surface = pygame.Surface((screen_w, screen_h))
surface.fill((100, 100, 100))


#------ Towers ------
towers_group = pygame.sprite.Group()

#------ Enemies ------
waypoints = { 
    #dictionay with waypoints that enemy will follow randomnly
    "path1": [(365, 607), (369, 239), (179, 239), (179, 144), (56, 146), (56, 0)],
    "path2": [(591, 611), (600, 237), (788, 237), (788, 143), (917, 143), (917, 0)]
}

enemy_group = pygame.sprite.Group()

def SpawnEnemy(EnemyTipe, cooldown):
    global timer #seconds
    if time.time() - timer > cooldown:
        if EnemyTipe == "rat":
            enemy_group.add(Rat(rat, ratDie,rm.choice(list(waypoints.values()))))
            waveLvl1.pop(0)
            timer = time.time()
        elif EnemyTipe == "knight":
            enemy_group.add(Knight(knight, knightDie, rm.choice(list(waypoints.values()))))
            waveLvl1.pop(0)
            timer = time.time()
        elif EnemyTipe == "wizard":
            enemy_group.add(Wizard(wizard, wizardDie, rm.choice(list(waypoints.values()))))
            waveLvl1.pop(0)
            timer = time.time()
         
#------ Loading ------
def Loading():
    global state, loadingFinished, loadingProgress
    
    loadingSurface = pygame.Surface((screen_w, screen_h))
    
    
    loadingSurface.fill("#90909077")
    
    screen.blit(loadingSurface, (0,0))
    
    loadingBackGround = pygame.image.load(loadingBarBackGroundPath)
    loadingBackGroundRect = loadingBackGround.get_rect(center=(518, 410))
    
    loadingBar = pygame.image.load(loadingBarPath)
    loadingBarWidth = loadingProgress /  work * loadingBackGroundRect.w
    scaledBar = pygame.transform.scale(loadingBar, (int(loadingBarWidth), loadingBar.get_height()))
    loadingBarRect = loadingBar.get_rect(midleft=(423, 410))
    
    screen.blit(loadingBackGround, loadingBackGroundRect)
    screen.blit(scaledBar, loadingBarRect)
    
    pygame.display.flip()
    
    if loadingFinished:
        global timer
        finished = buttonsFont.render("Loading Finished! Enjoy", True, (245, 222, 179))
        finishedRect = finished.get_rect(center=(518, 410))
        screen.fill("#90909077")
        screen.blit(finished, finishedRect)
        pygame.display.flip()
        time.sleep(1)
    
        timer = time.time()
        state = "Menu"
        
        
def progress():
    global loadingProgress, loadingFinished, sheet, loadingBackGround, loadingBar, tiles, rat, knight, wizard, ratDie, knightDie, wizardDie

    #------ Images Load ------
    sheet = pygame.image.load("game code/assets/images/FieldsTileset.png").convert_alpha()
    loadingProgress += 14
    time.sleep(1)
    rat = [pygame.image.load("game code/assets/images/enemie1/D_Run.png"), pygame.image.load("game code/assets/images/enemie1/S_Run.png"), pygame.image.load("game code/assets/images/enemie1/U_Run.png")]
    loadingProgress += 14
    time.sleep(1)
    knight = [pygame.image.load("game code/assets/images/enemie2/D_Run.png"), pygame.image.load("game code/assets/images/enemie2/S_Run.png"), pygame.image.load("game code/assets/images/enemie2/U_Run.png")]
    loadingProgress += 14
    time.sleep(1)
    wizard = [pygame.image.load("game code/assets/images/enemie3/D_Fly.png"), pygame.image.load("game code/assets/images/enemie3/S_Fly.png"),  pygame.image.load("game code/assets/images/enemie3/U_Fly.png")]
    loadingProgress += 14
    time.sleep(1)
    ratDie = [pygame.image.load("game code/assets/images/enemie1/D_Death.png"), pygame.image.load("game code/assets/images/enemie1/S_Death.png"),  pygame.image.load("game code/assets/images/enemie1/U_Death.png")]
    time.sleep(1)
    wizardDie = [pygame.image.load("game code/assets/images/enemie3/D_Death.png"), pygame.image.load("game code/assets/images/enemie3/S_Death.png"),  pygame.image.load("game code/assets/images/enemie3/U_Death.png")]
    loadingProgress += 14
    time.sleep(1)
    knightDie = [pygame.image.load("game code/assets/images/enemie2/D_Death.png"), pygame.image.load("game code/assets/images/enemie2/S_Death.png"), pygame.image.load("game code/assets/images/enemie2/U_Death.png")]
    loadingProgress += 14
    
    tiles = slicing(sheet, tile_size) #list that receives the cutted tiles, and after to draw game map
    loadingProgress += 14
    time.sleep(1)
    load_mapa(path_csv)
    loadingProgress = 100
    time.sleep(1)
    
    if loadingProgress == 100: 
        loadingFinished = True
            
threading.Thread(target=progress).start()        
    
#------ Menu ------
def Menu():
    #FALTA BOTAO DE SOM
    #Mudar estetica botoes ao passar rato
    global state
    global running
    
    superficieMenu = pygame.Surface((screen_w, screen_h))
    menuImage = pygame.image.load("game code/assets/images/MenuImagem.png").convert()
    menuImage = pygame.transform.scale(menuImage, (screen_w, screen_h))
    
    superficieMenu.blit(menuImage, (0, 0))
    superficieMenu.blit(title, (150, 75))
    
    Button1 = pygame.Rect(380, 250, 300, 100)
    Button2= pygame.Rect(380, 375, 300, 100)
    Button3= pygame.Rect(380, 500, 300, 100)
    
    pygame.draw.rect(superficieMenu, (139, 69, 19), Button1, border_radius= 10) #Button 1
    pygame.draw.rect(superficieMenu, (139, 69, 19), Button2, border_radius= 10) #Button 2
    pygame.draw.rect(superficieMenu, (139, 69, 19), Button3, border_radius = 10) #Button 3
    
    play = buttonsFont.render("Play", True, (245, 222, 179))
    leave = buttonsFont.render("Leave", True, (245, 222, 179))
    settings = buttonsFont.render("Settings", True, (245, 222, 179))
    
    superficieMenu.blit(play, (Button1.x + 85, Button1.y + 15))
    superficieMenu.blit(leave, (Button2.x + 70, Button2.y + 15))
    superficieMenu.blit(settings, (Button3.x + 55, Button3.y + 15))
    
    mousePosition = pygame.mouse.get_pos()
    
    if Button1.collidepoint(mousePosition):
        Button1 = pygame.draw.rect(superficieMenu, (139, 69, 19), Button1, border_radius= 10)
       
    if Button1.collidepoint(mousePosition) and pygame.mouse.get_pressed()[0] == 1:
            state = "Level1"
        
    elif Button2.collidepoint(mousePosition) and pygame.mouse.get_pressed()[0] == 1:
            running = False
            print("Leaving...")
        
    elif Button3.collidepoint(mousePosition) and pygame.mouse.get_pressed()[0] == 1:
            print("Settings") 
            #Here is the Setting function part that I´ll create if i have time
        
    screen.blit(superficieMenu, (0,0))
    
#------ Game Map ------        
def load_mapa(path):
    global game_map_layer0 
    with open(path, newline='') as f: #Opens CSV File
        reader = csv.reader(f) #Reads CSV File
        data = list(reader) #creates a list called data that contains all rows from the CSV file
        numCols = len(data) # data length
        numRows = len(data[0]) # data line 0 length 

    
    game_map_layer0 = np.zeros((numRows, numCols)) #Creation of a array 2D (Matrix)
    
    with open(path, 'r') as f: #Open CSV file only to read ('r')
        l = 0
        for line in f:
            values = line.split(",") # returns a array
            game_map_layer0[:,l] = np.array(values) #[:,l] All Rows, from l columns. Numpy Creates a array float64, so it puts a dot in each number 
            l += 1

def slicing(sheet, tile_size):
    largura = sheet.get_width() #get sheet width
    altura = sheet.get_height() #get sheet height
    tiles = [] #New list to receive map tiles
    
    for y in range(0, altura, tile_size):
        for x in range(0, largura, tile_size):
            square = sheet.subsurface(pygame.Rect(x, y, tile_size, tile_size)) #Cut the image to 32x32 pixels.
            tiles.append(square)
            
    return tiles

#------ Level 1 ------
def Level1():
    global waveLvl1
        
    for y in range(0, game_map_layer0.shape[0]):
        for x in range(game_map_layer0.shape[1]):
            surface.blit(tiles[int(game_map_layer0[y, x])], (y * tile_size, x * tile_size)) #Draw superficie

    if len(waveLvl1) > 0:
        SpawnEnemy(waveLvl1[0], 8)
    
    enemy_group.update()
    enemy_group.draw(surface)
     
    screen.blit(surface, (0,0))

#------ Game Loop ------
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN: #Here if we presse F2 print position
            if event.key == pygame.K_F2:
                showPos = not showPos
                
            if showPos:
                x, y = pygame.mouse.get_pos()
                print(x, y)
        
 
    if state == "Menu":
        
        Menu()
    elif state == "Loading":
        Loading()
    elif state == "Level1":
        Level1()
   
    
    pygame.display.flip()
pygame.quit()
sys.exit()
