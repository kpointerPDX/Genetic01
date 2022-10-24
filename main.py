import Robot
import Field

# Global simulation variables:
worldDims = 7
worldObstacles = 5
worldStartPos = (3, 0)
worldStartFacing = (0, 1)
worldNumRobots = 1
worldNumGenerations = 1
worldTrialTimeLimit = 1000


class World:                # Master superclass which contains all robots and manages simulations
    def __init__(self):
        self.generations = list[list[Robot.Robot]](())
        self.fitnessLog = list[list[float]](())
        for i in range(0, worldNumGenerations):
            self.fitnessLog.append(list[float](()))
            for j in range(0, worldNumRobots):
                self.fitnessLog[i].append(0.0)

    # Prints currently active robot's current state to the screen
    def printWorld(self, currentGen, currentRobot):
        robotPos = self.generations[currentGen][currentRobot].position
        for i in range(0, self.generations[currentGen][currentRobot].field.dims):
            line = " "
            for j in range(0, self.generations[currentGen][currentRobot].field.dims):
                cell = (i, j)
                if cell == robotPos:
                    line += self.generations[currentGen][currentRobot].char
                else:
                    line += self.generations[currentGen][currentRobot].field.cells[i][j]
            print(line)

    # Prints overall results of a given simulation
    def printSimReport(self, time, gen, robot):
        self.printWorld(gen, robot)
        print("Time: ", time, "\t Collisions: ", self.generations[gen][robot].collisions)
        print("Overall fitness score: ", self.fitnessLog[gen][robot])
        print()

    # Runs simulations for each robot in each generation,
    def runSim(self):
        for g in range(0, worldNumGenerations):
            self.generations.append(list[Robot.Robot](()))
            for r in range(0, worldNumRobots):
                self.generations[g].append(Robot.Robot(Field.Field(worldDims, worldObstacles), worldStartPos, worldStartFacing))
                while self.generations[g][r].seesGoal:
                    del self.generations[g][r]
                    self.generations[g].append(Robot.Robot(Field.Field(worldDims, worldObstacles), worldStartPos, worldStartFacing))
                trialRunning = True
                t = 0
                while trialRunning and t < worldTrialTimeLimit:
                    nextMove = self.generations[g][r].AI.getNextMove(self.generations[g][r])
                    if nextMove == "turnLeft":
                        self.generations[g][r].turnLeft(1)
                    elif nextMove == "turnRight":
                        self.generations[g][r].turnRight(1)
                    elif nextMove == "moveForward":
                        self.generations[g][r].move()
                    elif nextMove == "moveBack":
                        self.generations[g][r].reverse()
                    else:
                        print("ERROR: Invalid instruction received from AI, ", nextMove)
                    if self.generations[g][r].seesGoal:
                        trialRunning = False
                self.fitnessLog[g][r] = self.generations[g][r].calculateFitness(t)
                self.printSimReport(t, g, r)


# Initialize world, field, and robot:
theWorld = World()
theWorld.runSim()
