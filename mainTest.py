from brain import Brain
from creature import Creature
from landscape import Landscape
from main import printOneCreature
def main():
    brain=Brain.load("bestBrain.pk1")
    printOneCreature(brain)
if(__name__=="__main__"):
    main()
