from brain import Brain
from creature import Creature
from landscape import Landscape
from main import printOneCreature



def main():
    brain = Brain.load("bestBrain.pkl")
    gridSize = 30
    printOneCreature(brain,gridSize)

if __name__=="__main__":
    main()
