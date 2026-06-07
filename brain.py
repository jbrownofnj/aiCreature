import pickle

import numpy as np


class Brain:
    def __init__(self, inputSize, hiddenSize=32):
        self.inputSize = inputSize
        self.hiddenSize = hiddenSize
        self.outputSize = 5
        self.w1 = np.random.randn(hiddenSize, inputSize) * 0.1
        self.b1 = np.zeros(hiddenSize)
        self.w2 = np.random.randn(self.outputSize, hiddenSize) * 0.1
        self.b2 = np.zeros(5)

    def makeInputs(self, grid, creature, energy, maxEnergy):
        up = grid[creature.y - 1][creature.x]
        upLeft = grid[creature.y - 1][creature.x - 1]
        upRight = grid[creature.y - 1][creature.x + 1]
        left = grid[creature.y][creature.x - 1]
        right = grid[creature.y][creature.x + 1]
        down = grid[creature.y + 1][creature.x]
        downLeft = grid[creature.y + 1][creature.x - 1]
        downRight = grid[creature.y + 1][creature.x + 1]

        gridInputs = (
            np.array(
                [up, upLeft, upRight, left, right, down, downLeft, downRight],
                dtype=float,
            )
            / 4.0
        )
        energyInput = np.array([energy / maxEnergy])
        inputs = np.concatenate((gridInputs, energyInput))
        return inputs

    def think(self, grid, creature, energy, maxEnergy):
        inputs = self.makeInputs(grid, creature, energy, maxEnergy)
        hidden = np.tanh(self.w1 @ inputs + self.b1)
        outputs = self.w2 @ hidden + self.b2
        action = np.argmax(outputs)
        return int(action)

    def copy(self):
        newBrain = Brain(self.inputSize, self.hiddenSize)
        newBrain.w1 = self.w1.copy()
        newBrain.b1 = self.b1.copy()
        newBrain.w2 = self.w2.copy()
        newBrain.b2 = self.b2.copy()
        return newBrain

    def randomMutation(self, shape, rate, strength):
        mutationMask = np.random.random(shape) < rate
        mutationValues = np.random.normal(0, strength, shape)
        return mutationMask * mutationValues

    def mutate(self, rate=0.05, strength=0.02):
        child = self.copy()
        child.w1 += self.randomMutation(child.w1.shape, rate, strength)
        child.b1 += self.randomMutation(child.b1.shape, rate, strength)
        child.w2 += self.randomMutation(child.w2.shape, rate, strength)
        child.b2 += self.randomMutation(child.b2.shape, rate, strength)
        return child

    def save(self, fileName):
        with open(fileName, "wb") as file:
            pickle.dump(self, file)

    @staticmethod
    def load(fileName):
        with open(fileName, "rb") as file:
            return pickle.load(file)
