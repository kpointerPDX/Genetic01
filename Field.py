from math import floor
import random


class Field:
    # Constructor for Field object (container for search area, goal, and obstacles):
    def __init__(self, dims=5, obstacles=3):
        self.dims = max(3, min(25, dims))
        self.cells = [['.']]
        self.obstacles = max(0, min(obstacles, max(1, int(floor(((dims-2)**2)/2)))))
        self.goalPosition = (0, 0)
        #self.buildRandom()
        # trying alternate, static Fields
        #self.buildStatic_Wall()
        #self.buildStatic_Shield()
        self.buildStatic_Forest()

    # Generates field based on object parameters:
    def buildRandom(self):
        # Build empty field array:
        for i in range(0, self.dims):
            self.cells.append(['.'])
            for j in range(0, self.dims - 1):
                self.cells[i].append('.')

        # Place goal:
        self.goalPosition = (random.randint(0, self.dims-1), random.randint(0, self.dims-1))
        self.cells[self.goalPosition[0]][self.goalPosition[1]] = "X"

        # Place obstacles:
        for i in range(0, self.obstacles):
            validPick = False
            randR = 0
            randC = 0
            while not validPick:
                randR = random.randint(1, self.dims - 2)
                randC = random.randint(1, self.dims - 2)
                if self.cells[randR][randC] == '.':
                    neighbors = 0
                    r = randR - 1
                    while neighbors < 2 and r <= randR + 1:
                        c = randC - 1
                        while neighbors < 2 and c <= randC + 1:
                            if self.cells[r][c] == 'O':
                                neighbors += 1
                            c += 1
                        r += 1
                    if neighbors < 2:
                        validPick = True
            self.cells[randR][randC] = 'O'

    # Generates field based on preset configuration:
    def buildStatic_Wall(self):
        # Setup simple field with wall:
        self.cells.clear()
        self.cells.append(['.', '.', '.', '.', '.', '.', '.'])
        self.cells.append(['.', '.', '.', '.', '.', '.', '.'])
        self.cells.append(['.', '.', '.', 'O', '.', '.', '.'])
        self.cells.append(['.', '.', '.', 'O', '.', '.', '.'])
        self.cells.append(['.', '.', '.', 'O', '.', '.', '.'])
        self.cells.append(['.', '.', '.', '.', '.', '.', '.'])
        self.cells.append(['.', '.', '.', '.', '.', '.', '.'])
        self.obstacles = 3
        self.dims = 7

        # Place goal behind wall:
        self.goalPosition = (3, 4)
        self.cells[self.goalPosition[0]][self.goalPosition[1]] = "X"

    # Generates field based on preset configuration:
    def buildStatic_Shield(self):
        # Setup simple field with wall:
        self.cells.clear()
        self.cells.append(['.', '.', '.', '.', '.', '.', '.'])
        self.cells.append(['.', '.', '.', '.', '.', '.', '.'])
        self.cells.append(['.', '.', '.', '.', 'O', '.', '.'])
        self.cells.append(['.', '.', '.', 'O', '.', '.', '.'])
        self.cells.append(['.', '.', '.', '.', 'O', '.', '.'])
        self.cells.append(['.', '.', '.', '.', '.', '.', '.'])
        self.cells.append(['.', '.', '.', '.', '.', '.', '.'])
        self.obstacles = 5
        self.dims = 7

        # Place goal behind wall:
        self.goalPosition = (3, 4)
        self.cells[self.goalPosition[0]][self.goalPosition[1]] = "X"

    # Generates field based on preset configuration:
    def buildStatic_Forest(self):
        # Setup simple field with wall:
        self.cells.clear()
        self.cells.append(['.', '.', '.', '.', '.', '.', '.'])
        self.cells.append(['.', '.', '.', 'O', '.', '.', '.'])
        self.cells.append(['.', '.', 'O', '.', 'O', '.', '.'])
        self.cells.append(['.', 'O', '.', 'O', '.', 'O', '.'])
        self.cells.append(['.', '.', 'O', '.', 'O', '.', '.'])
        self.cells.append(['.', '.', '.', 'O', '.', '.', '.'])
        self.cells.append(['.', '.', '.', '.', '.', '.', '.'])
        self.obstacles = 9
        self.dims = 7

        # Place goal in forest somewhere:
        if random.randint(0, 1):
            self.goalPosition = (2, 3)
        else:
            self.goalPosition = (4, 3)
        self.cells[self.goalPosition[0]][self.goalPosition[1]] = "X"

    # Returns contents of call at specified coordinates:
    def getCoord(self, coord):
        if coord[0] < 0 or coord[1] < 0 or coord[0] >= self.dims or coord[1] >= self.dims:
            return None
        else:
            return self.cells[coord[0]][coord[1]]

    # Returns whether specified coordinate can be moved/seen through:
    def validCoord(self, coord):
        checkCoord = self.getCoord(coord)
        if checkCoord is None or checkCoord == "O":
            return False
        else:
            return True

    # Tallies and returns total number of explored spaces on the field:
    def countExplored(self):
        count = 0
        for i in range(0, self.dims):
            for j in range(0, self.dims):
                if self.cells[i][j] == "_":
                    count += 1
        return count

    # Tallies and returns total number of unexplored spaces on the field:
    def countUnexplored(self):
        count = 0
        for i in range(0, self.dims):
            for j in range(0, self.dims):
                if self.cells[i][j] == ".":
                    count += 1
        return count
