import Field
import Robot
import neat
import os
import pickle

# Global simulation variables:
DEBUG_OUTPUT = False
STATS_REPORTER = True
worldDims = 7
worldObstacles = 4
worldStartPos = (3, 0)
worldStartFacing = (0, 1)
worldTimeLimit = 100
worldNumGenerations = 10
worldTrialsPerGen = 10
worldConfirmSims = 3
# Global fitness function weights:
fitnessWeight_Explored = 0.5
fitnessWeight_Move = 0.0
fitnessWeight_Turn = 0.0
fitnessWeight_Collide = -2.0
fitnessWeight_TimeFactor = 0.5


def remove(index, rs, ns, gs):
    rs.pop(index)
    gs.pop(index)
    ns.pop(index)


def evalGenomes(genomes, configIn):
    robots = []
    gs = []
    nets = []

    for gID, g in genomes:
        robots.append(Robot.Robot(worldDims, worldObstacles, worldStartPos, worldStartFacing))
        gs.append(g)
        nets.append(neat.nn.FeedForwardNetwork.create(g, configIn))
        g.fitness = 0.0

    for n in range(0, worldTrialsPerGen):
        simRunning = True
        t = 0
        while simRunning:
            #print(str(len(robots)))
            if len(robots) == 0 or t >= worldTimeLimit:
                simRunning = False
            for i, thisRobot in enumerate(robots):
                if not thisRobot.seesGoal:
                    # NOTE: adding/removing inputs requires adjusting 'num_inputs' value in config.txt
                    inputs = (#thisRobot.field.countUnexplored(),                                                        # values fed into input nodes on the neural net
                              thisRobot.getImmediateExplorable(),
                              thisRobot.frontDistance,
                              #thisRobot.position[0],
                              #thisRobot.position[1],
                              thisRobot.findCFromEdge(),
                              thisRobot.findRFromEdge(),
                              t)
                    output = nets[i].activate(inputs)                                                                   # output # selected by the network, based on inputs
                    if DEBUG_OUTPUT:                                                                                    # print raw input/output values if flag is True
                        print("i:", str(i), "\t", inputs, "\t", output)
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
                        if thisRobot.reverse():                                                                         # NOTE: REVERSE OUTPUT CURRENTLY DISABLED IN CONFIG
                            pass
                        else:
                            gs[i].fitness += fitnessWeight_Collide
                    else:
                        print("ERROR: Invalid instruction received from neural net, ", decision)
                    if thisRobot.seesGoal:
                        gs[i].fitness += float(worldTimeLimit - t) * fitnessWeight_TimeFactor
                        thisRobot.field = Field.Field(worldDims, worldObstacles)
            t += 1
    for i, r in enumerate(robots):
        remove(i, robots, nets, gs)


def testGenome(testNet):
    for i in range(0, worldConfirmSims):
        testRobot = Robot.Robot(worldDims, worldObstacles, worldStartPos, worldStartFacing)
        print("Initial state:")
        testRobot.print()
        simRunning = True
        t = 0
        while simRunning:
            inputs = (#testRobot.field.countUnexplored(),
                      testRobot.getImmediateExplorable(),
                      testRobot.frontDistance,
                      #testRobot.position[0],
                      #testRobot.position[1],
                      testRobot.findCFromEdge(),
                      testRobot.findRFromEdge(),
                      t)
            output = testNet.activate(inputs)
            decision = output.index(max(output))
            collision = False
            if decision == 0:
                testRobot.turnLeft(1)
            elif decision == 1:
                testRobot.turnRight(1)
            elif decision == 2:
                if not testRobot.move():
                    collision = True
            elif decision == 3:
                if not testRobot.reverse():                                                                             # NOTE: REVERSE OUTPUT CURRENTLY DISABLED IN CONFIG
                    collision = True
            else:
                print("ERROR: Invalid instruction received from neural net, ", decision)
            print("End of sim step ", str(t), ":")
            testRobot.print()
            if collision:
                print("COLLISION!\n")
            else:
                print()
            if testRobot.seesGoal:
                testRobot.timeToGoal = t
                print("GOAL FOUND!!!\n")
            if testRobot.seesGoal or t >= worldTimeLimit:
                simRunning = False
            t += 1
        if testRobot.seesGoal:
            print("====================================")
            print("  Sim ended with robot SUCCESSFUL!")
            print("====================================\n\n")
        else:
            print("========================================")
            print("  Sim ended with robot UNSUCCESSFUL...")
            print("========================================\n\n")


# Setup for training the NEAT algorithm
def runNEAT(runConfigIn):
    pop = neat.Population(runConfigIn)                                                                                  # create genome population from config
    if STATS_REPORTER:
        pop.add_reporter(neat.StdOutReporter(True))                                                                         # creates object which displays data for each gen
        stats = neat.StatisticsReporter()
        pop.add_reporter(stats)
    winner = pop.run(evalGenomes, worldNumGenerations)                                                                  # return fittest genome after specified # of generations
    with open("best.pickle", "wb") as f:                                                                                # write genome object using pickle subsystem
        pickle.dump(winner, f)


# Test routine for selected best genome
def testBest(testConfigIn):
    with open("best.pickle", "rb") as f:                                                                                # read genome object using pickle
        winner = pickle.load(f)
    winnerNet = neat.nn.FeedForwardNetwork.create(winner, testConfigIn)                                                 # create new neural net from saved genome
    testGenome(winnerNet)                                                                                               # run tests using resultant neural net


# ENTRY POINT: prepare NEAT subsystem configuration
if __name__ == "__main__":                                                                                              # prevents execution when loaded as a module
    local_dir = os.path.dirname(__file__)                                                                               # get current directory path
    config_path = os.path.join(local_dir, "config.txt")                                                                 # append name of config file
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,                   # create config object using defaults and config file
                                neat.DefaultStagnation, config_path)
    runNEAT(config)                                                                                                     # pass config object to training function
    testBest(config)                                                                                                    # pass config object to testing function
