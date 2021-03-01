# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 15:03:22 2021

@author: 18moh
"""
from binarytohex import binhex
import environment

class Robot:
    position=[18, 1]            #current position
    right=2
    left=0
    up=17
    down=19
    
    direction='right'
    
    shortRange=7
    longRange=13
    
    sensors=[['long', 'up', 0],
             ['short', 'right', -1],
             ['short', 'right', 0],
             ['short', 'right', 1],
             ['short', 'down', -1],
             ['short', 'down', 1]
             ]      #sensors
    
    sensedEnvironment=[]   #mapped environment
    actionList=[]          #actions taken
    
    def __init__(self):
        for i in range(20):
            l=[]
            for j in range(15):
                l.append(['?'])
            self.sensedEnvironment.append(l)
            
        for i in range(16,20):
            for j in range(0,4):
                self.sensedEnvironment[i][j].remove('?')
                if(j<3 and i>16):
                    self.sensedEnvironment[i][j].append('S')
                else:
                    self.sensedEnvironment[i][j].append(' ')
                
        for i in range(0,3):
            for j in range(12,15):
                self.sensedEnvironment[i][j].append('G')
                self.sensedEnvironment[i][j].remove('?')
                
                
    def moveForward(self):
        self.actionList.append('move forward')
    
        if(self.direction=='right'):
            self.position[1]+=1
            self.right+=1
            self.left+=1
            
        elif(self.direction=='down'):
            self.position[0]+=1
            self.up+=1
            self.down+=1
            
        elif(self.direction=='left'):
            self.position[1]-=1
            self.right-=1
            self.left-=1
            
        elif(self.direction=='up'):
            self.position[0]-=1
            self.up-=1
            self.down-=1
    
    def turnRight(self):
        self.actionList.append('turn right')
    
        if(self.direction=='right'):
            self.direction='down'
            
        elif(self.direction=='down'):
            self.direction='left'
            
        elif(self.direction=='left'):
            self.direction='up'
            
        elif(self.direction=='up'):
            self.direction='right'
            
        for i in range(len(self.sensors)):
            if(self.sensors[i][1]=='right'):
                self.sensors[i][1]='down'
                
            elif(self.sensors[i][1]=='down'):
                self.sensors[i][1]='left'
                
            elif(self.sensors[i][1]=='left'):
                self.sensors[i][1]='up'
                
            elif(self.sensors[i][1]=='up'):
                self.sensors[i][1]='right'
        
    def turnLeft(self):
        self.actionList.append('turn left')
    
        if(self.direction=='right'):
            self.direction='up'
            
        elif(self.direction=='down'):
            self.direction='right'
            
        elif(self.direction=='left'):
            self.direction='down'
            
        elif(self.direction=='up'):
            self.direction='left'
            
        for i in range(len(self.sensors)):
            if(self.sensors[i][1]=='right'):
                self.sensors[i][1]='up'
                
            elif(self.sensors[i][1]=='down'):
                self.sensors[i][1]='right'
                
            elif(self.sensors[i][1]=='left'):
                self.sensors[i][1]='down'
                
            elif(self.sensors[i][1]=='up'):
                self.sensors[i][1]='left'
                
    def sense(self, environment):
        readings=[]
        
        for x in self.sensors:
            start=[]
            
            if('right' in x):
                pass
            
            elif('left' in x):
                pass
        
            elif('up' in x):
                pass
                
            elif('down' in x):
                pass
        
    
    def processSense(self, readings):
        pass
    
    
    
    
    
    
    
    
    








