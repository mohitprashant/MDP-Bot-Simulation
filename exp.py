# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 10:29:45 2021

@author: 18moh
"""

from environment import Environment
from robot import Robot
from fps import FPS
import time

class EXP:
    env=Environment()
    bot=Robot()
    fps=FPS()
    
    start=[18, 1]
    targetCoverage=100
    timeAvailable=360
    startTime=-1.0
    goalVisited=False
    
    executeEndSequence=False
    endSequence=[]
    endSequenceIndex=1
    
    
    def setEnvironment(self, p1, p2):
        self.env.createEnvironmentMDF(p1, p2)
        
        
    def reset(self):
        self.bot=Robot()
        self.fps=FPS()
        
        
    def getCoverage(self):
        unknowncount=0
        
        for i in range(len(self.bot.sensedEnvironment)):
            for j in range(len(self.bot.sensedEnvironment[i])):
                if('?' in self.bot.sensedEnvironment[i][j]):
                    unknowncount+=1
                    
        return (unknowncount/300)*100
    
    
    def setTargetCoverage(self, coverage):
        self.targetCoverage=coverage
        
        
    def processSensorData(self, readingstring):
        self.bot.processSense(readingstring)
        
        
    def getMDF(self):
        p1, p2 = self.bot.getBotMDF()
        return "FIN|"+p1+"|"+p2
    
    
    def updateAndroid(self):
        p1, p2 = self.bot.getBotMDF()
        p2=p2[:-1]
        orient, pos = self.bot.direction, self.bot.position       
        
        
    def exploreStep(self):
        if(self.startTime==-1.0):
            self.startTime=time.time()
        
        if(time.time()-self.startTime>=self.timeAvailable-60 or self.getCoverage()>=self.targetCoverage):
            self.executeEndSequence=True
            p1, p2 = self.bot.getBotMDF()
            self.fps.setEnvironment(p1, p2)
            
            if(self.goalVisited):
                self.endSequence=self.fps.getShortestPath(self.bot.position, self.bot.direction, [18, 1])
            else:
                pass
            
        
        if(self.bot.position[0]<4 and self.bot.position[1]>11):
            self.goalVisited=True
        
        if(self.executeEndSequence):
            if(self.endSequenceIndex>=len(self.endSequence)):
                return self.getMDF()
            
            if(self.endSequence[self.endSequenceIndex]=='F'):
                self.bot.moveForward()
                self.endSequenceIndex+=1
                return "EXP|SFS"
            
            elif(self.endSequence[self.endSequenceIndex]=='L'):
                self.bot.turnLeft()
                self.endSequenceIndex+=1
                return "EXP|SLS"
            
            elif(self.endSequence[self.endSequenceIndex]=='R'):
                self.bot.turnLeft()
                self.endSequenceIndex+=1
                return "EXP|SRS"                
            
        else:
            if(self.bot.direction=='right'):  #Turn right, else forward, else left, else back
                canGoRight=True
                canGoForward=True
                canGoLeft=True
                
                if(self.bot.down==19):
                    canGoRight=False
                else:
                    for i in range(self.bot.left, self.bot.right+1):
                        if('X' in self.bot.sensedEnvironment[self.bot.down+1][i] or '?' in self.bot.sensedEnvironment[self.bot.down+1][i]):
                            canGoRight=False     
                if(canGoRight):
                    self.bot.turnRight()
                    self.bot.moveForward()
                    return "EXP|SRSFS"
                else:
                    if(self.bot.right==14):
                        canGoForward=False
                    else:
                        for i in range(self.bot.up, self.bot.down+1):
                            if('X' in self.bot.sensedEnvironment[i][self.bot.right+1] or '?' in self.bot.sensedEnvironment[i][self.bot.right+1]):
                                canGoForward=False
                    if(canGoForward):
                        self.bot.moveForward()
                        return "EXP|SFS"
                    else:
                        if(self.bot.up==0):
                            canGoLeft=False
                        else:
                            for i in range(self.bot.left, self.bot.right+1):
                                if('X' in self.bot.sensedEnvironment[self.bot.up-1][i] or '?' in self.bot.sensedEnvironment[self.bot.up-1][i]):
                                    canGoLeft=False
                        if(canGoLeft):
                            self.bot.turnLeft()
                            self.bot.moveForward()
                            return "EXP|SLSFS"
                        else:
                            self.bot.turnLeft()
                            self.bot.turnLeft()
                            self.bot.moveForward()
                            return "EXP|SLSLSFS"          
            elif(self.bot.direction=='left'):
                canGoRight=True
                canGoForward=True
                canGoLeft=True
                
                if(self.bot.up==0):
                    canGoRight=False
                else:
                    for i in range(self.bot.left, self.bot.right+1):
                        if('X' in self.bot.sensedEnvironment[self.bot.up-1][i] or '?' in self.bot.sensedEnvironment[self.bot.up-1][i]):
                            canGoRight=False     
                if(canGoRight):
                    self.bot.turnRight()
                    self.bot.moveForward()
                    return "EXP|SRSFS"
                else:
                    if(self.bot.left==0):
                        canGoForward=False
                    else:
                        for i in range(self.bot.up, self.bot.down+1):
                            if('X' in self.bot.sensedEnvironment[i][self.bot.left-1] or '?' in self.bot.sensedEnvironment[i][self.bot.left-1]):
                                canGoForward=False
                    if(canGoForward):
                        self.bot.moveForward()
                        return "EXP|SFS"
                    else:
                        if(self.bot.down==19):
                            canGoLeft=False
                        else:
                            for i in range(self.bot.left, self.bot.right+1):
                                if('X' in self.bot.sensedEnvironment[self.bot.down+1][i] or '?' in self.bot.sensedEnvironment[self.bot.down+1][i]):
                                    canGoLeft=False
                        if(canGoLeft):
                            self.bot.turnLeft()
                            self.bot.moveForward()
                            return "EXP|SLSFS"
                        else:
                            self.bot.turnLeft()
                            self.bot.turnLeft()
                            self.bot.moveForward()
                            return "EXP|SLSLSFS"
            elif(self.bot.direction=='up'):
                canGoRight=True
                canGoForward=True
                canGoLeft=True
                
                if(self.bot.right==14):
                    canGoRight=False
                else:
                    for i in range(self.bot.up, self.bot.down+1):
                        if('X' in self.bot.sensedEnvironment[i][self.bot.right+1] or '?' in self.bot.sensedEnvironment[i][self.bot.right+1]):
                            canGoRight=False     
                if(canGoRight):
                    self.bot.turnRight()
                    self.bot.moveForward()
                    return "EXP|SRSFS"
                else:
                    if(self.bot.up==0):
                        canGoForward=False
                    else:
                        for i in range(self.bot.left, self.bot.right+1):
                            if('X' in self.bot.sensedEnvironment[self.bot.up-1][i] or '?' in self.bot.sensedEnvironment[self.bot.up-1][i]):
                                canGoForward=False
                    if(canGoForward):
                        self.bot.moveForward()
                        return "EXP|SFS"
                    else:
                        if(self.bot.left==0):
                            canGoLeft=False
                        else:
                            for i in range(self.bot.up, self.bot.down+1):
                                if('X' in self.bot.sensedEnvironment[i][self.bot.left-1] or '?' in self.bot.sensedEnvironment[i][self.bot.left-1]):
                                    canGoLeft=False
                        if(canGoLeft):
                            self.bot.turnLeft()
                            self.bot.moveForward()
                            return "EXP|SLSFS"
                        else:
                            self.bot.turnLeft()
                            self.bot.turnLeft()
                            self.bot.moveForward()
                            return "EXP|SLSLSFS"
            elif(self.bot.direction=='down'):
                canGoRight=True
                canGoForward=True
                canGoLeft=True
                
                if(self.bot.left==0):
                    canGoRight=False
                else:
                    for i in range(self.bot.up, self.bot.down+1):
                        if('X' in self.bot.sensedEnvironment[i][self.bot.left-1] or '?' in self.bot.sensedEnvironment[i][self.bot.left-1]):
                            canGoRight=False     
                if(canGoRight):
                    self.bot.turnRight()
                    self.bot.moveForward()
                    return "EXP|SRSFS"
                else:
                    if(self.bot.down==19):
                        canGoForward=False
                    else:
                        for i in range(self.bot.left, self.bot.right+1):
                            if('X' in self.bot.sensedEnvironment[self.bot.down+1][i] or '?' in self.bot.sensedEnvironment[self.bot.down+1][i]):
                                canGoForward=False
                    if(canGoForward):
                        self.bot.moveForward()
                        return "EXP|SFS"
                    else:
                        if(self.bot.right==14):
                            canGoLeft=False
                        else:
                            for i in range(self.bot.up, self.bot.down+1):
                                if('X' in self.bot.sensedEnvironment[i][self.bot.right+1] or '?' in self.bot.sensedEnvironment[i][self.bot.right+1]):
                                    canGoLeft=False
                        if(canGoLeft):
                            self.bot.turnLeft()
                            self.bot.moveForward()
                            return "EXP|SLSFS"
                        else:
                            self.bot.turnLeft()
                            self.bot.turnLeft()
                            self.bot.moveForward()
                            return "EXP|SLSLSFS"
        