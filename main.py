import Robot
import Field

# Global simulation variables:
worldDims = 7
worldObstacles = 5
worldStartPos = (3, 0)
worldStartFacing = (0, 1)
worldNumRobots = 10
worldNumGenerations = 250
worldTrialTimeLimit = 200
worldDebug = False


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

    # Writes fitness log to text file
    def writeLog(self):
        f = open("simLog.txt", "a")
        f.write("\n\n")
        f.write("============\n")
        f.write("  NEW LOG:\n")
        f.write("============\n")
        for g in range(0, len(self.fitnessLog)):
            lineString = "gen " + str(g) + ":\n"
            f.write(lineString)
            lineString = ""
            for r in range(3, len(self.fitnessLog[g])):
                lineString += "\t" + str(self.fitnessLog[g][r]) + "\n"
            lineString += "  1st: " + str(self.fitnessLog[g][1]) + "\n  2nd: " + str(self.fitnessLog[g][2]) + "\n"
            lineString += "  Best: " + str(self.fitnessLog[g][0]) + "\n"
            f.write(lineString)
            f.write("\n")
        f.write("\n")

    # Runs simulations for each robot in each generation,
    def runSim(self):
        for g in range(0, worldNumGenerations):
            self.generations.append(list[Robot.Robot](()))
            lastGenWinner1 = 0                                                                                          # TODO: implement end-of-gen logging
            lastGenWinner2 = 0
            if g > 0:
                bestFitness = 0.0
                for r in range(0, worldNumRobots):
                    if self.fitnessLog[g-1][r] >= bestFitness:
                        lastGenWinner2 = lastGenWinner1
                        bestFitness = self.fitnessLog[g - 1][r]
                        lastGenWinner1 = r
                print("gen ", g-1, " winner: ", bestFitness)
                self.fitnessLog[g-1].insert(0, lastGenWinner2)
                self.fitnessLog[g-1].insert(0, lastGenWinner1)
                self.fitnessLog[g-1].insert(0, bestFitness)
            for r in range(0, worldNumRobots):
                if g == 0:
                    self.generations[g].append(Robot.Robot(Field.Field(worldDims, worldObstacles), worldStartPos, worldStartFacing))
                else:
                    self.generations[g].append(Robot.Robot(Field.Field(worldDims, worldObstacles), worldStartPos, worldStartFacing, self.generations[g-1][lastGenWinner1], self.generations[g-1][lastGenWinner2]))
                while self.generations[g][r].seesGoal:
                    del self.generations[g][r]
                    if g == 0:
                        self.generations[g].append(Robot.Robot(Field.Field(worldDims, worldObstacles), worldStartPos, worldStartFacing))
                    else:
                        self.generations[g].append(Robot.Robot(Field.Field(worldDims, worldObstacles), worldStartPos, worldStartFacing, self.generations[g - 1][lastGenWinner1], self.generations[g - 1][lastGenWinner2]))
                trialRunning = True
                t = 0
                while trialRunning and t < worldTrialTimeLimit:
                    nextMove = self.generations[g][r].AI.getNextMove(self.generations[g][r])
                    if nextMove == "turnLeft":
                        self.generations[g][r].turnLeft(1)
                        #self.generations[g][r].path += "L"
                    elif nextMove == "turnRight":
                        self.generations[g][r].turnRight(1)
                        #self.generations[g][r].path += "R"
                    elif nextMove == "moveForward":
                        self.generations[g][r].move()
                        #self.generations[g][r].path += "F"
                    elif nextMove == "moveBack":
                        self.generations[g][r].reverse()
                        #self.generations[g][r].path += "B"
                    else:
                        print("ERROR: Invalid instruction received from AI, ", nextMove)
                    if self.generations[g][r].seesGoal:
                        trialRunning = False
                    else:
                        t += 1
                self.fitnessLog[g][r] = self.generations[g][r].calculateFitness(t)
                #print(self.generations[g][r].path)
                #self.printSimReport(t, g, r)
        self.printWorld(worldNumGenerations-1, self.fitnessLog[g-2][1])
        self.writeLog()


# Initialize world, field, and robot:
theWorld = World()
theWorld.runSim()
