import random
import sys
import pygame
from pygame.locals import *

FPS=32
SCREENWIDTH = 289
SCREENHEIGHT =511
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY= SCREENHEIGHT*0.8
GAME_SPRITES={}
GAME_SOUND={}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND=  'gallery/sprites/background1.png'
PIPES ='gallery/sprites/pipe.png'


def welcomescreen():
    playerx= int(SCREENWIDTH/5)
    playery = int ((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int ((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey =  int(SCREENHEIGHT*0.13)
    message3x = int((SCREENWIDTH- GAME_SPRITES['message3'].get_width())/2)
    message3y = int((SCREENHEIGHT*0.32))
    message4x = int((SCREENWIDTH- GAME_SPRITES['message3'].get_width())/2)
    message4y = int((SCREENHEIGHT*0.54))
    basex=0
    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],( 0,0 ))
                SCREEN.blit(GAME_SPRITES['player'],(playerx, playery ))
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey ))
                SCREEN.blit(GAME_SPRITES['message3'],(message3x,message3y ))
                SCREEN.blit(GAME_SPRITES['message4'],(message4x,message4y ))
                SCREEN.blit(GAME_SPRITES['base'], (basex ,GROUNDY ))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def getrandompipe():
    pipeheight = GAME_SPRITES['pipe'][0].get_height()
    offset= SCREENHEIGHT/3
    y2= offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()-1.2*offset))
    pipex=SCREENWIDTH +10
    y1= pipeheight -y2 + offset
    pipe = [{'x': pipex, 'y':-y1},{'x': pipex, 'y':y2}]
    return pipe

def iscollide(playerx , playery , upperpipe ,lowerpipe):
    if playery>GROUNDY-25 or playery<0:
        GAME_SOUND['hit'].play()
        return True
    for pipe in upperpipe:
        pipeheight = GAME_SPRITES['pipe'][0].get_height()
        if(playery<pipeheight+ pipe['y'] and abs(playerx- pipe['x'])< GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUND['hit'].play()
            return True

    for pipe in lowerpipe:
        
        if(playery+ GAME_SPRITES['player'].get_height() > pipe['y'] and abs(playerx- pipe['x'])< GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUND['hit'].play()
            return True
    return False
def maingame():
    score=0
    playerx=int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex=0

    newpipe1 =getrandompipe()
    newpipe2 =getrandompipe()

    upperpipe = [{'x': SCREENWIDTH+200 , 'y': newpipe1[0]['y']},
                {'x': SCREENWIDTH+200 +(SCREENWIDTH/2) , 'y': newpipe2[0]['y']}]

    lowerpipe = [{'x': SCREENWIDTH+200 , 'y': newpipe1[1]['y']},
                {'x': SCREENWIDTH+200 +(SCREENWIDTH/2) , 'y': newpipe2[1]['y']}]


    pipevelx= -4
    playervely = -9
    playermaxvely =10
    playerminvely = -8
    playeraccy =1

    playerflapaccv = -8
    playerflapped = False
    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                if playery>0:
                    playervely = playerflapaccv
                    playerflapped = True
                    GAME_SOUND['wing'].play()
        crashtest= iscollide(playerx , playery , upperpipe ,lowerpipe)
        
        if crashtest:
            return

    
        playermidpos= playerx + GAME_SPRITES['player'].get_width()/2

        for pipe in upperpipe:
            pipemidpos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipemidpos<=playermidpos<pipemidpos+4:
                score+=1
                print(f"you score is {score}")
                GAME_SOUND['point'].play()
        if playervely<playermaxvely and not playerflapped:
            playervely+=playeraccy
        
        if playerflapped:
            playerflapped=False
        playerheight= GAME_SPRITES['player'].get_height()
        playery = playery + min(playervely , GROUNDY - playery -playerheight)

        for upperpipes , lowerpipes in  zip(upperpipe,lowerpipe):
            upperpipes['x']+=pipevelx
            lowerpipes['x']+=pipevelx

        if 0<upperpipe[0]['x']<5:
            newpipe = getrandompipe()
            upperpipe.append(newpipe[0])
            lowerpipe.append(newpipe[1])

        if upperpipe[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperpipe.pop(0)
            lowerpipe.pop(0)
        
        SCREEN.blit(GAME_SPRITES['background'], (0,0) )
        for upperpipes , lowerpipes in  zip(upperpipe,lowerpipe):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperpipes['x'],upperpipes['y']) )
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerpipes['x'],lowerpipes['y']) )

            
        SCREEN.blit(GAME_SPRITES['base'], (basex,GROUNDY) )
        SCREEN.blit(GAME_SPRITES['player'], (playerx,playery) )
        mydigits = [int(x) for x in list(str(score))]
        width=0
        for digit in mydigits:
            width+= GAME_SPRITES['numbers'][digit].get_width()
        xoffset= (SCREENWIDTH- width)/2

        for digit in mydigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (xoffset,SCREENHEIGHT*0.12))
            xoffset+= GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)



if __name__== "__main__":
    pygame.init()
    FPSCLOCK= pygame.time.Clock()
    pygame.display.set_caption("FlappyBird")
    GAME_SPRITES['numbers']=( pygame.image.load('gallery/sprites/0.png').convert_alpha(),
    pygame.image.load('gallery/sprites/1.png').convert_alpha(),pygame.image.load('gallery/sprites/2.png').convert_alpha(),pygame.image.load('gallery/sprites/3.png').convert_alpha(),pygame.image.load('gallery/sprites/4.png').convert_alpha(),pygame.image.load('gallery/sprites/5.png').convert_alpha(),pygame.image.load('gallery/sprites/6.png').convert_alpha(),pygame.image.load('gallery/sprites/7.png').convert_alpha(),pygame.image.load('gallery/sprites/8.png').convert_alpha(),pygame.image.load('gallery/sprites/9.png').convert_alpha()
    )

GAME_SPRITES['message'] = pygame.image.load('gallery/sprites/message1.png').convert_alpha()
GAME_SPRITES['message3'] = pygame.image.load('gallery/sprites/message3.png').convert_alpha()
GAME_SPRITES['message4'] = pygame.image.load('gallery/sprites/message4.png').convert_alpha()
GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base1.png').convert_alpha()
GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPES).convert_alpha(), 180), 
    pygame.image.load(PIPES).convert_alpha()
    )
GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert_alpha()


GAME_SOUND['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
GAME_SOUND['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
GAME_SOUND['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
GAME_SOUND['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
GAME_SOUND['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')


while True:
    welcomescreen()
    maingame()


