difficulty = int(input("""What difficulty would you like? (options are 1-5)
"""))+1
transp = (90, 60, 45, 30, 0)[difficulty-2]
import pygame, random, sys, math
from random import randint
from pygame.locals import *
pygame.init()

screen = pygame.display.set_mode((700, 700))

def backg(pic):
    return genb(pic, (700, 700))
def genb(pic, size):
    return pygame.transform.scale(pygame.image.load(pic), size).convert_alpha()
good = (backg("topside/over1.png"), backg("topside/over2.jpg"), backg("topside/over3.jpg"), backg("topside/over3.jpg"), backg("topside/over4.jpg"), backg("topside/over5.jpg"))
evil = (backg("evil/under1.png"), backg("evil/under2.jpg"), backg("evil/under3.jpg"), backg("evil/under3.jpg"), backg("evil/under4.jpg"), backg("evil/under5.jpg"), backg("evil/under6.jpg"))
speed = 9
clock = pygame.time.Clock()
blockers = (genb("goodblocker.png", (35, 35)), genb("bigblocker.png", (80, 80)), genb("smallblock.png", (35, 35)), genb("blocker.png", (80, 80)))
lvl = 1
walls = []
backstats = [0]
score = 5+2*difficulty

class guy:
    def __init__(self):
        self.x = 600
        self.y = 600
        
    def move(self):
        key = pygame.key.get_pressed()
        if key[K_a] or key[K_LEFT]:
            self.x -= speed
            if self.x < 0:
                self.x = 0
        if key[K_w] or key[K_UP]:
            self.y -= speed
            if self.y < 0:
                self.y = 0
        if key[K_d] or key[K_RIGHT]:
            self.x += speed
            if self.x > 700:
                self.x = 700
        if key[K_s] or key[K_DOWN]:
            self.y += speed
            if self.y > 700:
                self.y = 700
            
    def drawself(self):
        pygame.draw.circle(screen, (0, 0, 255), (self.x-4, self.y-4), 8)
        if pygame.Rect(self.x-16, self.y-16, 32, 32).collidepoint(70, 70):
            self.x = 600
            self.y = 600
            temp = True
        else:
            temp = False
        death = False
        for i in walls:
            if i.size == 0:
                if pygame.Rect(i.x[int(backstats[1]/2)]-4, i.y[int(backstats[1]/2)]-4, 43, 43).collidepoint(self.x, self.y):
                    self.x = 600
                    self.y = 600
                    death = True
            if i.size == 1:
                if pygame.Rect(i.x[int(backstats[1]/2)]-4, i.y[int(backstats[1]/2)]-4, 88, 88).collidepoint(self.x, self.y):
                    self.x = 600
                    self.y = 600
                    death = True
        if temp:
            return 1
        elif death:
            return 2
        else:
            return 0
            
class block:
    def __init__(self, size):
        self.size = size
        self.x = (randint(0, 665), randint(0, 665))
        self.y = (randint(0, 665), randint(0, 665))

    def drawself(self, realms):
        realms[0].blit(blockers[self.size], (self.x[0], self.y[0]))
        realms[1].blit(blockers[self.size+2], (self.x[1], self.y[1]))

        
def levup(lvl):
    PC = guy()
    walls = []
    
    for i in range(difficulty*lvl+2*difficulty):
        temp = block(0)
        while pygame.Rect(temp.x[0]-6, temp.y[0]-6, 47, 47).collidepoint(600, 600) or pygame.Rect(temp.x[1]-6, temp.y[1]-6, 47, 47).collidepoint(600, 600):
            temp = block(0)
        walls.append(temp)
    for i in range(int(0.6*difficulty*lvl+difficulty)):
        temp = block(1)
        while pygame.Rect(temp.x[0]-6, temp.y[0]-6, 92, 92).collidepoint(600, 600) or pygame.Rect(temp.x[1]-6, temp.y[1]-6, 92, 92).collidepoint(600, 600):
            temp = block(1)
        walls.append(temp)
        
        realms = [pygame.Surface((700, 700), pygame.SRCALPHA), pygame.Surface((700, 700), pygame.SRCALPHA)]
    for i in walls:
        i.drawself(realms)
    temp = [pygame.Surface((700, 700)), pygame.Surface((700, 700))]
    temp[0].blit(realms[1], (0, 0))
    temp[1].blit(realms[0], (0, 0))
    temp[0].set_alpha(transp)
    temp[1].set_alpha(transp)
    realms[0].blit(temp[0], (0, 0))
    realms[1].blit(temp[1], (0, 0))
    
    return (walls, realms)

        
PC = guy()

temp = levup(lvl)
backstats = [0, 0, randint(0, 4), randint(0, 5)]
walls = temp[0]
realms = temp[1]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("You ended your run with a final score of "+str(score))
            sys.exit()
    if score < 0:
        print("Your soul itself has vanished from the world on level "+str(lvl))
        sys.exit()
            
    clock.tick(40)
                    
    if backstats[1] == 0:
        screen.blit(good[backstats[2]], (0, 0))
    else:
        screen.blit(evil[backstats[3]], (0, 0))
    backstats[0] += 1
    if backstats[0] >= 50:
        backstats[0] = 0
        score -= 1
        if backstats[1] == 0:
            backstats[1] = 2
        else:
            backstats[1] = 0
            
    pygame.draw.circle(screen, (0, 255, 0), (62, 62), 16)
    
    screen.blit(realms[int(backstats[1]/2)], (0, 0))
    PC.move()
    temp = PC.drawself()
    if temp == 1:
        lvl += 1
        temp = levup(lvl)
        backstats = [0, 0, randint(0, 4), randint(0, 5)]
        walls = temp[0]
        realms = temp[1]
        score += int(1.5*(lvl + (lvl/10+.5)*difficulty))
    elif temp == 2:
        score -= 3

    pygame.display.set_caption("""Etheral Void: Eternity
                                                                    
    Your current score is """+str(score))
        
    
    pygame.display.update()