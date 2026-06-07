import os
import time

from brain import Brain
from creature import Creature
from landscape import Landscape


def createGameSetup(gridSize, obsN, foodPercent, enemyPercent, holePercent):
    landscape = Landscape(gridSize)
    landscape.populateLandscape(obsN, foodPercent, enemyPercent, holePercent)
    creature = Creature()
    creature.enterLandscape(landscape)
    return (creature, landscape)


def runOneCreature(
    brain,
    sAttempts=50,
    gSize=30,
    fPercent=0.05,
    ePercent=0.025,
    hPercent=0.02,
    maxE=500,
    maxT=60,
    obsNum=0,
):
    startAttempts = sAttempts
    attempts = startAttempts
    gridSize = gSize
    foodPercent = fPercent
    enemyPercent = ePercent
    holePercent = hPercent
    maxEnergy = maxE
    maxTurns = maxT
    obsN = obsNum
    score = 0
    while attempts > 0:
        turns = 0
        creature, landscape = createGameSetup(
            gridSize, obsN, foodPercent, enemyPercent, holePercent
        )
        while creature.isAlive and turns < maxTurns:
            action = brain.think(landscape.grid, creature, creature.energy, maxEnergy)
            if action == 0:
                creature.moveUp()
            elif action == 1:
                creature.moveDown()
            elif action == 2:
                creature.moveLeft()
            elif action == 3:
                creature.moveRight()
            elif action == 4:
                creature.wait()
            creature.moveEnemies()
            turns += 1
            score += creature.energy
        attempts -= 1
    return score / startAttempts


def runGeneration(parentBrain, childrenCount, genNum, rate=0.05, strength=0.01):
    bestBrain = parentBrain
    bestScore = runOneCreature(parentBrain)
    for i in range(childrenCount):
        childBrain = parentBrain.mutate(rate, strength)
        childScore = runOneCreature(childBrain)
        if childScore > bestScore:
            bestScore = childScore
            bestBrain = childBrain
    print(f"The best Score in generation {genNum} was:{bestScore}")
    return bestBrain, bestScore

        
def printOneCreature(
    brain,
    gSize=30,
    fPercent=0.05,
    ePercent=0.025,
    hPercent=0.02,
    maxE=500,
    maxT=60,
    obsNum=0,
):
    gridSize = gSize
    foodPercent = fPercent
    enemyPercent = ePercent
    holePercent = hPercent
    maxEnergy = maxE
    maxTurns = maxT
    obsN = obsNum
    score = 0
    turns = 0
    creature, landscape = createGameSetup(
        gridSize, obsN, foodPercent, enemyPercent, holePercent
    )
    while creature.isAlive and turns < maxTurns:
        action = brain.think(landscape.grid, creature, creature.energy, maxEnergy)
        if action == 0:
            creature.moveUp()
        elif action == 1:
            creature.moveDown()
        elif action == 2:
            creature.moveLeft()
        elif action == 3:
            creature.moveRight()
        elif action == 4:
            creature.wait()
        creature.moveEnemies()
        turns += 1
        score += creature.energy
        os.system("clear")
        landscape.printLandscape()
        print(f"Score:{score}")
        time.sleep(0.5)
    print(f"Final Score is:{score}")    

    



def main():
    gridSize = 30
    brain = Brain(9)
    generations = 100
    childrenPerGen = 50
    topScore = 0
    rate = 0.05
    strength = 0.05
    for generation in range(generations):
        newBrain, newScore = runGeneration(
            brain, childrenPerGen, generation, rate, strength
        )
        if newScore > topScore:
            print("A new brain has taken the throne!")
            brain = newBrain
            topScore = newScore
            brain.save("bestBrain.pkl")
    printOneCreature(brain,gridSize)

if __name__ == "__main__":
    main()
