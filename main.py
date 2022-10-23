import Robot
import Field

# Global static variables:
worldDims = 7
worldObstacles = 5
worldStartPos = (3, 0)
worldStartFacing = (0, 1)
worldNumRobots = 5
worldNumGenerations = 10


class World:
#    # Default constructor (single-robot, single-generation constructor, for debugging purposes):
#    def __init__(self):
#        """self.field = None"""
#        self.robots = list(())
#        self.robots.append(Robot.Robot(Field.Field(worldDims, worldObstacles), worldStartPos, worldStartFacing))
#        self.trialTime = 0
#        self.trialRunning = True
#        self.numGenerations = 1
#
#    # Single-robot, single-generation constructor (for debugging purposes):
#    """def __init__(self, robotIn, fieldIn):"""
#    def __init__(self, robotIn):
#        self.robots = list(())
#        self.robots.append(robotIn)
#        """self.field = fieldIn"""
#        self.currentRobot = 0
#        self.trialTime = 0
#        self.trialRunning = True
#        self.numGenerations = 1
#
    # Robust, multi-robot, multi-generation constructor:
    """def __init__(self, fieldIn, numRobotsIn, numTrialsIn):"""
    def __init__(self):
        self.robots = list(())
        for i in range(0, worldNumRobots):
            thisField = Field.Field(worldDims, worldObstacles)
            self.robots.append(Robot.Robot(thisField, worldStartPos, worldStartFacing))
        """self.field = fieldIn"""
        self.currentRobot = 0
        self.trialTime = 0
        self.trialRunning = True
        self.numGenerations = worldNumGenerations

    # Calculates next time step for the world
    def tick(self):
        pass    # TODO: implement world.tick() function

    # Prints currently active robot's current state to the screen
    def printWorld(self):
        """pos = self.robot.position"""
        robotPos = self.robots[self.currentRobot].position
        for i in range(0, self.robots[self.currentRobot].field.dims):
            line = " "
            for j in range(0, self.robots[self.currentRobot].field.dims):
                cell = (i, j)
                if cell == robotPos:
                    line += self.robots[self.currentRobot].char
                else:
                    line += self.robots[self.currentRobot].field.cells[i][j]
            print(line)


# Initialize world, field, and robot:
"""playField = Field.Field(worldDims, worldObstacles)
robit = Robot.Robot(playField, worldStartPos, worldStartFacing)
theWorld = World(robit, playField)"""
"""theWorld = World(playField, worldNumRobots)"""
theWorld = World(1, 1)

theWorld.printWorld()

# SIM SCRIPT STARTS HERE:
"""print("Unexplored spaces: ", theWorld.field.countUnexplored())
print()
robit.turnLeft(1)
robit.turnLeft(1)
robit.turnRight(3)
robit.turnRight(1)
theWorld.printWorld()
print("Unexplored spaces: ", theWorld.field.countUnexplored())
print()
robit.turnLeft(2)
robit.move(1)
robit.turnLeft(2)
robit.turnRight(4)
theWorld.printWorld()
print("Unexplored spaces: ", theWorld.field.countUnexplored())"""