import random
from landscape import Landscape
import time
import os
import math
from collections import deque

class Creature:
    
    def __init__(self):
        self.energy=50
        self.brain=None
        self.x=None
        self.y=None
        self.landscape=None
        self.energy=50
        self.isAlive=True
   
    def die(self):
        self.energy=0
        self.isAlive=False

    def enterLandscape(self, landscape):
        gSize=len(landscape.grid)
        randPick=self.pickSpot(landscape)
        time.sleep(0.2)
       #print(f"We checking {randPick}")
       #print(f"Our value there is {landscape.grid[randPick[1]][randPick[0]]}")
        if(landscape.isDirt(randPick[1],randPick[0])==False):
            self.enterLandscape(landscape)
        else:
            self.x=randPick[1]
            self.y=randPick[0]
            landscape.grid[self.y][self.x]=5
            self.landscape=landscape

    def pickSpot(self, landscape):
        gSize=len(landscape.grid)
        xPick=random.randint(1,gSize-2)
        yPick=random.randint(1,gSize-2)
        coords=[xPick,yPick]
       #print(f"Pick spot is returning: {coords}")
        return coords

    def moveUp(self):
        self.energy=self.energy-1
       # print(f"Starting move up currently at {self.x},{self.y}")
        nextSpotVal=self.landscape.grid[self.y-1][self.x]
       # print(f"The spot above me is: {nextSpotVal}")
        if(nextSpotVal != 0 and nextSpotVal != 3):
           # print("Spots Open")
            if(nextSpotVal==2):
               # print(f"Found energy. Was {self.energy}")
                self.energy=self.energy+10
               # print(f"Now energy is {self.energy}")
            self.y=self.y-1
            self.landscape.grid[self.y][self.x]=5
            self.landscape.grid[self.y+1][self.x]=1
       # print(f"I am now at {self.x},{self.y}")

    def moveDown(self): 
        self.energy=self.energy-1
        nextSpotVal=self.landscape.grid[self.y+1][self.x]
        if(nextSpotVal !=0 and nextSpotVal != 3):
            if(nextSpotVal==2):
                self.energy=self.energy+10
            self.y=self.y+1
            self.landscape.grid[self.y][self.x]=5
            self.landscape.grid[self.y-1][self.x]=1
    
    def moveRight(self): 
        self.energy=self.energy-1
        nextSpotVal=self.landscape.grid[self.y][self.x+1]
        if(nextSpotVal !=0 and nextSpotVal != 3):
            if(nextSpotVal==2):
                self.energy=self.energy+10
            self.x=self.x+1
            self.landscape.grid[self.y][self.x]=5
            self.landscape.grid[self.y][self.x-1]=1
    
    def moveLeft(self): 
        self.energy=self.energy-1
        nextSpotVal=self.landscape.grid[self.y][self.x-1]
        if(nextSpotVal !=0 and nextSpotVal != 3):
            if(nextSpotVal==2):
                self.energy=self.energy+10
            self.x=self.x-1
            self.landscape.grid[self.y][self.x]=5
            self.landscape.grid[self.y][self.x+1]=1

    def wait(self):
       self.energy=self.energy-1

    def printLoc(self):
        print(f"Create is at {self.x},{self.y}")
   
    def withinXDist(self,x,y,maxD):
        dist=(abs(self.x-x)**2+abs(self.y-y)**2)**0.5
        return maxD>dist

    def bfs(self,x,y):
        start_x=x 
        start_y=y
        queue=deque()
        queue.append((x,y))
        visited=set()
        visited.add((x,y))
        parent={}
        directions=[(0,-1),(0,1),(-1,0),(1,0)]
        while queue:
            current_x,current_y=queue.popleft()
            if(current_x,current_y)==(self.x,self.y):
                break
            for dx,dy in directions:
                next_x=current_x+dx
                next_y=current_y+dy
                if next_x<0 or next_y<0:
                    continue
                if next_y >= len(self.landscape.grid):
                    continue
                if next_x >= len(self.landscape.grid[0]):
                    continue
                if self.landscape.grid[next_y][next_x]==0:
                    continue
                if self.landscape.grid[next_y][next_x]==2:
                    continue
                if self.landscape.grid[next_y][next_x]==4:
                    continue
                if (next_x,next_y) in visited:
                    continue
                visited.add((next_x,next_y))
                parent[(next_x,next_y)]=current_x,current_y
                queue.append((next_x,next_y))
        if((self.x,self.y) not in parent):
            return None
        path=[]
        current=(self.x,self.y)
        while current!= (start_x,start_y):
            path.append(current)
            current=parent[current]
        path.reverse()
        return path
    
    def moveEnemy(self,i,j):
        grid=self.landscape.grid
        if(self.withinXDist(i,j,8)):
            path=self.bfs(i,j)
            nextMove=None
            if(path is not None):
                nextMove=path[0]
            if(nextMove is not None):
                if(grid[nextMove[1]][nextMove[0]]==5):
                    self.die()
                grid[nextMove[1]][nextMove[0]]=3
                grid[j][i]=1
        else:
            rand=random.randint(1,4)
            if rand==1 and grid[j-1][i]!=0 and grid[j-1][i]!=3 and grid[j-1][i]!=4:
                grid[j][i]=1
                grid[j-1][i]=3
            if rand==2 and grid[j+1][i]!=0 and grid[j+1][i]!=3 and grid[j+1][i]!=4:
                grid[j][i]=1
                grid[j+1][i]=3
            if rand==3 and grid[j][i-1]!=0 and grid[j][i-1]!=3 and grid[j][i-1]!=4:
                grid[j][i]=1
                grid[j][i-1]=3
            if rand==4 and grid[j][i+1]!=0 and grid[j][i+1]!=3 and grid[j][i+1]!=4:
                grid[j][i]=1
                grid[j][i+1]=3
        
    def moveEnemies(self):
        enemies=[]
        gSize=len(self.landscape.grid)
        for i in range(gSize):
            for j in range(gSize):
                if(self.landscape.grid[j][i]==3):
                    enemies.append((i,j))
        for x,y in enemies:
            if self.landscape.grid[y][x]==3:
                self.moveEnemy(x,y)

def main():
    testLandscape=Landscape(30)
    testLandscape.populateLandscape()
    newCreature=Creature()
    newCreature.enterLandscape(testLandscape)
    os.system("clear")
    testLandscape.printLandscape()
   # time.sleep(1)
   # os.system("clear")
   # newCreature.moveUp()
   # testLandscape.printLandscape()
   # time.sleep(1)
   # os.system("clear")
   # newCreature.moveUp()
   # testLandscape.printLandscape()
   # time.sleep(1)
   # os.system("clear")
   # newCreature.moveLeft()
   # testLandscape.printLandscape()
   # time.sleep(1)
   # os.system("clear")
   # newCreature.moveDown()
   # testLandscape.printLandscape()
   # time.sleep(1)
   # os.system("clear")
   # newCreature.moveRight()
   # testLandscape.printLandscape()
   # time.sleep(1)
   # os.system("clear")
   # newCreature.moveRight()
   # testLandscape.printLandscape()
    time.sleep(2)
    os.system("clear")
    newCreature.moveEnemies()
    testLandscape.printLandscape()
    time.sleep(2)
    os.system("clear")
    newCreature.moveEnemies()
    testLandscape.printLandscape()
    time.sleep(2)
    os.system("clear")
    newCreature.moveEnemies()
    testLandscape.printLandscape()
    time.sleep(2)
    os.system("clear")
    newCreature.moveEnemies()
    testLandscape.printLandscape()
    time.sleep(2)
    os.system("clear")
    newCreature.moveEnemies()
    testLandscape.printLandscape()
    time.sleep(2)
    os.system("clear")
    newCreature.moveEnemies()
    testLandscape.printLandscape()
    time.sleep(2)
    os.system("clear")
    newCreature.moveEnemies()
    testLandscape.printLandscape()

    
    print("Creature test complete")
 
if __name__=="__main__":
    main()
