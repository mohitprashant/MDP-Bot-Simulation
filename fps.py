# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 03:46:09 2021

@author: 18moh
"""

from robot import Robot
from environment import Environment

class FPS:
    env=Environment()
    bot=Robot()
    
    start=[18, 1]
    waypoint=[1, 1]
    goal=[1, 13]
    
    def setEnvironment(self, p1, p2):
        self.env.createEnvironmentMDF(p1, p2)
    
    def setWaypoint(self, x, y):
        self.waypoint=[x, y]
        
    def getShortestPath(self, start, direction, goal):
        self.bot.sensedEnvironment=self.env.env        
        pathBuilder=[]
        
        for i in range(20):
            l=[]        
            for j in range(15):
                l.append([])
            pathBuilder.append(l)
        
        for i in range(20):
            pathBuilder[i][0].append('X')
            pathBuilder[i][14].append('X')
        for i in range(15):
            pathBuilder[0][i].append('X')
            pathBuilder[19][i].append('X')
        
        for i in range(20):
            for j in range(15):
                if('X' in self.env.env[i][j] or '?' in self.env.env[i][j]):
                    pathBuilder[i][j].append('X')
                    for a in range(i-1, i+2):
                        for b in range(j-1, j+2):
                            try:
                                if('X' not in pathBuilder[a][b]):
                                    pathBuilder[a][b].append('X')
                            except:
                                pass
                            
        for i in range(20):
            for j in range(15):
                if(len(pathBuilder[i][j])>1):
                    del pathBuilder[i][j][1]
        
        pathBuilder[start[0]][start[1]].append(direction)
    
        queue=[]
        finished=[]
        queue.append(start)
        
        while(len(queue)>0):
            node=queue[0]
            
            currentDirection=pathBuilder[node[0]][node[1]][0]
            adjacent=[]
            
            
            if('X' not in pathBuilder[node[0]][node[1]+1] ):
                adjacent.append([node[0], node[1]+1])
                if([node[0], node[1]+1] not in finished and [node[0], node[1]+1] not in queue):
                    queue.append([node[0], node[1]+1])
                    
            if('X' not in pathBuilder[node[0]][node[1]-1]):
                adjacent.append([node[0], node[1]-1])
                if([node[0], node[1]-1] not in finished and [node[0], node[1]-1] not in queue):
                    queue.append([node[0], node[1]-1])
                    
            if('X' not in pathBuilder[node[0]+1][node[1]]):
                adjacent.append([node[0]+1, node[1]])
                if([node[0]+1, node[1]] not in finished and [node[0]+1, node[1]] not in queue):
                    queue.append([node[0]+1, node[1]])
                    
            if('X' not in pathBuilder[node[0]-1][node[1]]):
                adjacent.append([node[0]-1, node[1]])
                if([node[0]-1, node[1]] not in finished and [node[0]-1, node[1]] not in queue):
                    queue.append([node[0]-1, node[1]])               
            
            for adj in adjacent:
                moveList=[]
                for i in range(len(pathBuilder[node[0]][node[1]])):
                    moveList.append(pathBuilder[node[0]][node[1]][i])
                    
                if(adj[0]==node[0]+1):
                    moveList[0]='down'
                elif(adj[0]==node[0]-1):
                    moveList[0]='up'
                elif(adj[1]==node[1]+1):
                    moveList[0]='right'
                elif(adj[1]==node[1]-1):
                    moveList[0]='left'
                
                if(currentDirection=='right'):
                    if(moveList[0]=='right'):
                        moveList.append('F')
                    elif(moveList[0]=='left'):
                        moveList.append('L')
                        moveList.append('L')
                        moveList.append('F')
                    elif(moveList[0]=='up'):
                        moveList.append('L')
                        moveList.append('F')
                    elif(moveList[0]=='down'):
                        moveList.append('R')
                        moveList.append('F')
                        
                elif(currentDirection=='left'):
                    if(moveList[0]=='right'):
                        moveList.append('L')
                        moveList.append('L')
                        moveList.append('F')
                    elif(moveList[0]=='left'):
                        moveList.append('F')
                    elif(moveList[0]=='up'):
                        moveList.append('R')
                        moveList.append('F')
                    elif(moveList[0]=='down'):
                        moveList.append('L')
                        moveList.append('F')
                        
                elif(currentDirection=='up'):
                    if(moveList[0]=='right'):
                        moveList.append('R')
                        moveList.append('F')
                    elif(moveList[0]=='left'):
                        moveList.append('L')
                        moveList.append('F')
                    elif(moveList[0]=='up'):
                        moveList.append('F')
                    elif(moveList[0]=='down'):
                        moveList.append('L')
                        moveList.append('L')
                        moveList.append('F')
                        
                elif(currentDirection=='down'):
                    if(moveList[0]=='right'):
                        moveList.append('L')
                        moveList.append('F')
                    elif(moveList[0]=='left'):
                        moveList.append('R')
                        moveList.append('F')
                    elif(moveList[0]=='up'):
                        moveList.append('L')
                        moveList.append('L')
                        moveList.append('F')
                    elif(moveList[0]=='down'):
                        moveList.append('F')
                
                if(len(moveList)<len(pathBuilder[adj[0]][adj[1]]) or len(pathBuilder[adj[0]][adj[1]])==0):
                    pathBuilder[adj[0]][adj[1]]=moveList
            
            finished.append(queue[0])
            del queue[0]
                    
        return pathBuilder[goal[0]][goal[1]]
        
    def getShortestPathWithWaypoint(self):
        actionlist1=self.getShortestPath(self.start, self.bot.direction, self.waypoint)
        actionlist2=self.getShortestPath(self.waypoint, actionlist1[0], self.goal)
        
        movesFromLastAlign=0
        alignASAP=False
        
        moveset=actionlist1[1:]+actionlist2[1:]            
        
        outputstring=""
        for x in moveset:
            outputstring+=x
            
            if(x=='L'):
                self.bot.turnLeft()
                #alignASAP=True
            elif(x=='R'):
                self.bot.turnRight()
                #alignASAP=True
            elif(x=='F'):
                self.bot.moveForward()
                movesFromLastAlign+=1
            
            readings=self.bot.sense(self.env).split('|')
            
            if((movesFromLastAlign>=4 or alignASAP) and (readings[0]==readings[2])):
                #outputstring+='A'
                movesFromLastAlign=0
                alignASAP=False
            elif((movesFromLastAlign>=4 or alignASAP) and (readings[3]==readings[4])):
                #outputstring+='A'
                movesFromLastAlign=0
                alignASAP=False
        
        print(outputstring)
        
        betteroutputstring="FPS|"
        fcount=0
        for x in outputstring:
            if(x=='F'):
                fcount+=1
            else:
                if(fcount==0):
                    continue
                else:
                    betteroutputstring+=str(fcount)+","
                    fcount=0
                    betteroutputstring+=x+","
        betteroutputstring+=str(fcount)
        
        return betteroutputstring
    
    
#########
fps=FPS()
p1='FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
p2='00400080010000000000003F000000000000400100040F000000000380000000080010002000'
fps.setEnvironment(p1, p2)
fps.setWaypoint(1, 1)
print(fps.getShortestPathWithWaypoint())
#########
        
        
        