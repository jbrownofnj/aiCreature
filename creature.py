import math
import os
import random
import time
from collections import deque

from landscape import Landscape


class Creature:
    def __init__(self, startEnergy=10):
        self.brain = None
        self.x = None
        self.y = None
        self.landscape = None
        self.energy = startEnergy
        self.isAlive = True

    def die(self):
        self.energy = 0
        self.isAlive = False

    def getValidEntrySpot(self, landscape):
        gSize = len(landscape.grid)
        randPick = self.pickSpot(landscape)
        if landscape.isDirt(randPick[0], randPick[1]) == False:
            return self.getValidEntrySpot(landscape)
        else:
            return (randPick[0], randPick[1])

    def enterLandscape(self, landscape):
        gSize = len(landscape.grid)
        startCoord = self.getValidEntrySpot(landscape)
        self.x = startCoord[0]
        self.y = startCoord[1]
        landscape.grid[self.y][self.x] = 5
        self.landscape = landscape

    def pickSpot(self, landscape):
        gSize = len(landscape.grid)
        xPick = random.randint(1, gSize - 2)
        yPick = random.randint(1, gSize - 2)
        coords = [xPick, yPick]
        return coords

    def moveUp(self):
        self.energy = self.energy - 1
        if self.energy == 0:
            self.die()
        nextSpotVal = self.landscape.grid[self.y - 1][self.x]
        if nextSpotVal != 0 and nextSpotVal != 3:
            if nextSpotVal == 2:
                self.energy = self.energy + 50
            self.y = self.y - 1
            self.landscape.grid[self.y][self.x] = 5
            self.landscape.grid[self.y + 1][self.x] = 1

    def moveDown(self):
        self.energy = self.energy - 1
        if self.energy == 0:
            self.die()
        nextSpotVal = self.landscape.grid[self.y + 1][self.x]
        if nextSpotVal != 0 and nextSpotVal != 3:
            if nextSpotVal == 2:
                self.energy = self.energy + 50
            self.y = self.y + 1
            self.landscape.grid[self.y][self.x] = 5
            self.landscape.grid[self.y - 1][self.x] = 1

    def moveRight(self):
        self.energy = self.energy - 1
        if self.energy == 0:
            self.die()
        nextSpotVal = self.landscape.grid[self.y][self.x + 1]
        if nextSpotVal != 0 and nextSpotVal != 3:
            if nextSpotVal == 2:
                self.energy = self.energy + 50
            self.x = self.x + 1
            self.landscape.grid[self.y][self.x] = 5
            self.landscape.grid[self.y][self.x - 1] = 1

    def moveLeft(self):
        self.energy = self.energy - 1
        if self.energy == 0:
            self.die()
        nextSpotVal = self.landscape.grid[self.y][self.x - 1]
        if nextSpotVal != 0 and nextSpotVal != 3:
            if nextSpotVal == 2:
                self.energy = self.energy + 50
            self.x = self.x - 1
            self.landscape.grid[self.y][self.x] = 5
            self.landscape.grid[self.y][self.x + 1] = 1

    def wait(self):
        self.energy = self.energy - 1

    def withinXDist(self, x, y, maxD):
        dist = (abs(self.x - x) ** 2 + abs(self.y - y) ** 2) ** 0.5
        return maxD > dist

    def bfs(self, x, y):
        start_x = x
        start_y = y
        queue = deque()
        queue.append((x, y))
        visited = set()
        visited.add((x, y))
        parent = {}
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        while queue:
            current_x, current_y = queue.popleft()
            if (current_x, current_y) == (self.x, self.y):
                break
            for dx, dy in directions:
                next_x = current_x + dx
                next_y = current_y + dy
                if next_x < 0 or next_y < 0:
                    continue
                if next_y >= len(self.landscape.grid):
                    continue
                if next_x >= len(self.landscape.grid[0]):
                    continue
                if self.landscape.grid[next_y][next_x] == 0:
                    continue
                if self.landscape.grid[next_y][next_x] == 2:
                    continue
                if self.landscape.grid[next_y][next_x] == 4:
                    continue
                if (next_x, next_y) in visited:
                    continue
                visited.add((next_x, next_y))
                parent[(next_x, next_y)] = current_x, current_y
                queue.append((next_x, next_y))
        if (self.x, self.y) not in parent:
            return None
        path = []
        current = (self.x, self.y)
        while current != (start_x, start_y):
            path.append(current)
            current = parent[current]
        path.reverse()
        return path

    def moveEnemy(self, i, j):
        grid = self.landscape.grid
        if self.withinXDist(i, j, 8):
            path = self.bfs(i, j)
            nextMove = None
            if path is not None:
                nextMove = path[0]
            if nextMove is not None:
                if grid[nextMove[1]][nextMove[0]] == 5:
                    self.die()
                grid[nextMove[1]][nextMove[0]] = 3
                grid[j][i] = 1
        else:
            rand = random.randint(1, 4)
            if (
                rand == 1
                and grid[j - 1][i] != 0
                and grid[j - 1][i] != 3
                and grid[j - 1][i] != 4
            ):
                grid[j][i] = 1
                grid[j - 1][i] = 3
            if (
                rand == 2
                and grid[j + 1][i] != 0
                and grid[j + 1][i] != 3
                and grid[j + 1][i] != 4
            ):
                grid[j][i] = 1
                grid[j + 1][i] = 3
            if (
                rand == 3
                and grid[j][i - 1] != 0
                and grid[j][i - 1] != 3
                and grid[j][i - 1] != 4
            ):
                grid[j][i] = 1
                grid[j][i - 1] = 3
            if (
                rand == 4
                and grid[j][i + 1] != 0
                and grid[j][i + 1] != 3
                and grid[j][i + 1] != 4
            ):
                grid[j][i] = 1
                grid[j][i + 1] = 3

    def moveEnemies(self):
        enemies = []
        gSize = len(self.landscape.grid)
        for i in range(gSize):
            for j in range(gSize):
                if self.landscape.grid[j][i] == 3:
                    enemies.append((i, j))
        for x, y in enemies:
            if self.landscape.grid[y][x] == 3:
                self.moveEnemy(x, y)


def main():
    return


if __name__ == "__main__":
    main()
