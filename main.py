from creature import Creature
from landscape import Landscape
from brain import Brain
import time
import os

def createGameSetup(gridSize,obsN,foodPercent,enemyPercent,holePercent):
    landscape=Landscape(gridSize)
    landscape.populateLandscape(obsN,foodPercent,enemyPercent,holePercent)
    creature=Creature()
    creature.enterLandscape(landscape)
    return(creature, landscape)
    
def runOneCreature(brain):
    startAttempts=50
    attempts=startAttempts
    gridSize=30
    foodPercent=0.05
    enemyPercent=0.025
    holePercent=0.02
    maxEnergy=500
    maxTurns=60
    obsN=0
    score=0
    while(attempts>0):
        turns=0
        creature,landscape=createGameSetup(gridSize,obsN,foodPercent,enemyPercent,holePercent)
        while(creature.isAlive and turns<maxTurns):
            action=brain.think(landscape.grid,creature,creature.energy,maxEnergy)
            if(action==0):
                creature.moveUp()
            elif(action==1):
                creature.moveDown()
            elif(action==2):
                creature.moveLeft()
            elif(action==3):
                creature.moveRight()
            elif(action==4):
                creature.wait()
            creature.moveEnemies()
           #creature.landscape.printLandscape()
            turns+=1
            score+=creature.energy
           #print(f"On this attempt the score was{score}")
        attempts-=1
   #print(f"attmepts left:{attempts}")
   #print(f"His average score was {score/startAttempts}")
    return score/startAttempts

def runGeneration(parentBrain,childrenCount,genNum):
    bestBrain=parentBrain
    bestScore=runOneCreature(parentBrain)
    for i in range(childrenCount):
        childBrain=parentBrain.mutate(0.05,0.01)
        childScore=runOneCreature(childBrain)
        if childScore>bestScore:
            bestScore=childScore
            bestBrain=childBrain
    print(f"The best Score in generation {genNum} was:{bestScore}")
    return bestBrain,bestScore
def printOneCreature(brain):
    gridSize=30
    foodPercent=0.05
    enemyPercent=0.025
    holePercent=0.02
    maxEnergy=500
    maxTurns=60
    obsN=0
    creature,landscape=createGameSetup(gridSize,obsN,foodPercent,enemyPercent,holePercent)
    score=0
    turns=0
    while(creature.isAlive and turns<maxTurns):
        action=brain.think(landscape.grid,creature,creature.energy,maxEnergy)
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
    generations=10
    childrenPerGen=50
    topScore=0
    for generation in range(generations):
        newBrain,newScore=runGeneration(brain,childrenPerGen,generation)
        if(newScore>topScore):
            print("A new brain has taken the throne!")
            brain=newBrain
            topScore=newScore
    brain.save("bestBrain.pk1")

if __name__=="__main__":
    main()
