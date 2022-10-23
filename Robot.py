import AI


class Robot:
    # Facings and display characters that correspond with each other:
    facingMap = [(0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1)]
    charMap = [">", "7", "^", "`", "<", "L", "V", ","]      # TODO: find better diagonal characters

    """# Default constructor:
    def __init__(self):
        self.position = (0, 0)
        self.facing = (0, 1)
        self.char = self.getChar()
        self.field = None
        self.collisions = 0
        self.seesGoal = False
        self.frontDistance = self.look(self.field)
        self.AI = AI.AI()"""

    """# Specific constructor with random AI:
    def __init__(self, field, position, facing):
        self.position = position
        self.facing = facing
        self.char = self.getChar()
        self.field = field
        self.collisions = 0
        self.seesGoal = False
        self.frontDistance = self.look(self.field)
        self.AI = AI.AI()"""

    # Specific constructor with AI from parents:
    def __init__(self, field, position, facing, parent1=None, parent2=None):
        self.position = position
        self.facing = facing
        self.char = self.getChar()
        self.field = field
        self.collisions = 0
        self.seesGoal = False
        self.frontDistance = self.look()
        if parent1 is None or parent2 is None:
            self.AI = AI.AI()
        else:
            self.AI = AI.AI(parent1.AI, parent2.AI)

    # turns robot left by multiples of 45 degrees:
    def turnLeft(self, turnAngle):
        turnAngle = turnAngle % 8
        currentAngle = self.facingMap.index(self.facing)
        self.facing = self.facingMap[(currentAngle + turnAngle) % 8]
        self.char = self.getChar()
        self.frontDistance = self.look()

    # turns robot right by multiples of 45 degrees:
    def turnRight(self, turnAngle):
        turnAngle = turnAngle % 8
        currentAngle = self.facingMap.index(self.facing)
        self.facing = self.facingMap[(currentAngle - turnAngle) % 8]
        self.char = self.getChar()
        self.frontDistance = self.look()

    # Returns robot's current display character, depending on the direction it faces:
    def getChar(self):
        currentFacing = self.facingMap.index(self.facing)
        return self.charMap[currentFacing]

    # Returns the adjacent coordinates in the specified direction from a specified coordinate:
    def nextCoord(self, current, facing):
        destination = (current[0] + facing[0], current[1] + facing[1])
        return destination

    # Check spaces in a line "in front" of robot until finding an obstacle; returns distance to obstacle:
    def look(self):
        distance = 0
        self.seesGoal = False                                               # updates robot's seesGoal state
        currentPos = self.position
        while self.field.validCoord(currentPos):
            if self.field.getCoord((currentPos[0], currentPos[1])) == "X":
                self.seesGoal = True                                        # sets seesGoal to True if seen
            else:
                self.field.cells[currentPos[0]][currentPos[1]] = "_"
            distance += 1
            currentPos = self.nextCoord(currentPos, self.facing)
        return distance

    # Move robot one space in the direction it is facing; fails and increments collisions if space contains an obstacle:
    def move(self):
        moveTarget = self.nextCoord(self.position, self.facing)
        if self.field.validCoord(moveTarget):
            self.position = moveTarget
        else:
            print("COLLISION!")
            self.collisions += 1
