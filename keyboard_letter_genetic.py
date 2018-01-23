import csv
from random import shuffle
from pyevolve import G1DList, GSimpleGA, Consts, Initializators, Selectors, Mutators, Crossovers

NUM_PARTS = 26

def read_inputs():
    global probabilities, interkey_intervals
    with open('input-26-S.txt') as input_file:
        lines = input_file.readlines()
        probabilities = lines[3:30]
        for i, line in enumerate(probabilities):
            probabilities[i] = map(float, line.split()[0:27])
        probabilities = probabilities[0:27]
        # print probabilities
        interkey_intervals = lines[31:58]
        for i, line in enumerate(interkey_intervals):
            interkey_intervals[i] = map(int, line.split()[0:27])
        interkey_intervals = interkey_intervals[0:27]
        # print interkey_intervals

def fitness_func(sequence):
    sum = 0
    for i,x in enumerate(sequence):
        for j,y in enumerate(sequence):
            sum += probabilities[x][y]*interkey_intervals[i][j]
    for i,x in enumerate(sequence):
        sum += probabilities[x][26]*interkey_intervals[x][26]
    return sum


def init_pop(genome, **args):
    genome.genomeList = range(0, NUM_PARTS)
    shuffle(genome.genomeList)

def prettify_sequence(sequence):
    print [ chr(65+i) for i in sequence[0:10] ]
    print " ", [ chr(65+i) for i in sequence[10:19] ]
    print "      ", [ chr(65+i) for i in sequence[19:] ]

if __name__ == "__main__":

    read_inputs()

    genome = G1DList.G1DList(NUM_PARTS)
    genome.setParams(rangemin=0, rangemax=NUM_PARTS-1)
    genome.initializator.set(init_pop)

    # Set mutator function
    # genome.mutator.setRandomApply(True)
    genome.mutator.set(Mutators.G1DListMutatorSwap)

    # Set Crossover function
    genome.crossover.set(Crossovers.G1DListCrossoverCutCrossfill)

    # Set evaluation function
    genome.evaluator.set(fitness_func)

    ga = GSimpleGA.GSimpleGA(genome)

    ga.setGenerations(280)

    ga.setPopulationSize(14)
    # ga.setMutationRate(0.16)
    # ga.setCrossoverRate(0.80)

    # Set Selection scheme
    # ga.selector.set(Selectors.GRouletteWheel)
    ga.selector.set(Selectors.GTournamentSelector)

    # Set type of objective/ fitness function: Convergence
    ga.setMinimax(Consts.minimaxType["minimize"])
    ga.evolve(freq_stats=50)
    ans = ga.bestIndividual()
    # print ans
    print "Fitness:", fitness_func(ans)
    prettify_sequence(ans)

    ideal_sequence = ['Q', 'J', 'P', 'U', 'R', 'L', 'D', 'C', 'K', 'Z', 'X', 'B', 'M', 'O', 'E', 'A', 'N', 'G', 'V', 'F', 'Y', 'S', 'T', 'H', 'I', 'W']
    ideal_genome = [ord(i)-65 for i in ideal_sequence]
    print "***** Ideal ***** Fitness:", fitness_func(ideal_genome)
    # prettify_sequence(ideal_genome)
