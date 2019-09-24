"""
Program : Collision Drawer App
Author : Mark Song & Ivy Lyu
Last Updated : 6/18/2018
Description:
    This app allows you to input a picture file, draw smaller rectangle boxes on the picture that are
    to be used to repersent smaller collision hitboxes, it allows you to test the hitboxes after you are
    finish the drawing, it outputs a .txt file with their X Y H W values aswell a surface screenshot. 

"""
#https://stackoverflow.com/questions/136734/key-presses-in-python?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
#https://www.autohotkey.com/docs/commands/ControlSend.htm
#https://stackoverflow.com/questions/38001898/what-fonts-can-i-use-with-pygame-font-font
#https://automatetheboringstuff.com/chapter18/
#Imports 
import sys
import math
import pygame
import random
import os
pygame.init()
from classes import *#import the classes

#Colors RGB
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
WHEAT  = (255,231,186)
mode = 0
save = 0


#Functions 
def drawAll():
    global mode
    global save
    screen.blit(bg,(0,0))
    menu.draw()#draw the frame of the surface
    text(550,3,"                Preview",30,RED)
    text(5,507,"                  Tool Box",30,RED)
    
    for b in buttonList:
         b.draw(screen,mp)                                                                                                  #Drawing Every button made in buttonList
    if rectangle_draging:                                                                                                   #While mouse drag draw rectangle
        drawRect(start_mouse_x,start_mouse_y,end_mouse_x,end_mouse_y)
    for item in savedRects:                                                     
        pygame.draw.rect(screen, RED, (item[0],item[1],item[2],item[3]),1)                                                         #Draw the saved rectangles (finished ones) 

    if mode == 3:
        for i in range(len(savedRects)):                        #Preview Mode , bilting the coords under preview box
            xyhw = str(savedRects[i])
            text(540,50 + 100*(i),xyhw,30,RED)
            
    if mode == 4:
        with open('out.txt', 'w') as f:                              #Saving mode , saving the data into a .txt file
            for i in range(len(savedRects)):#save every drawed rectangle coordinate into the text file for further using for collision
                xyhw = str(savedRects[i])
                print(xyhw, file=f)#write coordinates into txt file
    
    if mode == 5:
        ball.draw()
        for item in savedRects:                             
            pygame.draw.rect(screen, RED, (item[0],item[1],item[2],item[3]),1)#draw all rectangles
                
        pressed = pygame.key.get_pressed()    #Move the ball by arrow keys
        if pressed[pygame.K_UP]:
                ball.move("UP")
                for r in savedRects:
                    if ball.isCollision(r[0],r[1],r[2],r[3]):                    #Collision Testing 
                        ball.move("DOWN")
        if pressed[pygame.K_DOWN]:
                ball.move("DOWN")
                for r in savedRects:
                    if ball.isCollision(r[0],r[1],r[2],r[3]):                    #Collision Testing 
                        ball.move("UP")
        if pressed[pygame.K_LEFT]:
                ball.move("LEFT")
                for r in savedRects:
                    if ball.isCollision(r[0],r[1],r[2],r[3]):                    #Collision Testing 
                        ball.move("RIGHT")
        if pressed[pygame.K_RIGHT]:
                ball.move("RIGHT")
                for r in savedRects:
                    if ball.isCollision(r[0],r[1],r[2],r[3]):#Collision Testing 
                        ball.move("LEFT")
                        
                        
    pygame.display.flip()                                                                                                 
    clock.tick(FPS)                                                                                                            
    
def drawRect(start_mouse_x1,start_mouse_y1,start_mouse_x2,start_mouse_y2):   #Dragging Rectangle 
    rect_x = start_mouse_x1
    rect_y = start_mouse_y1 
    rect_w = start_mouse_x2 - start_mouse_x1
    rect_h = start_mouse_y2- start_mouse_y1
    pygame.draw.rect(screen, RED, (rect_x,rect_y,rect_w, rect_h),1)

def text(x,y,text,size,color):         #use for bliting text onto the screen
    myfont = pygame.font.SysFont("Arialrounded", size)
    label = myfont.render(text, 1, color)
    screen.blit(label, (x, y)) 

def createButtons(buttonPos,buttonNames): #Creates list of buttons 
    buttonList=[]
    for i in range(len(buttonPos)):
        b = button((buttonPos[i][0],buttonPos[i][1],50,50),buttonNames[i],WHEAT,2)#use the class button from the class file
        buttonList.append(b)
    return buttonList


#Window Settings
FPS = 30
screen = pygame.display.set_mode((1000,1000))#set window
pygame.display.set_caption("Collision App")
clock = pygame.time.Clock()
pygame.mouse.set_visible(True)

#Global Variables
menu = drawMenu("plane.png",screen,BLACK) #use the drawMenu class to create the frame
buttonPos = [[25,600],[100,600],[175,600],[250,600],[325,600],[400,700],[25,700],[100,700]]#buttons position
buttonNames = ["DRAW",'STOP DRAW','PREVIEW','SAVE','TEST','QUIT', 'UNDO','RESET']#buttons name
buttonList = createButtons(buttonPos, buttonNames)
ball = ball(485,485,10,(RED),screen)#use ball class to create the ball object
rectangle = pygame.rect.Rect(0, 0, 25, 25)
rectangle_draging = False
savedRects = []
bg = pygame.image.load("bg.jpg")#blit the background image



#Main Code
inDraw = True
while inDraw:
    
    if mode == 0:        #Start Mode 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inDraw = False
            elif event.type == pygame.MOUSEBUTTONUP:     
                mp = pygame.mouse.get_pos()
                if event.button == 1:                                           #If click button 0 goes into drawing mode 
                        if buttonList[0].isOver(mp):
                            mode=1
                        if buttonList[7].isOver(mp):
                            mode = 7
                           
    elif mode == 1:                                                             #Drawing Mode 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inDraw = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mp = pygame.mouse.get_pos()
                if event.button == 1:
                    if  mp[0] < 500 and mp[1] < 500:                                 #Can't Draw beyond image's border  
                            start_mouse_x, start_mouse_y = event.pos                                        #end x end y = x2,y2            
                            end_mouse_x, end_mouse_y = start_mouse_x, start_mouse_y                 #Used to calculate and draw the rectangle while dragging
                            rectangle_draging = True
    
                        
            elif event.type == pygame.MOUSEBUTTONUP:
                mp = pygame.mouse.get_pos()
                if event.button == 1:
                    if mp[0] < 500 and mp[1] < 500:
                        rectangle_draging = False
                        savedRects.append((start_mouse_x, start_mouse_y, end_mouse_x - start_mouse_x,end_mouse_y- start_mouse_y))
                    if buttonList[1].isOver(mp): #Stop Drawing 
                        mode = 2
                    if buttonList[7].isOver(mp):  #Reset
                        mode = 7
                    if buttonList[6].isOver(mp):  #Undo 
                        if len(savedRects)>0:
                            savedRects.pop()#delete the last coordinates
                    
                                  
        
            elif event.type == pygame.MOUSEMOTION:                          
                mp = pygame.mouse.get_pos()
                if rectangle_draging:
                    end_mouse_x, end_mouse_y = event.pos

    elif mode == 2:                                     #Stop Drawing Mode 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inDraw = False
            elif event.type == pygame.MOUSEBUTTONUP:       
                mp = pygame.mouse.get_pos()
                if event.button == 1:                                           
                        if buttonList[2].isOver(mp):
                            mode = 3
                        if buttonList[7].isOver(mp):
                            mode = 7
                            
    elif mode == 3:                                     #Preview Mode 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inDraw = False
            elif event.type == pygame.MOUSEBUTTONUP:     
                mp = pygame.mouse.get_pos()
                if event.button == 1:                                           
                        if buttonList[3].isOver(mp):
                            mode = 4
                        if buttonList[7].isOver(mp):
                            mode = 7
    elif mode == 4:                                     #Save mode 
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inDraw = False
            elif event.type == pygame.MOUSEBUTTONUP:     
                mp = pygame.mouse.get_pos()
                if event.button == 1:                                           
                        if buttonList[4].isOver(mp):
                            mode = 5
                        if buttonList[7].isOver(mp):
                            mode = 7

    elif mode == 5:                                     #Test Mode 
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inDraw = False
            elif event.type == pygame.MOUSEBUTTONUP:     
                mp = pygame.mouse.get_pos()
                if event.button == 1:                                           
                        if buttonList[5].isOver(mp):
                            mode = 6
                        if buttonList[7].isOver(mp):
                            mode = 7
                             
    elif mode == 6:                                      #Quit Mode
        pygame.image.save(screen,'surface.png')
        inDraw = False
         
    elif mode == 7:          #Reset to mode 0 
        screen.blit(bg,(0,0))
        savedRects = []#set the rectangle list back to empty list
        pygame.display.update()
        file = open('out.txt', 'w') #clear the previous coordinates
        mode = 0#go back into mode 0
            
    mp = pygame.mouse.get_pos()       
    drawAll()
    
pygame.quit()
    

