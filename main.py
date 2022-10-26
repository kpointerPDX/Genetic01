import Field
import Robot
import neat
import os
import pickle

# Global simulation variables:
worldDims = 7
worldObstacles = 8
worldStartPos = (3, 0)
worldStartFacing = (0, 1)
worldTimeLimit = 100
worldNumGenerations = 1000
worldTrialsPerGen = 10
worldConfirmSims = 2
# Global fitness function weights:
fitnessWeight_Explored = 0.01
fitnessWeight_Move = 4.0
fitnessWeight_Turn = 0.02
fitnessWeight_Collide = -2.0
fitnessWeight_Time = -0.01


def remove(index, rs, ns, gs):
    rs.pop(index)
    gs.pop(index)
    ns.pop(index)


# Prints currently active robot's current state to the screen
def printRobot(robot):
    robotPos = robot.position
    for i in range(0, robot.field.dims):
        line = " "
        for j in range(0, robot.field.dims):
            cell = (i, j)
            if cell == robotPos:
                line += robot.char
            else:
                line += robot.field.cells[i][j]
        print(line)


def evalGenomes(genomes, config):
    robots = []
    gs = []
    nets = []

    for gID, g in genomes:
        robots.append(Robot.Robot(worldDims, worldObstacles, worldStartPos, worldStartFacing))
        gs.append(g)
        nets.append(neat.nn.FeedForwardNetwork.create(g, config))
        g.fitness = 0.0

    for n in range(0, worldTrialsPerGen):
        simRunning = True
        t = 0
        while simRunning:
            if len(robots) == 0 or t >= worldTimeLimit:
                simRunning = False
            for i, thisRobot in enumerate(robots):
                if not thisRobot.seesGoal:
                    output = nets[i].activate((thisRobot.field.countUnexplored(), thisRobot.frontDistance, thisRobot.position[0], thisRobot.position[1], thisRobot.findCFromEdge(), thisRobot.findRFromEdge(), t))
                    decision = output.index(max(output))
                    if decision == 0:
                        thisRobot.turnLeft(1)
                        gs[i].fitness += fitnessWeight_Turn
                        gs[i].fitness += float(thisRobot.newlyExplored) * fitnessWeight_Explored
                    elif decision == 1:
                        thisRobot.turnRight(1)
                        gs[i].fitness += fitnessWeight_Turn
                        gs[i].fitness += float(thisRobot.newlyExplored) * fitnessWeight_Explored
                    elif decision == 2:
                        if thisRobot.move():
                            gs[i].fitness += fitnessWeight_Move
                        else:
                            gs[i].fitness += fitnessWeight_Collide
                    elif decision == 3:
                        if thisRobot.reverse():
                            pass
                        else:
                            gs[i].fitness += fitnessWeight_Collide
                    else:
                        print("ERROR: Invalid instruction received from neural net, ", decision)
                    if thisRobot.seesGoal:
                        gs[i].fitness += float(worldTimeLimit - t) / 2.0
                        thisRobot.field = Field.Field(worldDims, worldObstacles)
            t += 1
    for i, r in enumerate(robots):
        remove(i, robots, nets, gs)


def testGenome(testNet):
    for i in range(0, worldConfirmSims):
        testRobot = Robot.Robot(worldDims, worldObstacles, worldStartPos, worldStartFacing)
        simRunning = True
        t = 0
        while simRunning:
            t += 1
            print("sim step: ", str(t))
            printRobot(testRobot)
            output = testNet.activate((testRobot.field.countUnexplored(), testRobot.frontDistance, testRobot.position[0], testRobot.position[1], testRobot.findCFromEdge(), testRobot.findRFromEdge(), t))
            decision = output.index(max(output))
            if decision == 0:
                testRobot.turnLeft(1)
            elif decision == 1:
                testRobot.turnRight(1)
            elif decision == 2:
                if not testRobot.move():
                    print("COLLISION!")
            elif decision == 3:
                if not testRobot.reverse():
                    print("COLLISION!")
            else:
                print("ERROR: Invalid instruction received from neural net, ", decision)
            if testRobot.seesGoal:
                testRobot.timeToGoal = t
                print("\nGOAL FOUND!!!")
            if testRobot.seesGoal or t >= worldTimeLimit:
                simRunning = False


# Setup for the NEAT algorithm"
def runNEAT(config):
    global pop
    pop = neat.Population(config)
    winner = pop.run(evalGenomes, worldNumGenerations)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)


def testBest(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    winnerNet = neat.nn.FeedForwardNetwork.create(winner, config)
    testGenome(winnerNet)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    runNEAT(config)
    testBest(config)
