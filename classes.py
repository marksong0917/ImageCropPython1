"""
Program : Classes for Collision Drawer
Author : Mark Song & Ivy Lyu
Last Updated : 06/18/18
Description:
    This file is used for collision app developed by the author,
this py file contains button class, ball class,  rectangle class and getData class
"""

#Imports
import sys
import math
import pygame
import random
import os
pygame.init()

#Define some colors 
SNOW   = (255,250,250) 	
BLACK  = (0  ,  0,  0)
WHITE  = (255,255,255)
GREEN  = (0  ,255,  0)
RED    = (255,  0,  0)
LBLUE  = (0  ,191,255)
BLUE   = (  0,  0,255)
YELLOW = (255,255,  0)	
GOLD   = (255,215,  0) 	
WOOD   = (222,184,135)
PURPLE = (255,  0,255)
LGREEN = (173,255, 47)
DGREEN = (107,142, 35)


#-------------------------------------------------------------------------------------------------------------------------#
class button:  
    bfont=pygame.font.SysFont('arial',15)
    def __init__(self,rect,text,colour,borderColour=(0,0,0),textColour=(0,0,0),borderThickness=2,mouseOverColour=(255,255,0)):
        self.visible=True
        self.rect=rect
        self.x=rect[0]
        self.y=rect[1]
        self.width=rect[2]
        self.height=rect[3]
        self.text=text
        self.colour=colour
        self.borderColour=borderColour
        self.textColour=textColour
        self.borderThickness=borderThickness
        self.mouseOverColour=mouseOverColour

    def draw(self,screen,mp):
        if self.visible==True:
            pygame.draw.rect(screen,self.colour,self.rect)
            if self.isOver(mp):
                pygame.draw.rect(screen,self.mouseOverColour,self.rect,self.borderThickness)
            else:
                pygame.draw.rect(screen,self.borderColour,self.rect,self.borderThickness)
            bText=self.bfont.render(self.text,True,self.textColour)
            tx=self.x+(self.width-bText.get_width())//2
            ty=self.y+(self.height-bText.get_height())//2
            screen.blit(bText,(tx,ty))

    def isOver(self,mp):
        mx,my=mp[0],mp[1]
        return self.x<= mx<=self.x+self.width and self.y<= my<=self.y+self.height

    def setFont(self,fontName,size):
        self.font=pygame.font.SysFont(fontName,size)
#-------------------------------------------------------------------------------------------------------------------------#
class ball:                #Makes a simple ball           
    def __init__(self,x,y,r,c,screen):
        self.x = x
        self.y = y
        self.r = r
        self.c = c
        self.screen = screen
        self.speed_x = 5
        self.speed_y = 5
        self.h = 10
        self.w = 10

    def draw(self):#draw the ball shape
        pygame.draw.circle(self.screen, self.c, [self.x, self.y], self.r)

    def reset(self): #make the x and y coordinates be 0      
        self.x = 0
        self.y = 0

    def move(self, mt):								#Able to move with Arrow Keys
        if mt == "UP":
            self.y -= 5
        elif mt =="DOWN":
            self.y += 5
        elif mt == "LEFT":
            self.x -=5
        elif mt =="RIGHT":
            self.x +=5

        if self.x - self.r <0:
            self.x = self.r

        elif self.x + self.r > 500:            #Preventing the ball from going off screen / 2 
            self.x = 500 - self.r

        if self.y - self.r < 0:
            self.y = self.r
        elif  self.y + self.r > 500:
            self.y = 500 - self.r

    def distance(self, x1,y1,x2,y2):#calculate the distance between the two given coordinates
        return math.sqrt((y2 - y1)**2 + (x2 - x1)**2 )

    def isCollision(self, rectLeft, rectTop, rectW, rectH):
        testX = self.x
        testY = self.y
        # which edge is closest?
        if (self.x < rectLeft):
            testX = rectLeft      # test left edge
        elif (self.x > rectLeft+rectW):
            testX = rectLeft+rectW;   # right edge
        if (self.y < rectTop):
            testY = rectTop      # top edge
        elif (self.y > rectTop+rectH):
            testY = rectTop+rectH   # bottom edge
        # get distance from closest edges
        distX = self.x-testX
        distY = self.y-testY
        distance = math.sqrt(distX**2 + distY**2)

        # if the distance is less than the radius, collision!
        if (distance <= self.r): 
            return True
        else:
            return False
            
#-------------------------------------------------------------------------------------------------------------------------#
class makeRectangle:                #Creates rectangles using an large dataList 
    def __init__(self,dataList,screen):
        self.screen = screen
        self.dataList = dataList
        
    def draw(self):#draw the rectangle on the screen
        while self.dataList != []:
            temp = self.dataList.pop()
            rect = (temp[0],temp[1],temp[3],temp[2])
            pygame.draw.rect(self.screen,RED,(rect[0],rect[1],rect[2],rect[3]),2)
#-------------------------------------------------------------------------------------------------------------------------#
class readData:                  #Reads data, organize them into a large list that can be used for drawing rectangles    
    def __init__(self,filename):
        self.List = []
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file]
        for line in lines:
            line = line.strip('(')
            line = line.strip(')')
            line = line.split(",")
            item = [ int(i) for i in line ]
            self.List.append(item)
            
    def getData(self):
        return (self.List) #Returns the data list 
#-------------------------------------------------------------------------------------------------------------------------#
class drawMenu:
    def __init__(self,ImgName,win,c):           #Main GUI drawing 
        self.ImgName=ImgName
        self.win=win
        self.c = c

    def draw(self):
        Img = pygame.image.load(self.ImgName)
        self.win.blit(Img,(50,50))
        pygame.draw.rect(self.win,self.c,(500,0,7,1000),0)     #Preview Box
        pygame.draw.rect(self.win,self.c,(505,0,500,50),4)    # Preview Divider
        pygame.draw.rect(self.win,self.c,(0,500,500,7),0)       #Tool Box
        pygame.draw.rect(self.win,self.c,(0,505,500,50),4)   #Divider

#-------------------------------------------------------------------------------------------------------------------------#
