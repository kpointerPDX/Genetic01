import Robot
import Field

# Global static variables:
worldDims = 7
worldObstacles = 5
worldStartPos = (3, 0)
worldStartFacing = (0, 1)
worldNumRobots = 1
worldNumGenerations = 1


class World:
    # World (container for robots, trials, etc.) constructor:
    def __init__(self):
        self.robots = list(())
        for i in range(0, worldNumRobots):
            thisField = Field.Field(worldDims, worldObstacles)
            self.robots.append(Robot.Robot(thisField, worldStartPos, worldStartFacing))
        self.currentRobot = 0
        self.trialTime = 0
        self.trialRunning = True
        self.numGenerations = worldNumGenerations

    # Calculates next time step for the world
    def tick(self):
        pass    # TODO: implement world.tick() function

    # Prints currently active robot's current state to the screen
    def printWorld(self):
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
theWorld = World()

theWorld.printWorld()
print("Unexplored spaces: ", theWorld.robots[0].field.countUnexplored())
print()

# SIM SCRIPT STARTS HERE:
theWorld.robots[0].turnLeft(1)
theWorld.robots[0].turnLeft(1)
theWorld.robots[0].turnRight(3)
theWorld.robots[0].turnRight(1)
theWorld.printWorld()
print("Unexplored spaces: ", theWorld.robots[0].field.countUnexplored())