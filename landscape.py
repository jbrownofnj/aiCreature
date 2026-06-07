import random


class Landscape:

    def __init__(self, dim):
        self.grid = [[0 for x in range(dim)] for y in range(dim)]

    def addDirt(self):
        gSize = len(self.grid)
        for y in range(gSize):
            for x in range(gSize):
                if x != 0 and y != 0 and x != gSize - 1 and y != gSize - 1:
                    self.grid[y][x] = 1

    def isDirt(self, x, y):
        if self.grid[y][x] == 1:
            return True
        else:
            return False

    def isEnterable(self, x, y):
        if self.grid[y][x] == 1 or self.grid[y][x] == 2 or self.grid[y][x] == 4:
            return True
        return False

    def printLandscape(self):
        Colors = {
            0: "\033[37m",
            1: "\033[33m",
            2: "\033[34m",
            3: "\033[31m",
            4: "\033[35m",
            5: "\033[32m",
            6: "\033[0m",
        }
        gSize = len(self.grid)
        gSize = len(self.grid)
        for y in range(gSize):
            for x in range(gSize):
                val = self.grid[y][x]
                print(f"{Colors[val]}{val}{Colors[6]}", end="")
            print()

    def addFood(self, percent):
        gSize = len(self.grid)
        for y in range(gSize):
            for x in range(gSize):
                if self.isDirt(x, y):
                    isFood = percent > random.random()
                    if isFood:
                        self.grid[y][x] = 2

    def addEnemies(self, percent):
        gSize = len(self.grid)
        for y in range(gSize):
            for x in range(gSize):
                if self.isDirt(x, y):
                    isEnemy = percent > random.random()
                    if isEnemy:
                        self.grid[y][x] = 3

    # This is temp a 1 until i want to add in hole logic
    def addHoles(self, percent):
        gSize = len(self.grid)
        for y in range(gSize):
            for x in range(gSize):
                if self.isDirt(x, y):
                    isHole = percent > random.random()
                    if isHole:
                        self.grid[y][x] = 1

    def addObsticles(self, num):
        gSize = len(self.grid)
        for i in range(num):
            length = random.randint(4, 6)
            isVert = random.randint(0, 1) == 1
            if isVert:
                xPos = random.randint(1, gSize - 2)
                yPos = random.randint(1, gSize - (2 + length))
                for j in range(length):
                    self.grid[yPos + j][xPos] = 0
            if isVert == False:
                xPos = random.randint(1, gSize - (2 + length))
                yPos = random.randint(1, gSize - 2)
                for j in range(length):
                    self.grid[yPos][xPos + j] = 0

    def populateLandscape(self, obsN, foodP, enemyP, holesP):
        self.addDirt()
        self.addObsticles(obsN)
        self.addFood(foodP)
        self.addEnemies(enemyP)
        self.addHoles(holesP)


def main():
    print("tets")
    newLand = Landscape(20)
    newLand.populateLandscape()
    newLand.printLandscape()


if __name__ == "__main__":
    main()
