from creature import Creature
from landscape import Landscape
from brain import Brain
import time
import os

def createGameSetup(gridSize,foodPercent,enemyPercent,holePercent):
    landscape=Landscape(gridSize)
    landscape.populateLandscape()
    creature=Creature()
    creature.enterLandscape(landscape)
    return(creature, landscape)
    
def runOneCreature(brain):
    gridSize=30
    foodPercent=0.05
    enemyPercent=0.025
    holePercent=0.02
    maxEnergy=500
    maxTurns=20
    creature,landscape=createGameSetup(gridSize,foodPercent,enemyPercent,holePercent)
    score=0
    turns=0
    while(creature.isAlive and turns<maxTurns):
        action=brain.think(landscape.grid,creature.energy,maxEnergy)
        if(action==0):
            creature.moveUp()
        elif(action==1):
            creature.moveDown()
        elif(action==2):
            creature.moveLeft()
        elif(action==3):
            creature.moveRight()
        elif(action==4):
            pass
        creature.moveEnemies()
        turns+=1
        score+=creature.energy
        return score

def runGeneration(parentBrain,childrenCount):
    bestBrain=parentBrain
    bestScore=runOneCreature(parentBrain)
    for i in range(childrenCount):
        childBrain=parentBrain.mutate()
        childScore=runOneCreature(childBrain)
        if childScore>bestScore:
            bestScore=childScore
            bestBrain=childBrain
    return bestBrain,bestScore
def printOneCreature(brain):
    gridSize=30
    foodPercent=0.05
    enemyPercent=0.025
    holePercent=0.02
    maxEnergy=500
    maxTurns=60
    creature,landscape=createGameSetup(gridSize,foodPercent,enemyPercent,holePercent)
    score=0
    turns=0
    while(creature.isAlive and turns<maxTurns):
        action=brain.think(landscape.grid,creature.energy,maxEnergy)
        if(action==0):
            creature.moveUp()
        elif(action==1):
            creature.moveDown()
        elif(action==2):
            creature.moveLeft()
        elif(action==3):
            creature.moveRight()
        elif(action==4):
            pass
        creature.moveEnemies()
        turns+=1
        score+=creature.energy
        os.system("clear")
        landscape.printLandscape()
        time.sleep(1)
    print(f"Final Score is:{score}")
def main():
    gridSize=30
    inputSize=gridSize*gridSize+1
    brain=Brain(inputSize)
    generations=100 
    childrenPerGen=100
    for generation in range(generations):
        brain,score=runGeneration(brain,childrenPerGen)
    brain.save("bestBrain.pk1")

if __name__=="__main__":
    main()
