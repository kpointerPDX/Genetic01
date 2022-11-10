import Field


class Robot:
    # Facings and display characters that correspond with each other
    facingMap = [(0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1)]
    charMap = [">", "┓", "^", "┏", "<", "┗", "v", "┛"]

    # Specific constructor with AI from parents
    def __init__(self, fieldDims, fieldObstacles, position, facing):
        self.position = position
        self.facing = facing
        self.char = self.getChar()
        self.exploredLast = 0
        self.explored = 0
        self.newlyExplored = 0
        self.seesGoal = True
        while self.seesGoal:
            self.field = Field.Field(fieldDims, fieldObstacles)
            self.frontDistance = self.look()
        self.trialNum = 0
        self.trialTime = 0

    # turns robot left by multiples of 45 degrees
    def turnLeft(self, turnAngle):
        turnAngle = turnAngle % 8
        currentAngle = self.facingMap.index(self.facing)
        self.facing = self.facingMap[(currentAngle + turnAngle) % 8]
        self.char = self.getChar()
        self.frontDistance = self.look()

    # turns robot right by multiples of 45 degrees
    def turnRight(self, turnAngle):
        turnAngle = turnAngle % 8
        currentAngle = self.facingMap.index(self.facing)
        self.facing = self.facingMap[(currentAngle - turnAngle) % 8]
        self.char = self.getChar()
        self.frontDistance = self.look()

    # Returns robot's current display character, depending on the direction it faces
    def getChar(self):
        currentFacing = self.facingMap.index(self.facing)
        return self.charMap[currentFacing]

    # Returns the adjacent coordinates in the specified direction from a specified coordinate
    def nextCoord(self, current, facing):
        destination = (current[0] + facing[0], current[1] + facing[1])
        return destination

    # finds distance from the nearest top/bottom edge of the field (negative if top edge is closest)
    def findRFromEdge(self):
        rows = self.field.dims
        currentRow = self.position[0]
        if currentRow < (rows/2.0):
            return -1 * currentRow
        else:
            return rows - 1 - currentRow

    # finds distance from the nearest left/right edge of the field (negative if left edge is closest)
    def findCFromEdge(self):
        cols = self.field.dims
        currentCol = self.position[1]
        if currentCol < (cols/2.0):
            return -1 * currentCol
        else:
            return cols - 1 - currentCol

    # finds percentage of adjacent explorable spaces that are explored
    def getImmediateExplorable(self):
        explorable = 0.0
        explored = 0.0
        for f in self.facingMap:
            checkPos = self.nextCoord(self.position, f)
            if self.field.validCoord(checkPos):
                contents = self.field.cells[checkPos[0]][checkPos[1]]
                if contents == "_":
                    explored += 1.0
                    explorable += 1.0
                elif contents == ".":
                    explorable += 1.0
        return float(float(explored)/float(explorable))

    # Check spaces in a line "in front" of robot until finding an obstacle; returns distance to obstacle
    def look(self):
        distance = 0
        self.seesGoal = False                                                                                           # updates robot's seesGoal state
        currentPos = self.position
        while self.field.validCoord(currentPos):
            if self.field.getCoord((currentPos[0], currentPos[1])) == "X":
                self.seesGoal = True                                                                                    # sets seesGoal to True if seen
            else:
                self.field.cells[currentPos[0]][currentPos[1]] = "_"
            distance += 1
            currentPos = self.nextCoord(currentPos, self.facing)
        self.exploredLast = self.explored
        self.explored = self.field.countExplored()
        self.newlyExplored = self.explored - self.newlyExplored
        return distance

    # Move robot one space in the direction it is facing; fails and increments collisions if destination is invalid
    def move(self):
        moveTarget = self.nextCoord(self.position, self.facing)
        if self.field.validCoord(moveTarget):
            self.position = moveTarget
            return True
        else:
            return False

    # Move robot one space in the direction it is facing; fails and increments collisions if destination is invalid
    def reverse(self):
        moveTarget = self.nextCoord(self.position, (self.facing[0]*-1, self.facing[1]*-1))
        if self.field.validCoord(moveTarget):
            self.position = moveTarget
            return True
        else:
            return False

    # Prints the current state of the robot's field:
    def print(self):
        for i in range(0, self.field.dims):
            line = " "
            for j in range(0, self.field.dims):
                cell = (i, j)
                if cell == self.position:
                    line += self.char
                else:
                    line += self.field.cells[i][j]
            print(line)
