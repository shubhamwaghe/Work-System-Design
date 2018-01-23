# Author: Shubham Waghe
# Roll No: 13MF3IM17
# Description: WSD-II Assignment-3
import random, math

NUMBER_OF_ITERATIONS = 1000
MARKOV_CHAIN_LENGTH = 100
temperature = 1000
SIGMA = 0.95

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

def calculate_cost(sequence):
    sum = 0
    for i,x in enumerate(sequence):
        for j,y in enumerate(sequence):
            sum += probabilities[x][y]*interkey_intervals[i][j]
    for i,x in enumerate(sequence):
        sum += probabilities[x][26]*interkey_intervals[x][26]
    return sum

def prettify_sequence(sequence):
    print [ chr(65+i) for i in sequence[0:10] ]
    print " ", [ chr(65+i) for i in sequence[10:19] ]
    print "      ", [ chr(65+i) for i in sequence[19:] ]

if __name__ == "__main__":

    print "Running,..."
    # Read inputs
    read_inputs()

    # Generate initial sequence
    current_sequence = range(0,26)
    random.shuffle(current_sequence)
    # print current_sequence
    starting_cost = calculate_cost(current_sequence)

    # print "**** Initial **** Cost:", starting_cost
    old_cost = starting_cost
    modified_sequence = current_sequence
    # print current_sequence
    # print [ chr(65+i) for i in current_sequence ]

    # for _ in xrange(NUMBER_OF_ITERATIONS):
    while temperature > 0.001:

        for _ in xrange(MARKOV_CHAIN_LENGTH):

            # Choosing 1-swap or 2-swap with equal probability
            niters = 1 if random.uniform(0,1) < 0.5 else 2 

            for k in xrange(niters):

                # Swap operator between two indices i and j    
                i,j = random.sample(set(range(26)), 2)
                p_cost = calculate_cost(modified_sequence)
                modified_sequence[i], modified_sequence[j] = modified_sequence[j], modified_sequence[i]
                if p_cost < old_cost:

                    # Calculate critical probability value
                    critical_value = math.exp((p_cost - old_cost)/(temperature))
                    # print critical_value
                    if random.uniform(0,1) < critical_value:
                        # print "******Changed*****",i,j, temperature, critical_value
                        current_sequence = modified_sequence
                        old_cost = p_cost

        # Temperature updation
        temperature = temperature*SIGMA

    print "**** Final **** Cost:", calculate_cost(current_sequence)
    print current_sequence
    prettify_sequence(current_sequence)
    print "Done!"

