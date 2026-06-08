from brain import Brain
from creature import Creature
from landscape import Landscape
from main import printOneCreature, runGeneration


def main():
    brain = Brain.load("bestBrain.pkl")
    gridSize = 30
    generations = 30
    childrenPerGen = 50
    topScore = 530
    rate = 0.05
    strength = 0.02
    for generation in range(generations):
        newBrain, newScore = runGeneration(
            brain, childrenPerGen, generation, rate, strength
        )
        print(f"Score is currently:{topScore}")
        if newScore > topScore:
            print("A new brain has taken the throne!")
            brain = newBrain
            topScore = newScore
            brain.save("bestBrain2.pkl")
    printOneCreature(brain)


if __name__ == "__main__":
    main()
