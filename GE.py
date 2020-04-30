from classes import *
import random, time

test_for_unknowns = True
converge = True

def test():
    strs = ["cars", "drives", "good"]
    auto = buildAutomatonFromStrings(strs, "G")
    print(auto.checkInput("drives"))
    print(mergeAutomaton(auto, [0,1,1,2,5,5,1,3,6,6,2,6,2,3,4]))
    tempauto = mergeAutomaton(auto, [6,4,7,0,2,3,5,4,1,0,2,7,6,5,5])
    print(tempauto)
    print(tempauto.checkInput("good"))

def printFitness(fitness):
    stringg = "["
    for x in fitness:
        stringg += str(x) + ", "
    stringg = stringg[:-2]
    stringg += "]"
    print(stringg)



def buildAndTest(arr, MCA, s_neg, u_pos, u_neg, negs):
    newauto = mergeAutomaton(MCA, arr)
    fitness = _testFitness(newauto, s_neg, u_pos, u_neg, negs)
    #print("Correctly rejected {} incorrect words out of {}".format(fitness, len(s_neg)))
    return fitness

def _testFitness(auto, s_neg, u_pos, u_neg, negs):
    performance = 0
    for i in s_neg:
        if (not(auto.checkInput(i))):
            performance += 1
    if (negs):
        for x in u_pos:
            if (auto.checkInput(x)):
                performance += 1
        for x in u_neg:
            if (not auto.checkInput(x)):
                performance += 1
    return performance

def crossOver(samples, fitnessarr, pos1, pos2, test_for_unknowns, converge = None):
    temparr = _crossOver(samples[pos1], samples[pos2])
    if converge == None:
        samples[pos1] = flattenMergeList(temparr[0])
        samples[pos2] = flattenMergeList(temparr[1])
        fitnessarr[pos1] = buildAndTest(samples[pos1], MCA, s_neg, u_pos, u_neg, test_for_unknowns)
        fitnessarr[pos2] = buildAndTest(samples[pos2], MCA, s_neg, u_pos, u_neg, test_for_unknowns)
    elif (not converge == None):
        samples[converge] = flattenMergeList(temparr[random.randint(0,1)])
        fitnessarr[converge] = buildAndTest(samples[min], MCA, s_neg, u_pos, u_neg, test_for_unknowns)

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

def generateNewSampleElement(ssize):
    arr = []
    for x in range(ssize):
        arr.append(random.randint(0, ssize - 1))
    return arr

def mutate(arr, fitnessarr, ptr, test_for_unknowns):
    pos = random.randint(0, len(arr) - 1)
    arr[pos] = random.randint(0, len(arr) - 1)
    arr = flattenMergeList(arr)
    fitnessarr[ptr] = buildAndTest(arr, MCA, s_neg, u_pos, u_neg, test_for_unknowns)

start_time = time.time()
try:
    _s_pos = open("ex+.txt", "r")
    _s_neg = open("ex-.txt", "r")
    _u_pos = open("ex+_u.txt", "r")
    _u_neg = open("ex-_u.txt", "r")
    s_pos = []
    s_neg = []
    u_pos = []
    u_neg = []
    s_pos = [line.rstrip('\n') for line in _s_pos]
    s_neg = [line.rstrip('\n') for line in _s_neg]
    u_pos = [line.rstrip('\n') for line in _u_pos]
    u_neg = [line.rstrip('\n') for line in _u_neg]
    _s_pos.close()
    _s_neg.close()
    _u_pos.close()
    _u_neg.close()
except():
    print("File not found!")
    exit()
print("Building these stringd")
MCA = buildAutomatonFromStrings(s_pos, "Q")
print("Finished building the MCA")
print(MCA)
if (test_for_unknowns):
    optimalFitness = len(s_neg) + len(u_pos) + len(u_neg)
else:
    optimalFitness = len(s_neg)
samplesize = 10
samples = []
for i in range(samplesize):
    check = True
    while(check):
        newsample = flattenMergeList(generateNewSampleElement(MCA.getSize()))
        fitness_1 = buildAndTest(newsample, MCA, s_neg, u_pos, u_neg, test_for_unknowns)
        if (not(fitness_1 == optimalFitness)):
            check = False
        samples.append(newsample)
        #samples.append(flattenMergeList(generateNewSampleElement(MCA.getSize())))
fitnessarr = [0 for i in range(len(samples))]
for x in range(len(samples)):
    fitnessarr[x] = buildAndTest(samples[x], MCA, s_neg, u_pos, u_neg, test_for_unknowns)
print("Current Fitnesses : {} /{}".format(fitnessarr, optimalFitness))
randcount = count = 0
win = False
pre_min1 = pre_min2 = -1
while(win == False):
    printFitness(fitnessarr)
    count += 1
    if (optimalFitness in fitnessarr):   #    WIN CONDITION
        solution = 0
        for x in range(len(fitnessarr)):
            if fitnessarr[x] == optimalFitness:
                solution = x
        correct_auto = mergeAutomaton(MCA, samples[solution])
        print("Automaton with max score found in\n{}\n{} generations \n Correct Fitness found at position {}".format(correct_auto, count, solution))
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
            crossOver(samples, fitnessarr, max1, max2, findMin(fitnessarr))
        max = findMax(fitnessarr)
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
