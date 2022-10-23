from math import floor
import random

class Field:
    def __init__(self):
        self.dims = 5
        self.cells = [['.']]
        self.obstacles = 3
        self.goalPosition = (self.dims-1, self.dims-1)
        self.build()
        self.unexplored = self.countUnexplored()

    def __init__(self, dims, obstacles):
        self.dims = max(3, min(25, dims))
        self.cells = [['.']]
        self.obstacles = max(0, min(obstacles, max(1, floor((dims-2)**2)/2)))
        self.goalPosition = (0, 0)
        self.build()

    def build(self):
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
                    c = randC - 1
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

    def getCoord(self, coord):
        if coord[0] < 0 or coord[1] < 0 or coord[0] >= self.dims or coord[1] >= self.dims:
            return None
        else:
            return self.cells[coord[0]][coord[1]]

    def validCoord(self, coord):
        checkCoord = self.getCoord(coord)
        if checkCoord == None or checkCoord == "O":
            return False
        else:
            return True

    def setExplored(self, coord):
        pass

    def countUnexplored(self):
        count = 0
        for i in range(0, self.dims):
            for j in range(0, self.dims):
                if self.cells[i][j] == ".":
                    count += 1
        return count

#    def placeRobot(self, Robot, position):
#        if position[0] < 0 or position[1] < 0 or position[0] >= self.dims or position[1] >= self.dims:
#            print("Out of bounds robot placement!")
#        else:
#            robotChars = [">", "7", "^", "`", "<", "L", "V", ","]
#            self.cells[position[0]][position[1]] = ">"