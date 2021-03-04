# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 15:03:22 2021

@author: 18moh
"""
from binarytohex import binhex
from environment import Environment

class Robot:
    position=[18, 1]            #current position
    right=2
    left=0
    up=17
    down=19
    
    direction='right'
    
    shortRange=3
    longRange=8
    
    sensors=[
             ['short', 'right', 1],
             ['short', 'right', -1],
             ['short', 'right', -1],
             ['short', 'down', 0],
             ['short', 'down', -1],
             ['long', 'up', 0]
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
                if('?' in self.sensedEnvironment[i][j]):
                    self.sensedEnvironment[i][j].remove('?')
                if(j<3 and i>16):
                    self.sensedEnvironment[i][j].append('S')
                else:
                    self.sensedEnvironment[i][j].append(' ')
                
        for i in range(0,3):
            for j in range(12,15):
                self.sensedEnvironment[i][j].append('G')
                if('?' in self.sensedEnvironment[i][j]):
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
                self.sensors[i][2]*=-1
                
            elif(self.sensors[i][1]=='down'):
                self.sensors[i][1]='left'
                
            elif(self.sensors[i][1]=='left'):
                self.sensors[i][1]='up'
                self.sensors[i][2]*=-1
                
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
                self.sensors[i][2]*=-1
                
            elif(self.sensors[i][1]=='left'):
                self.sensors[i][1]='down'
                
            elif(self.sensors[i][1]=='up'):
                self.sensors[i][1]='left'
                self.sensors[i][2]*=-1
                
    def sense(self, environment):
        readings=[]
        
        for x in self.sensors:
            senseRange=0
            obstacleDetect=False
            
            if('right' in x):
                if('long' in x):
                    senseRange=self.longRange
                else:
                    senseRange=self.shortRange
                
                for i in range(0, senseRange):
                    if(self.right+i>=14 or 'X' in environment.env[self.up+1+x[2]][self.right+i]):
                        readings.append(i)
                        obstacleDetect=True
                        break
                if(obstacleDetect==False):
                    readings.append(-1)
            
            elif('left' in x):
                if('long' in x):
                    senseRange=self.longRange
                else:
                    senseRange=self.shortRange
                
                for i in range(0, senseRange):
                    if(self.left-i<=0 or 'X' in environment.env[self.up+1+x[2]][self.left-i]):
                        readings.append(i)
                        obstacleDetect=True
                        break
                if(obstacleDetect==False):
                    readings.append(-1)
        
            elif('up' in x):
                if('long' in x):
                    senseRange=self.longRange
                else:
                    senseRange=self.shortRange
                
                for i in range(0, senseRange):
                    if(self.up-i<=0 or 'X' in environment.env[self.up-i][self.left+1+x[2]]):
                        readings.append(i)
                        obstacleDetect=True
                        break
                if(obstacleDetect==False):
                    readings.append(-1)
                
            elif('down' in x):
                if('long' in x):
                    senseRange=self.longRange
                else:
                    senseRange=self.shortRange
                
                for i in range(0, senseRange):
                    if(self.down+i<=19 or 'X' in environment.env[self.down+i][self.left+1+x[2]]):
                        readings.append(i)
                        obstacleDetect=True
                        break
                if(obstacleDetect==False):
                    readings.append(-1)
            
        outstring=""
        for x in readings:
            outstring+=str(x)+"|"
            
        return outstring
        
    
    def processSense(self, readings):
        for i in range(self.left, self.right+1):
            for j in range(self.up, self.down+1):
                if(self.sensedEnvironment[j][i]=='?'):
                    self.sensedEnvironment[j][i]==' '
        
        sense=readings.split('|')
        for i in range(len(sense)):
            sense[i]=float(sense[i])
            
        for i in range(sense):
            value=sense[i]
            x=self.sensors[i]
            senseRange=0
            
            if('right' in x):
                if('long' in x):
                    senseRange=self.longRange
                else:
                    senseRange=self.shortRange
                    
                if(value==-1):
                    for j in range(0, senseRange):
                        if(self.sensedEnvironment[self.up+1+x[2]][self.right+j][0]=='?'):
                            self.sensedEnvironment[self.up+1+x[2]][self.right+j][0]=' '
                    
                for j in range(0, value):
                    if(self.right+j<=14):
                        if(self.sensedEnvironment[self.up+1+x[2]][self.right+j][0]=='?'):
                            self.sensedEnvironment[self.up+1+x[2]][self.right+j][0]=' '
                
                if(self.right+value<=14):          
                    if(self.sensedEnvironment[self.up+1+x[2]][self.right+value][0]=='?'):
                            self.sensedEnvironment[self.up+1+x[2]][self.right+value][0]='X'
                    
            elif('left' in x):
                if('long' in x):
                    senseRange=self.longRange
                else:
                    senseRange=self.shortRange
                    
                if(value==-1):
                    for j in range(0, senseRange):
                        if(self.sensedEnvironment[self.up+1+x[2]][self.left-j][0]=='?'):
                            self.sensedEnvironment[self.up+1+x[2]][self.left-j][0]=' '
                    
                for j in range(0, value):
                    if(self.left-j>=0):
                        if(self.sensedEnvironment[self.up+1+x[2]][self.left-j][0]=='?'):
                            self.sensedEnvironment[self.up+1+x[2]][self.left-j][0]=' '
                            
                if(self.left-value>=0):          
                    if(self.sensedEnvironment[self.up+1+x[2]][self.left-value][0]=='?'):
                            self.sensedEnvironment[self.up+1+x[2]][self.left-value][0]='X'
        
            elif('up' in x):
                if('long' in x):
                    senseRange=self.longRange
                else:
                    senseRange=self.shortRange
                    
                if(value==-1):
                    for j in range(0, senseRange):
                        if(self.sensedEnvironment[self.up-j][self.left+1+x[2]][0]=='?'):
                            self.sensedEnvironment[self.up-j][self.left+1+x[2]][0]=' '
                    
                for j in range(0, value):
                    if(self.up-j>=0):
                        if(self.sensedEnvironment[self.up-j][self.left+1+x[2]][0]=='?'):
                            self.sensedEnvironment[self.up-j][self.left+1+x[2]][0]=' '
                            
                if(self.up-value>=0):        
                    if(self.sensedEnvironment[self.up-j][self.left+1+x[2]][0]=='?'):
                            self.sensedEnvironment[self.up-j][self.left+1+x[2]][0]='X'
                
            elif('down' in x):
                if('long' in x):
                    senseRange=self.longRange
                else:
                    senseRange=self.shortRange
                    
                if(value==-1):
                    for j in range(0, senseRange):
                        if(self.sensedEnvironment[self.down+j][self.left+1+x[2]][0]=='?'):
                            self.sensedEnvironment[self.down+j][self.left+1+x[2]][0]=' '
                    
                for j in range(0, value):
                    if(self.down+j<=14):
                        if(self.sensedEnvironment[self.down+j][self.left+1+x[2]][0]=='?'):
                            self.sensedEnvironment[self.down+j][self.left+1+x[2]][0]=' '
                
                if(self.down+value<=14):          
                    if(self.sensedEnvironment[self.down+j][self.right+value][0]=='?'):
                            self.sensedEnvironment[self.down+j][self.right+value][0]='X'
            
    def getBotMDF(self):
        p1=''
        p2=''
        
        p1+='11'
        
        for i in range(0, 20):
            for j in range(0, 15):
                if('?' in self.sensedEnvironment[19-i][j]):
                    p1+='0'
                else:
                    p1+='1'
                    if('X' in self.sensedEnvironment[19-i][j]):
                        p2+='1'
                    else:
                        p2+='0'
                        
        p1+='11'
        
        hexp1=''
        hexp2=''
        
        i=0
        while(i<len(p1)):
            h1=p1[i:i+4]
            hexp1+=binhex[h1]
            i+=4
            
        while(len(p2)%4!=0):
            p2+='0'
        
        i=0
        while(i<len(p2)):
            h2=p2[i:i+4]
            hexp2+=binhex[h2]
            i+=4
            
        return hexp1, hexp2
    
    
def displayEnvironmentWithBot(environment, bot):    
    for i in range(bot.left, bot.right+1):
        for j in range(bot.up, bot.down+1):
            environment.env[j][i].append('R')
    
    for x in environment.env:
        print(x)
        
    for i in range(len(environment.env)):
        for j in range(len(environment.env[i])):
            if('R' in environment.env[i][j]):
                environment.env[i][j].remove('R')
    
    
    
    
    
    








