# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 14:48:28 2021

@author: 18moh
"""
from binarytohex import binhex


class Environment:
    env=[]
    
    def __init__(self):
        for i in range(20):
            l=[]
            for j in range(15):
                l.append([])
            self.env.append(l)
        
    def createEnvironmentMDF(self, p1, p2):
        binp1=''
        for x in p1:
            binp1+=binhex[x]
            
        binp2=''
        for x in p2:
            binp2+=binhex[x]
        
        a=[]
        for i in range(20):
            b=[]
            for j in range(15):
                b.append([])
            a.append(b)
            
        p=2
        for i in range(20):
            for j in range(15):
                if(binp1[p]=='0'):
                    a[19-i][j].append('?')
                p+=1
        
        p=0
        for i in range(20):
            for j in range(15):
                if(len(a[19-i][j])==0):
                    if(binp2[p]=='1'):
                        a[19-i][j].append('X')
                    elif(binp2[p]=='0'):
                        a[19-i][j].append(' ')
                    p+=1
                
        #Start and Goal
        for i in range(17,20):
            for j in range(0,3):
                a[i][j][0]='S'    
        for i in range(0,3):
            for j in range(12,15):
                a[i][j][0]='G'
                    
        self.env=a
        
        
    def displayEnvironment(self):
        for x in self.env:
            print(x)
            


        







