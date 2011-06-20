import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 800
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 40 #used to help us limit the frames per second
CIVSIZE = 20
ZOMSIZE = 20
ZOMSPEEDMIN = 5
ZOMSPEEDMAX = 8
ZOMSPAWNRATE = 6
ZOMSENSE = 120
CIVMOVERATE = 5
CIVQTY = 8
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
NULLRECT = pygame.Rect(0, 0, 0, 0)

def Terminate():
    pygame.quit()
    sys.exit()

def WaitForKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                Terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    Terminate()
                return

def ZomBite(c, zombies):
    for z in zombies:
        if c['rect'].colliderect(z['rect']):
            z['target'] = NULLRECT
            return True
    return False

def ZomMove(civies, zombies):
    for z in zombies:
        if z['target'] == NULLRECT:
            for c in civies:
                czdistx = abs(z['rect'].x - c['rect'].x)
                czdisty = abs(z['rect'].y - c['rect'].y)
                if czdistx <= ZOMSENSE and czdisty <= ZOMSENSE:
                    z['target'] = c['rect']
                    break
        if z['target'] != NULLRECT:
                if z['rect'].x - z['target'].x > 0:
                    z['rect'].move_ip(z['speed'],0)
                if z['rect'].x - z['target'].x < 0:
                    z['rect'].move_ip(-z['speed'],0) #test to see if need -1 *
                if z['rect'].y - z['target'].y > 0:
                    z['rect'].move_ip(0, z['speed'])
                if z['rect'].y - z['target'].y < 0:
                    z['rect'].move_ip(0, -z['speed'])
        else:
                z['target'].x = random.randrange(-400, 400, 100) + z['rect'].x
                z['target'].y = random.randrange(-400, 400, 100) + z['rect'].y
                if z['rect'].x - z['target'].x > 0:
                    z['rect'].move_ip(z['speed'],0)
                if z['rect'].x - z['target'].x < 0:
                    z['rect'].move_ip(-z['speed'],0) #test to see if need -1 *
                if z['rect'].y - z['target'].y > 0:
                    z['rect'].move_ip(0, z['speed'])
                if z['rect'].y - z['target'].y < 0:
                    z['rect'].move_ip(0, -z['speed'])
                
def DrawBigText(text, bigfont, surface, x, y):
    textobj = bigfont.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
    
def DrawSmText(text, smfont, surface, x, y):
    textobj = smfont.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def ZomSpawn():
    newzom = {'rect': pygame.Rect(random.randint(0,1)*WINDOWWIDTH, random.randint(0,1)*WINDOWHEIGHT, ZOMSIZE, ZOMSIZE),
              'speed':random.randint (ZOMSPEEDMIN, ZOMSPEEDMAX),
              'target': NULLRECT
              }
    zombies.append(newzom)

def CivSpawn():
    newciv = {'rect': pygame.Rect((WINDOWWIDTH/2) + random.randint(-100, 100), (WINDOWWIDTH / 2)  + random.randint(-100, 100), CIVSIZE, CIVSIZE),
              'infect': False
              }
    civies.append(newciv)

# Set up pygame and the game surface window
pygame.init()
MainClock = pygame.time.Clock()
WindowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Zom')
# Set up fonts
bigfont = pygame.font.SysFont(None, 48) #Default font, size 48
smfont = pygame.font.SysFont(None, 24) #Default font, size 24

# Display starting screen
DrawBigText('ZOM', bigfont, WindowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
DrawSmText('Press a key to begin the slaughter.', smfont, WindowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
WaitForKey()

# Start of main program code
while True:
    zombies = []
    civies = []
    ZomAddCounter = 0
    CivAddCounter = CIVQTY
    
    #Populate game world with civies
    while CivAddCounter >= 0:
        CivSpawn()
        CivAddCounter -= 1
    
    while True: #main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                Terminate()
                
        # Add new zombies as they should spawn
        ZomAddCounter += 1
        if ZomAddCounter == ZOMSPAWNRATE:
            ZomAddCounter = 0
            ZomSpawn()
        
        #Move Zombies
        ZomMove(civies, zombies)
        
        # Draw game world on the window
        WindowSurface.fill (BACKGROUNDCOLOR)
        
        #Bite Civies, if possible
        for c in civies:
            if ZomBite(c, zombies):
                c['infect'] = True
        #Remove Bitten Civies
        zify = []
        for c in civies:
            if c['infect'] == True:
                zify.append(c)
                zombies.append(c)
        for victim in zify:
            civies.remove(victim)
        
        #Draw Zombies and Civies
        for z in zombies:    
            pygame.draw.rect(WindowSurface, GREEN, z['rect'])
        for c in civies:
            pygame.draw.rect(WindowSurface, YELLOW, c['rect'])
        
        pygame.display.update()
        
        MainClock.tick(FPS)