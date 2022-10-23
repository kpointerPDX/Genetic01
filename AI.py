import random

class AI:
    class Genome:
        class Gene:
            def __init__(self):
                self.value = 0.0

            def setValue(self, valueIn):
                self.value = valueIn

        class StrategyGene(Gene):
            strategyList = list(("random", "spin and move", "spiral", "grid"))

            def __init__(self):
                super().__init__()
                self.strategy = random.choice(self.strategyList)

            def __init__(self, stratGeneIn):
                super().__init__()
                self.strategy = stratGeneIn.strategy

        class InputGene(Gene):
            def __init__(self):
                super().__init__()
                self.connection = None
                self.connectionWeight = 0

            def __init__(self, outputGeneIn):
                super().__init__()
                self.connection = outputGeneIn
                self.connectionWeight = random.uniform(-1.0, 1.0)

            def __init__(self, geneIn):
                super().__init__()
                self.connection = geneIn.connection
                self.connectionWeight = geneIn.connectionWeight

            def calcValue(self, valueIn):
                self.value = valueIn
                if self.connection is not None:
                    self.connection.calcValue(valueIn * self.connectionWeight)

        class OutputGene(Gene):
            def __init__(self):
                super().__init__()
                self.scalar = random.uniform(-1.0, 1.0)

            def __init__(self, geneIn):
                super().__init__()
                self.scalar = geneIn.scalar

            def calcValue(self, valueIn):
                self.setValue(valueIn * self.scalar)

        def __init__(self):
            self.strategy = self.StrategyGene()
            self.turnLeft = self.OutputGene()
            self.turnRight = self.OutputGene()
            self.moveForward = self.OutputGene()
            self.moveBack = self.OutputGene()
            self.outGenes = list((self.turnLeft, self.turnRight, self.moveForward, self.moveBack))
            self.unexploredSpaces = self.InputGene(random.choice(self.outGenes))
            self.distanceInFront = self.InputGene(random.choice(self.outGenes))
            self.xCoord = self.InputGene(random.choice(self.outGenes))
            self.yCoord = self.InputGene(random.choice(self.outGenes))
            self.xToEdge = self.InputGene(random.choice(self.outGenes))
            self.yToEdge = self.InputGene(random.choice(self.outGenes))
            self.inGenes = list((self.unexploredSpaces, self.distanceInFront, self.xCoord, self.yCoord,
                                 self.xToEdge, self.yToEdge))

        def __init__(self, parent1, parent2):
            sequence1 = parent1.getSequence()
            sequence2 = parent2.getSequence()
            reverseOrder = random.choice([True, False])
            split = random.randint(0, sequence1.length())
            self.setFromSequence(self.mergeSequences(reverseOrder, sequence1, sequence2, split))

        def getSequence(self):
            """return tuple((self.outGenes + self.inGenes))"""
            """outSequence = list[self.Gene]
            for i in self.inGenes:
                outSequence.append(i)
            for o in self.outGenes:
                outSequence.append(o)
            return outSequence"""
            """return self.outGenes + self.inGenes"""
            """outSequence = list[self.Gene]
            outSequence.append(self.strategy, self.turnLeft, self.turnRight, self.moveForward, self.moveBack,\
                          self.unexploredSpaces, self.distanceInFront, self.xCoord, self.yCoord,\
                          self.xToEdge, self.yToEdge)"""
            outSequence = tuple((self.strategy, self.turnLeft, self.turnRight, self.moveForward, self.moveBack,
                          self.unexploredSpaces, self.distanceInFront, self.xCoord, self.yCoord,
                          self.xToEdge, self.yToEdge))
            return outSequence

        def setFromSequence(self, sequence):
            """self.strategy = sequence[0][0]
            self.turnLeft = sequence[0][1]
            self.turnRight = sequence[0][2]
            self.moveForward = sequence[0][3]
            self.moveBack = sequence[0][4]
            self.unexploredSpaces = sequence[1][0]
            self.distanceInFront = sequence[1][1]
            self.xCoord = sequence[1][2]
            self.yCoord = sequence[1][3]
            self.xToEdge = sequence[1][4]
            self.yToEdge = sequence[1][5]"""
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

    def __init__(self):
        self.genome = AI.Genome()

    def __init__(self, parent1, parent2):
        self.genome = AI.Genome(parent1, parent2)

    def getNextMove(self):
        if self.genome.strategy == "spin and move":
            pass    # TODO: implement logic for 'spin and move' strategy
        elif self.genome.strategy == "spiral":
            pass    # TODO: implement logic for 'spiral' strategy
        elif self.genome.strategy == "grid":
            pass    # TODO: implement logic for 'grid' strategy
        else:
            pass    # TODO: implement logic for 'random' strategy
