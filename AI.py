import math
import random

inputCount = 6                                                                                                          # total count of AI inputs
outputCount = 4                                                                                                         # total count of AI outputs


class AI:               # The class which acts as the "brain" for the robot, containing its neural network and genome
    mutationChance = 100                                                                                                # 1/X chance of a mutation when reproducing
    mutationFactor = 2.0                                                                                                # factor by which a value is mutated

    class AIInput:          # The "input node" class on the simple neural network used to determine the AI's next move
        def __init__(self, inputPrototype=None):
            self.connectionWeights = list[float](())
            self.rawOutputs = list[float](())
            for i in range(0, outputCount):
                if inputPrototype is None:                                                                              # if no prototype was given, assign weight randomly:
                    self.connectionWeights.append(random.uniform(-10.0, 10.0))
                else:                                                                                                   # if prototype was given, copy weight value:
                    for j in inputPrototype.connectionWeights:
                        self.connectionWeights.append(inputPrototype.connectionWeights[j])
                self.rawOutputs.append(0.0)                                                                                # in either case, initialize raw outputs to 0

        def mutate(self):                       # Performs random mutation on input node
            indexToMutate = random.randint(0, outputCount)
            valueToMutate = self.connectionWeights[indexToMutate]
            isDecrease = random.choice([True, False])
            if isDecrease:
                AI.mutationFactor *= -1
            self.connectionWeights[indexToMutate] += valueToMutate * AI.mutationFactor                                  # adds/subtracts multiple of connection weight

        def feedInput(self, valueIn):           # Calculates raw output values based on fed input
            for i in range(0, len(self.connectionWeights)):
                self.rawOutputs[i] = valueIn * self.connectionWeights[i]

        def getRawOutput(self, index):          # Returns raw output value from specified index
            if index < 0 or index >= len(self.rawOutputs):
                print("ERROR: Queried raw output values with invalid index ", index, "!")
                return 0.0
            else:
                return self.rawOutputs[index]

    class AIOutput:         # The "output node" class on the AI's neural network; collects and normalizes output values
        def __init__(self, outputPrototype=None):
            self.value = 0.0
            if outputPrototype is None:                                                                                 # if no prototype, set bias with minor initial randomness
                self.bias = random.uniform(0.75, 1.25)
            else:                                                                                                       # otherwise, copy value from prototype
                self.bias = outputPrototype.bias

        def mutate(self):               # Performs random mutation on output
            multiplyVsDivide = random.choice([True, False])
            if multiplyVsDivide:
                self.bias += (2.0 - self.bias) / AI.mutationFactor                                                      # increase by 1/mutationFactor of difference from 2
            else:
                self.bias -= self.bias / AI.mutationFactor                                                              # decrease by value/mutationFactor
            # note "self-correcting" mutation algorithm: larger changes toward middle when value is near the extremes

        def resetOutputValue(self):     # Clears previously held output value
            self.value = 0.0

        def addValue(self, inValue):    # Accumulates fed input value
            self.value += inValue

        def getRawValue(self):          # Returns raw output value
            return self.value

        def getNormalizedValue(self):   # Returns output value, normalized to between 0 and 1
            normValue = 0.5 + math.tanh(self.value * self.bias) * 0.5                                                   # bias value adjusts "steepness" of tanh curve
            return normValue

    def __init__(self, parent1=None, parent2=None):
        self.outputs = list[self.AIOutput](())                                                                          # list of output nodes, each with a bias scalar
        self.oDict = {                                                                                                  # translates text output names to correct list index
            "turnLeft": 0,
            "turnRight": 1,
            "moveForward": 2,
            "moveBack": 3
        }
        self.invODict = {                                                                                               # inverse oDict to get move from index
            0: "turnLeft",
            1: "turnRight",
            2: "moveForward",
            3: "moveBack"
        }
        self.inputs = list[self.AIInput](())                                                                            # list of input nodes, each with output weights
        self.iDict = {                                                                                                  # translates text input names to correct list index
            "unexploredSpaces": 0,
            "distanceInFront": 1,
            "rCoord": 2,
            "cCoord": 3,
            "rFromEdge": 4,
            "cFromEdge": 5
        }
        if parent1 is None or parent2 is None:                                                                          # if <2 parents, assign new random node objects
            for i in range(0, outputCount):
                self.outputs.append(self.AIOutput())
            for i in range(0, inputCount):
                self.inputs.append(self.AIInput())
        else:                                                                                                           # if 2 parents, copy a semi-random combination of nodes
            splitPoint = random.randint(0, inputCount)
            reverseOrder = random.choice([False, True])
            """ algorithm copies one side of the genome from parent 1, and the remainder from parent 2.
                splitPoint: determines where in the genome the split between the two parents is.
                reverseOrder: decides whether to begin with parent 1 or parent 2 before switching to the other at split"""
            for i in range(0, outputCount):                                                                             # create combination of inputs from parents
                if (i <= splitPoint and not reverseOrder) or (i > splitPoint and reverseOrder):
                    self.inputs.append(self.AIInput(parent1.inputs[i]))
                else:
                    self.inputs.append(self.AIInput(parent2.inputs[i]))
                if random.randint(0, AI.mutationChance) == 0:                                                           # 1-in-mutationChance probability to mutate node
                    self.inputs[i].mutate()
            splitPoint = random.randint(0, outputCount)
            reverseOrder = random.choice([False, True])
            for i in range(0, inputCount):                                                                              # repeat for outputs
                if (i <= splitPoint and not reverseOrder) or (i > splitPoint and reverseOrder):
                    self.outputs.append(self.AIOutput(parent1.outputs[i]))
                else:
                    self.outputs.append(self.AIOutput(parent2.outputs[i]))
                if random.randint(0, AI.mutationChance) == 0:                                                           # 1-in-mutationChance probability to mutate node
                    self.outputs[i].mutate()

    # Resets all accumulated output values to 0
    def resetNetwork(self):
        for i in self.outputs:
            i.resetOutputValue()

    # Collects robot's inputs, feeds them to AI, collates resultant output values
    def processInputs(self, robotIn):
        self.inputs[self.iDict["unexploredSpaces"]].feedInput(robotIn.field.countUnexplored())
        self.inputs[self.iDict["distanceInFront"]].feedInput(robotIn.frontDistance)
        self.inputs[self.iDict["rCoord"]].feedInput(robotIn.position[0])
        self.inputs[self.iDict["cCoord"]].feedInput(robotIn.position[1])
        self.inputs[self.iDict["rFromEdge"]].feedInput(robotIn.findRFromEdge())
        self.inputs[self.iDict["cFromEdge"]].feedInput(robotIn.findCFromEdge())
        for o in range(0, outputCount):
            for i in range(0, inputCount):
                self.outputs[o].addValue(self.inputs[i].rawOutputs[o])

    # Determines AI's next move by input values processed through neural network
    def getNextMove(self, robotIn):
        self.resetNetwork()
        self.processInputs(robotIn)
        highestOutput = 0.0
        peakIndex = 0
        for o in range(0, len(self.outputs)):
            val = self.outputs[o].getNormalizedValue()
            if val > highestOutput:
                highestOutput = val
                peakIndex = o
        return self.invODict[peakIndex]

    # Returns current mutation chance
    def getMutationChance(self):
        return self.mutationChance

    # Returns current mutation factor
    def getMutationFactor(self):
        return self.mutationFactor

    # Sets new mutation chance
    def setMutationChance(self, newMutationChance):
        self.mutationChance = newMutationChance

    # Sets new mutation factor
    def setMutationFactor(self, newMutationFactor):
        self.mutationFactor = newMutationFactor
