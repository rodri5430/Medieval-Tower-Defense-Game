'''
Name: Rodrigo Gonçalves 
UC: Multimedia e Computação Gráfica
File: main.py
Date: 2025
'''

#hexacolor toRgb on Google for colors
import pygame
import sys
import csv
import threading
import numpy as np
import time
from Towers import *
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
gameOverState = False
running = True
FPS = 60
showPos = False
timer = time.time()
initGameTimer = time.time()
gameOverTime = time.time()
work = 100
loadingFinished = False
loadingProgress = 0
loadingBarWidth = 8

#------ Player Settings ------
playerMoney = 100
playerLife = 50
    
#------ Pygame Init ------
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

pygame.display.set_caption(gameName)

screen = pygame.display.set_mode((screen_w, screen_h))

#ArialFont = pygame.font('Arial-sans', )
font = pygame.font.Font('game code/files/Fonte.ttf', 72)
buttonsFont = pygame.font.Font('game code/files/Fonte.ttf', 60)
MoneyFont = pygame.font.Font('game code/files/Fonte.ttf', 40)
loadingFont = pygame.font.Font('game code/files/Fonte.ttf', 60)
gameFont = pygame.font.Font('game code/files/Fonte.ttf', 30)
title = font.render(gameName, True, (0,0,0))

#------ Towers ------
towers_group = pygame.sprite.Group()
towersPositions = [
    (866, 225), (826, 60), (678, 322), (481, 446),
    (254, 160), (132, 60), (89, 225), (286, 319), 
    (481, 286), (705, 160)
]
towerSelected = None
showMessage = False

#------ Enemies ------
waypoints = { 
    #dictionay with waypoints that enemy will follow randomnly
    "path1": [(365, 607), (369, 239), (179, 239), (179, 144), (56, 146), (56, 0)],
    "path2": [(591, 611), (600, 237), (788, 237), (788, 143), (917, 143), (917, 0)]
}

enemy_group = pygame.sprite.Group()
waveLvl1 = ["rat", "rat", "knight", "wizard"]

#------ Towers Spawn ------
def SpawnTower():
    towersImagesList = [towerImageLvl1, towerImageLvl2, towerImageLvl3]
    
    for i in towersPositions:
        towers_group.add(Towers(towersImagesList, i))

#------ No Money Message ------
def noMoney():
    global initGameTimer, showMessage
    if showMessage:
        noMoneytimer = time.time()
        if noMoneytimer - initGameTimer <= 2:
            Nomoney = MoneyFont.render("You have no Money! Can't afford this tower Sorry :(", True, (255, 0, 0))
            screen.blit(Nomoney, (44, 357))
        else:
            showMessage = False

#------ Enemies Spawn ------
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
    
    loadingSurface.fill((144, 144, 144))
    
    screen.blit(loadingSurface, (0,0))
    
    loadingBackGround = pygame.image.load(loadingBarBackGroundPath)
    loadingBackGroundRect = loadingBackGround.get_rect(center=(518, 410))
    
    loadingBar = pygame.image.load(loadingBarPath)
    loadingBarWidth = loadingProgress / work * loadingBackGroundRect.w
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
    global loadingProgress, loadingFinished, sheet, tiles, rat, knight, wizard, ratDie, knightDie, wizardDie, towerImageLvl1, towerImageLvl2, towerImageLvl3

    #------ Images Load ------
    sheet = pygame.image.load("game code/assets/images/FieldsTileset.png").convert_alpha()
    loadingProgress += 8
    time.sleep(0.1)
    rat = [pygame.image.load("game code/assets/images/enemie1/D_Run.png"), pygame.image.load("game code/assets/images/enemie1/S_Run.png"), pygame.image.load("game code/assets/images/enemie1/U_Run.png")]
    loadingProgress += 8
    time.sleep(0.1)
    knight = [pygame.image.load("game code/assets/images/enemie2/D_Run.png"), pygame.image.load("game code/assets/images/enemie2/S_Run.png"), pygame.image.load("game code/assets/images/enemie2/U_Run.png")]
    loadingProgress += 8
    time.sleep(0.1)
    wizard = [pygame.image.load("game code/assets/images/enemie3/D_Fly.png"), pygame.image.load("game code/assets/images/enemie3/S_Fly.png"),  pygame.image.load("game code/assets/images/enemie3/U_Fly.png")]
    loadingProgress += 8
    time.sleep(0.1)
    ratDie = [pygame.image.load("game code/assets/images/enemie1/D_Death.png"), pygame.image.load("game code/assets/images/enemie1/S_Death.png"),  pygame.image.load("game code/assets/images/enemie1/U_Death.png")]
    loadingProgress += 8
    time.sleep(0.1)
    wizardDie = [pygame.image.load("game code/assets/images/enemie3/D_Death.png"), pygame.image.load("game code/assets/images/enemie3/S_Death.png"),  pygame.image.load("game code/assets/images/enemie3/U_Death.png")]
    loadingProgress += 8
    time.sleep(0.1)
    knightDie = [pygame.image.load("game code/assets/images/enemie2/D_Death.png"), pygame.image.load("game code/assets/images/enemie2/S_Death.png"), pygame.image.load("game code/assets/images/enemie2/U_Death.png")]
    loadingProgress += 8
    time.sleep(0.1)
    
    #------ Tower images Load ------ 
    towerImageLvl1 = pygame.image.load("game code/assets/images/Torres/1 Upgrade/1.png").convert_alpha()
    towerImageLvl2 = pygame.image.load("game code/assets/images/Torres/1 Upgrade/2.png").convert_alpha()
    towerImageLvl3 = pygame.image.load("game code/assets/images/Torres/1 Upgrade/3.png").convert_alpha()
    loadingProgress += 20
    time.sleep(0.1)
    
    #map tiles
    tiles = slicing(sheet, tile_size) #list that receives the cutted tiles, and after to draw game map
    loadingProgress += 24
    time.sleep(1)
    
    #load mapa
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
    global towerLvl
    
    superficieMenu = pygame.Surface((screen_w, screen_h))
    menuImage = pygame.image.load("game code/assets/images/MenuImagem.png").convert()
    menuImage = pygame.transform.scale(menuImage, (screen_w, screen_h))
    
    superficieMenu.blit(menuImage, (0, 0))
    superficieMenu.blit(title, (150, 75))
    
    Button1 = pygame.Rect(380, 250, 300, 100)
    Button2= pygame.Rect(380, 375, 300, 100)
    
    pygame.draw.rect(superficieMenu, (139, 69, 19), Button1, border_radius= 10) #Button 1
    pygame.draw.rect(superficieMenu, (139, 69, 19), Button2, border_radius= 10) #Button 2

    
    play = buttonsFont.render("Play", True, (245, 222, 179))
    leave = buttonsFont.render("Leave", True, (245, 222, 179))
    
    superficieMenu.blit(play, (Button1.x + 85, Button1.y + 15))
    superficieMenu.blit(leave, (Button2.x + 70, Button2.y + 15))
    
    mousePosition = pygame.mouse.get_pos()
    
    if Button1.collidepoint(mousePosition):
        Button1 = pygame.draw.rect(superficieMenu, (139, 69, 19), Button1, border_radius= 10)
       
    if Button1.collidepoint(mousePosition) and pygame.mouse.get_pressed()[0] == 1:
            state = "Level1"
            SpawnTower()
        
    elif Button2.collidepoint(mousePosition) and pygame.mouse.get_pressed()[0] == 1:
            running = False
            print("Leaving...")
        
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
    global buttonsFont, playerMoney, waveLvl1, towerSelected, showMessage, initGameTimer, Button, CancelButton, playerLife, surface, gameOverState, gameOverTime
    
    surface = pygame.Surface((screen_w, screen_h))
    surface.fill((100, 100, 100))
    
    for y in range(0, game_map_layer0.shape[0]):
        for x in range(game_map_layer0.shape[1]):
           surface.blit(tiles[int(game_map_layer0[y, x])], (y * tile_size, x * tile_size)) #Draw superficie
           
    Button = pygame.Rect(13, 658, 300, 100)
    pygame.draw.rect(surface, (245, 66, 66), Button, border_radius= 10)
    CancelButton = pygame.Rect(325, 600, 300, 100)
    pygame.draw.rect(surface, (139, 69, 19), CancelButton, border_radius= 10)
    
    upgrade = buttonsFont.render("Upgrade", True, (245, 222, 179))
    cancel = buttonsFont.render("Cancel", True, (245, 222, 179))
    surface.blit(upgrade, (Button.x + 45, Button.y + 15))
    surface.blit(cancel, (CancelButton.x + 40, CancelButton.y + 15))
    
    mousePos = pygame.mouse.get_pos()
    for tower in towers_group:
        tower.pick_target(enemy_group)
        if pygame.mouse.get_pressed()[0]:
            if tower.rect.collidepoint(mousePos):
                towerSelected = tower
    
    for enemy in enemy_group:
        if enemy.target_waypoints >= len(enemy.waypoints):
            playerLife -= enemy.damage
            
            if playerLife < 0: 
                #Life can not be negative
                playerLife = 0 
            print(playerLife)    
            
            if playerLife <= 0:
                gameOverState = True 
                gameOverTime = time.time()        
                               
    if len(waveLvl1) > 0:
        SpawnEnemy(waveLvl1[0], 8)
    
    enemy_group.update()
    enemy_group.draw(surface)
    
    towers_group.draw(surface)

    screen.blit(surface, (0,0))

    noMoney()
    GameOver()
#------ Game Over ------
def GameOver():
    global gameOverState, gameOverTimem, state, playerMoney
    timerGameOver = time.time()
    if gameOverState == True:
        if timerGameOver - gameOverTime <= 8:
            gameOverRect = pygame.Rect(322, 197, 315, 366) #I taked a photoprinted of the map with the size of gameOver Rect
            gameOver = gameFont.render("GAME OVER", True, (255, 0, 0))
            pygame.draw.rect(screen, (245, 66, 66), gameOverRect, border_radius = 10)
            screen.blit(gameOver, (356, 239))
            gameOver = gameFont.render(f"Money Earned: {playerMoney}", True, (255, 0, 0)) #FICA A PISCAR !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            pygame.display.flip()
            screen.blit(gameOver, (356, 400))
        else:
            state = "Menu"
            gameOverState = False
#------ Game Loop ------
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
            #------ Towers Upgrade ------
            #Here we do the tower update, in the past i was using get_pressed, but it was not indicated to this part because it cheks the mouse state every frame and if we get it pressed it will do the upgrade a lot of times and this event is better
            mousePos = pygame.mouse.get_pos()
            if towerSelected is not None:
                if Button.collidepoint(mousePos):
                    if towerSelected.towerCost <= playerMoney:
                        playerMoney -= towerSelected.towerCost
                        towerSelected.update()
                        towerSelected.upgradeLevel()
                        initGameTimer = time.time()
                        print("Tower Selected")
                    else:
                        showMessage = True
                        initGameTimer = time.time()
                if CancelButton.collidepoint(mousePos):
                        towerSelected = None
                        print("No Tower Selected")    
        elif event.type == pygame.KEYDOWN: #Here if we presse F2 print position
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
