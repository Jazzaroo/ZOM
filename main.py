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
ZOMSENSE = 50
CIVMOVERATE = 2
CIVQTY = 8
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

class Entity:
    location = None
    target = None
    speed = None
    
    def Chase( self ):
        if self.HasTarget():
            if self.location.colliderect( self.target ):
                self.TargetMet()
            else:
                if self.location.x > self.target.x:
                    self.location.move_ip(-self.speed,0)
                elif self.location.x < self.target.x:
                    self.location.move_ip(self.speed,0)
                if self.location.y > self.target.y:
                    self.location.move_ip(0, -self.speed)
                elif self.location.y < self.target.y:
                    self.location.move_ip(0, self.speed)
                
                    
    def Evade( self ):
        if self.HasTarget():
            if self.location.x > self.target.x:
                self.location.move_ip(self.speed,0)
            elif self.location.x < self.target.x:
                self.location.move_ip(-self.speed,0)
            if self.location.y > self.target.y:
                self.location.move_ip(0, self.speed)
            elif self.location.y < self.target.y:
                self.location.move_ip(0, -self.speed)
    
    def HasTarget( self ):
        return self.target != None
    
    def TargetMet( self ):
        self.target = None
    

class Zombie( Entity ):
    
    def __init__(self, C = None):
        if C is pygame.Rect:
            self.location = C
        else:
            self.location = pygame.Rect(random.randint(0,1)*WINDOWWIDTH, random.randint(0,1)*WINDOWHEIGHT, ZOMSIZE, ZOMSIZE)
            
        self.speed = random.randint( 1, 2 )
        print("I AM ZOMBIE .. GWAR!")

class Civilian( Entity ):
    speed = CIVMOVERATE
    infected = False
    
    def __init__(self):
        self.location = pygame.Rect((WINDOWWIDTH/2) + random.randint(-100, 100), (WINDOWWIDTH / 2)  + random.randint(-100, 100), CIVSIZE, CIVSIZE)
        print("I am a weenie human")
        
    def TargetMet(self):
        infected = True

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
        if c.location.colliderect(z.location):
            z.target = None
            return True
    return False

def ZomMove(civies, zombies):
    for z in zombies:
        for c in civies:
            czdistx = abs(z.location.x - c.location.x)
            czdisty = abs(z.location.y - c.location.y)
            if czdistx <= ZOMSENSE and czdisty <= ZOMSENSE:
                print( "Found a human" )
                z.target = c.location
                c.target = z.location
                break
        
        if not z.HasTarget():
            newrect = pygame.Rect( random.randint(0,WINDOWWIDTH),
                                   random.randint(0,WINDOWHEIGHT), ZOMSIZE, ZOMSIZE )
            z.target = newrect
            
        z.Chase()
                                
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
    zombies.append( Zombie() )

def CivSpawn():
    civies.append( Civilian() )

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
                c.infected = True
        #Remove Bitten Civies
        zify = []
        for c in civies:
            if c.infected == True:
                zify.append(c)
                zombies.append(Zombie( c.location ) )
            else:
                c.Evade()
        for victim in zify:
            civies.remove(victim)
        
        #Draw Zombies and Civies
        for z in zombies:    
            pygame.draw.rect(WindowSurface, GREEN, z.location)
        for c in civies:
            pygame.draw.rect(WindowSurface, YELLOW, c.location)
        
        pygame.display.update()
        
        MainClock.tick(FPS)