from classes import *
from create_random_reg_exp import checkUniqueSymbols
import random, time

test_for_unknowns = False
num_unknown_words = 10 #number of unknown words tested if test_for_unknowns is set to True
converge = True
use_pta = True
sample_size = 10
mutation_rate = 0.5
mutate_samples = False
use_examples = False

def printFitness(fitness):
    stringg = "["
    for x in fitness:
        stringg += str(x) + ", "
    stringg = stringg[:-2]
    stringg += "]"
    print(stringg)

def buildAndTest(arr, start_automaton, negative_training_data, unknown_positives, negs):
    newauto = mergeAutomaton(start_automaton, arr)
    fitness = _testFitness(newauto, negative_training_data, unknown_positives, negs)
    #print("Correctly rejected {} incorrect words out of {}".format(fitness, len(negative_training_data)))
    return fitness

def _testFitness(auto, negative_training_data, unknown_positives, negs):
    performance = 0
    for i in negative_training_data:
        if (not(auto.checkInput(i))):
            performance += 1
    if (negs):
        for x in unknown_positives:
            if (auto.checkInput(x)):
                performance += 1
    return performance

def crossOver(samples, fitnessarr, pos1, pos2, test_for_unknowns, converge = None):
    if converge == None:
        temparr = _crossOver(samples[pos1], samples[pos2])
        samples[pos1] = flattenMergeList(temparr[0])
        samples[pos2] = flattenMergeList(temparr[1])
        fitnessarr[pos1] = buildAndTest(samples[pos1], start_automaton, negative_training_data, unknown_positives, test_for_unknowns)
        fitnessarr[pos2] = buildAndTest(samples[pos2], start_automaton, negative_training_data, unknown_positives, test_for_unknowns)
        if (mutate_samples ):
            if (random.randint(1,100) <= mutation_rate*100):
                mutate(samples[pos1], fitnessarr, pos1, test_for_unknowns)
            if (random.randint(1,100) <= mutation_rate*100):
                mutate(samples[pos2], fitnessarr, pos2, test_for_unknowns)
    else:
        arr1, arr2 = __crossover(samples[pos1].copy(), samples[pos2].copy())
        arr1 = flattenMergeList(arr1)
        arr2 = flattenMergeList(arr2)
        arr1_fitness = buildAndTest(arr1, start_automaton, negative_training_data, unknown_positives, test_for_unknowns)
        arr2_fitness = buildAndTest(arr2, start_automaton, negative_training_data, unknown_positives, test_for_unknowns)
        check = False
        if (arr1_fitness > fitnessarr[pos1]):
            samples[pos1] = arr1
            fitnessarr[pos1] = arr1_fitness
            check = True
        elif (arr1_fitness > fitnessarr[pos2]):
            samples[pos2] = arr1
            fitnessarr[pos2] = arr1_fitness
            check = True
        if (arr2_fitness > fitnessarr[pos1]):
            samples[pos1] = arr2
            fitnessarr[pos1] = arr2_fitness
            check = True
        elif (arr2_fitness > fitnessarr[pos2]):
            samples[pos2] = arr2
            fitnessarr[pos2] = arr2_fitness
            check = True
        if (check == False):
            if (not arr1_fitness < fitnessarr[converge]) or (not arr2_fitness < fitnessarr[converge]):
                if arr1_fitness > arr2_fitness:
                    samples[converge] = arr1
                    fitnessarr[converge] = arr1_fitness
                else:
                    samples[converge] = arr2
                    fitnessarr[converge] = arr2_fitness
        if (mutate_samples ):
            if (random.randint(1,100) <= mutation_rate*100):
                mutate(samples[converge], fitnessarr, converge, test_for_unknowns)

def _crossOver(arr, arr2):
    returnarr = [None for i in range(2)]
    split = random.randint(0, len(arr) - 1)
    b_arr = arr[0:split]
    e_arr = arr[split:]
    b_arr2 = arr2[0:split]
    e_arr2 = arr2[split:]
    b_arr = b_arr + e_arr2
    b_arr2 = b_arr2 + e_arr
    returnarr[0] = b_arr
    returnarr[1] = b_arr2
    return returnarr

def __crossover(arr, arr2):
    split = random.randint(0, len(arr) - 1)
    b_arr = arr[0:split]
    e_arr = arr2[split:]
    b_arr += e_arr
    b_arr2 = arr2[0:split]
    e_arr2 = arr[split:]
    b_arr2 += e_arr2
    return b_arr, b_arr2

def generateNewSampleElement(ssize):
    arr = []
    for x in range(ssize):
        arr.append(random.randint(0, ssize - 1))
    return arr

def mutate(arr, fitnessarr, ptr, test_for_unknowns):
    pos = random.randint(0, len(arr) - 1)
    arr[pos] = random.randint(0, len(arr) - 1)
    arr = flattenMergeList(arr)
    fitnessarr[ptr] = buildAndTest(arr, start_automaton, negative_training_data, unknown_positives, test_for_unknowns)

start_time = time.time()
try:
    if (use_examples):
        _positive_training_data = open("ex+.txt", "r")
        _negative_training_data = open("ex-.txt", "r")
        _positive_testing_data = open("ex+_u.txt", "r")
        _negative_testing_data = open("ex-_u.txt", "r")
    else:
        _positive_training_data = open("regex+.txt", "r")
        _negative_training_data = open("regex-.txt", "r")
        _positive_testing_data = open("regex+_u.txt", "r")
        _negative_testing_data = open("regex-_u.txt", "r")
    positive_training_data = []
    negative_training_data = []
    positive_testing_data = []
    negative_testing_data = []
    positive_training_data = [line.rstrip('\n') for line in _positive_training_data]
    negative_training_data = [line.rstrip('\n') for line in _negative_training_data]
    positive_testing_data = [line.rstrip('\n') for line in _positive_testing_data]
    negative_testing_data = [line.rstrip('\n') for line in _negative_testing_data]
    _positive_training_data.close()
    _negative_training_data.close()
    _positive_testing_data.close()
    _negative_testing_data.close()
except():
    print("File not found!")
    exit()
print("Building these strings")
if (use_pta == False):
    start_automaton = buildAutomatonFromStrings(positive_training_data, "Q")
else:
    start_automaton = buildPTA(positive_training_data, "Q", False)
print("Finished building the start_automaton")
print(start_automaton)
unknown_positives = []
if (test_for_unknowns):
    try:
        while(not len(unknown_positives) == num_unknown_words):
            ran_pos = random.choice(positive_training_data)
            if (checkUniqueSymbols(ran_pos, positive_training_data) == False):
                unknown_positives.append(ran_pos)
                positive_training_data.remove(ran_pos)
    except(IndexError):
        print("Not enough positive words for ")
        exit()
    optimalFitness = len(negative_training_data) + len(unknown_positives)
else:
    optimalFitness = len(negative_training_data)
samplesize = sample_size
samples = []
for i in range(samplesize):
    check = True
    while(check):
        newsample = flattenMergeList(generateNewSampleElement(start_automaton.getSize()))
        fitness_1 = buildAndTest(newsample, start_automaton, negative_training_data, unknown_positives, test_for_unknowns)
        if (not(fitness_1 == optimalFitness)):
            check = False
        samples.append(newsample)
        #samples.append(flattenMergeList(generateNewSampleElement(start_automaton.getSize())))
fitnessarr = [0 for i in range(len(samples))]
for x in range(len(samples)):
    fitnessarr[x] = buildAndTest(samples[x], start_automaton, negative_training_data, unknown_positives, test_for_unknowns)
print("Current Fitnesses : {} /{}".format(fitnessarr, optimalFitness))
randcount = count = 0
win = False
pre_min1 = pre_min2 = -1
try:
    while(win == False):
        printFitness(fitnessarr)
        count += 1
        if (optimalFitness in fitnessarr):   #    WIN CONDITION
            solution = 0
            for x in range(len(fitnessarr)):
                if fitnessarr[x] == optimalFitness:
                    solution = x
            correct_auto = mergeAutomaton(start_automaton, samples[solution])
            print("Automaton with max score found in\n{}\n{} generations \n Correct Fitness found at position {}".format(correct_auto, count, solution))
            pos_count = 0
            for x in positive_testing_data:
                if correct_auto.checkInput(x):
                    pos_count += 1
            neg_count = 0
            for x in negative_testing_data:
                if (not correct_auto.checkInput(x)):
                    neg_count += 1
            print("The given Solution correctly accepts {}/{} of Unknown Posotive Testing Examples\nAnd correctly rejects {}/{} of Unknown Negative Testing Examples".format(pos_count, len(positive_testing_data), neg_count, len(negative_testing_data)))
            win = True
        if (win == False):
            min1, min2 = find2Min(fitnessarr)
            if (not converge):
                if (not randcount == 10):
                    crossOver(samples, fitnessarr, min1, min2, test_for_unknowns)
                else:
                    crossOver(samples, fitnessarr, random.randint(0, len(fitnessarr) - 1), random.randint(0, len(fitnessarr) - 1), test_for_unknowns)
            elif (converge):
                max1, max2 = find2Max(fitnessarr, [min1, min2])
                crossOver(samples, fitnessarr, max1, max2, test_for_unknowns, findMin(fitnessarr))
            max = findMax(fitnessarr)
            if (mutate_samples == False):
                if (random.randint(1,100) <= mutation_rate*100):
                    mutate(samples[max], fitnessarr, max, test_for_unknowns)
            if (min1 == pre_min1) and (min2 == pre_min2):
                randcount += 1
            else:
                randcount = 0
            pre_min1 = min1
            pre_min2 = min2

    timed = ("--- %s seconds ---" % (time.time() - start_time))
    print("Correct Automaton found!")
    print(timed)
    with open('genetic_time.txt', 'w') as fh:
        fh.write(timed)

    exit()
except(KeyboardInterrupt):
    max = findMax(fitnessarr)
    finish_auto = mergeAutomaton(start_automaton, samples[max])
    print("The Current Fitnesses are : {}\nThe current generation is {}".format(fitnessarr, count))
    print("The final best solution is : \n{}\nIt scored {}/{}".format(finish_auto, fitnessarr[max], optimalFitness))
    pos_count = 0
    for x in positive_testing_data:
        if finish_auto.checkInput(x):
            pos_count += 1
    neg_count = 0
    for x in negative_testing_data:
        if (not finish_auto.checkInput(x)):
            neg_count += 1
    print("The given Best Solution correctly accepts {}/{} of Unknown Posotive Testing Examples\nAnd correctly rejects {}/{} of Unknown Negative Testing Examples".format(pos_count, len(positive_testing_data), neg_count, len(negative_testing_data)))
