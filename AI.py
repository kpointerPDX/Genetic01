import random


class AI:
    class Genome:
        class Gene:
            # Prototype constructor for "Gene" (node in neural net graph structure):
            def __init__(self):
                self.value = 0.0

            # Stores fed value:
            def setValue(self, valueIn):
                self.value = valueIn

        class StrategyGene(Gene):
            strategyList = list(("random", "spin and move", "spiral", "grid"))  # List of general search strategies

            # Constructor for "StrategyGene" (special node which stores general search strategy):
            def __init__(self, strategyGeneIn=None):
                super().__init__()
                if strategyGeneIn is None:
                    self.strategy = "random"
                else:
                    self.strategy = strategyGeneIn.strategy

        class InputGene(Gene):
            # Constructor for "InputGene" (node which connects sensory inputs to outputs):
            def __init__(self, inputGeneIn=None, connectedGeneIn=None):
                super().__init__()
                if inputGeneIn is not None:
                    self.value = inputGeneIn.value
                    self.connection = inputGeneIn.connection
                    self.connectionWeight = inputGeneIn.connectionWeight
                elif connectedGeneIn is not None:
                    self.connection = connectedGeneIn
                    self.connectionWeight = random.uniform(-1.0, 1.0)
                else:
                    self.connection = None
                    self.connectionWeight = 0.0

            # Takes fed value, stores it, and passes weighted value to connected node:
            def calcValue(self, valueIn):
                self.value = valueIn
                if self.connection is not None:
                    self.connection.calcValue(valueIn * self.connectionWeight)

        class OutputGene(Gene):
            # Constructor for "OutputGene" (node which triggers action outputs):
            def __init__(self, copyGeneIn=None):
                super().__init__()
                if copyGeneIn is not None:
                    self.scalar = copyGeneIn.scalar
                else:
                    self.scalar = random.uniform(-1.0, 1.0)

            # Takes value fed by connection, applies scalar, and stores:
            def calcValue(self, valueIn):
                self.setValue(valueIn * self.scalar)

        # Genome constructor (container for Gene graph; is sequenced for inheritance):
        def __init__(self, parent1=None, parent2=None):
            if parent1 is None or parent2 is None:
                self.strategy = self.StrategyGene()
                self.turnLeft = self.OutputGene()
                self.turnRight = self.OutputGene()
                self.moveForward = self.OutputGene()
                self.moveBack = self.OutputGene()
                self.outGenes = list((self.turnLeft, self.turnRight, self.moveForward, self.moveBack))
                self.unexploredSpaces = self.InputGene(None, random.choice(self.outGenes))
                self.distanceInFront = self.InputGene(None, random.choice(self.outGenes))
                self.xCoord = self.InputGene(None, random.choice(self.outGenes))
                self.yCoord = self.InputGene(None, random.choice(self.outGenes))
                self.xToEdge = self.InputGene(None, random.choice(self.outGenes))
                self.yToEdge = self.InputGene(None, random.choice(self.outGenes))
                self.inGenes = list((self.unexploredSpaces, self.distanceInFront, self.xCoord, self.yCoord,
                                     self.xToEdge, self.yToEdge))
            else:
                sequence1 = parent1.getSequence()
                sequence2 = parent2.getSequence()
                reverseOrder = random.choice([True, False])
                split = random.randint(0, sequence1.length())
                self.setFromSequence(self.mergeSequences(reverseOrder, sequence1, sequence2, split))

        # Encodes Gene graph as a list to be split and reassembled between 2 parents to create new generation:
        def getSequence(self):
            outSequence = tuple((self.strategy, self.turnLeft, self.turnRight, self.moveForward, self.moveBack,
                                self.unexploredSpaces, self.distanceInFront, self.xCoord, self.yCoord,
                                self.xToEdge, self.yToEdge))
            return outSequence

        # Sets Genome according to input sequence
        def setFromSequence(self, sequence):
            self.strategy = self.StrategyGene(sequence[0])
            self.turnLeft = self.OutputGene(sequence[1])
            self.turnRight = self.OutputGene(sequence[2])
            self.moveForward = self.OutputGene(sequence[3])
            self.moveBack = self.OutputGene(sequence[4])
            self.unexploredSpaces = self.InputGene(sequence[5])
            self.distanceInFront = self.InputGene(sequence[6])
            self.xCoord = self.InputGene(sequence[7])
            self.yCoord = self.InputGene(sequence[8])
            self.xToEdge = self.InputGene(sequence[9])
            self.yToEdge = self.InputGene(sequence[10])

        # Creates new sequence from random combination of 2 parent sequences:
        def mergeSequences(self, reverseOrder, sequence1, sequence2, split):
            newSequence = list[self.Gene]
            if reverseOrder:
                for i in range(0, split):
                    newSequence.append(sequence2[i])
                for i in range(split, len(sequence1)):
                    newSequence.append(sequence1[i])
            else:
                for i in range(0, split):
                    newSequence.append(sequence1[i])
                for i in range(split, len(sequence2)):
                    newSequence.append(sequence2[i])
            return newSequence

    # AI constructor (container class for genome and base logic):
    def __init__(self, parent1=None, parent2=None):
        if (parent1 is None) or (parent2 is None):
            self.genome = AI.Genome()
        else:
            self.genome = AI.Genome(parent1, parent2)

    # Determines AI's next move by search strategy and inputs processed through genome:
    def getNextMove(self):
        if self.genome.strategy == "spin and move":
            pass    # TODO: implement logic for 'spin and move' strategy
        elif self.genome.strategy == "spiral":
            pass    # TODO: implement logic for 'spiral' strategy
        elif self.genome.strategy == "grid":
            pass    # TODO: implement logic for 'grid' strategy
        else:
            pass    # TODO: implement logic for 'random' strategy
