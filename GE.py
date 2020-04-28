from classes import *
import random, time


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



def buildAndTest(arr, MCA, s_neg, u_pos):
    newauto = mergeAutomaton(MCA, arr)
    fitness = _testFitness(newauto, s_neg, u_pos)
    #print("Correctly rejected {} incorrect words out of {}".format(fitness, len(s_neg)))
    return fitness

def _testFitness(auto, s_neg, u_pos):
    performance = 0
    for i in s_neg:
        if (not(auto.checkInput(i))):
            performance += 1
    for x in u_pos:
        if (auto.checkInput(x)):
            performance += 1
    return performance

def crossOver(samples, fitnessarr, pos1, pos2):
    temparr = _crossOver(samples[pos1], samples[pos2])
    samples[pos1] = flattenMergeList(temparr[0])
    samples[pos2] = flattenMergeList(temparr[1])
    fitnessarr[pos1] = buildAndTest(samples[pos1], MCA, s_neg, u_pos)
    fitnessarr[pos2] = buildAndTest(samples[pos2], MCA, s_neg, u_pos)

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

def mutate(arr, fitnessarr, ptr):
    pos = random.randint(0, len(arr) - 1)
    arr[pos] = random.randint(0, len(arr) - 1)
    arr = flattenMergeList(arr)
    fitnessarr[ptr] = buildAndTest(arr, MCA, s_neg, u_pos)

start_time = time.time()
try:
    _s_pos = open("regex+.txt", "r")
    _s_neg = open("regex-.txt", "r")
    _u_pos = open("regex+_u.txt", "r")
    _u_neg = open("regex-_u.txt", "r")
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
optimalFitness = len(s_neg) + len(u_pos)
samplesize = 10
samples = []
for i in range(samplesize):
    check = True
    while(check):
        newsample = flattenMergeList(generateNewSampleElement(MCA.getSize()))
        fitness_1 = buildAndTest(newsample, MCA, s_neg, u_pos)
        if (not(fitness_1 == optimalFitness)):
            check = False
        samples.append(newsample)
        #samples.append(flattenMergeList(generateNewSampleElement(MCA.getSize())))
fitnessarr = [0 for i in range(len(samples))]
for x in range(len(samples)):
    fitnessarr[x] = buildAndTest(samples[x], MCA, s_neg, u_pos)
print("Current Fitnesses : {} /{}".format(fitnessarr, optimalFitness))
count = 0
populations = 0
win = False
while(win == False):
    count += 1
    if (optimalFitness in fitnessarr):   #    WIN CONDITION
        correct_auto = mergeAutomaton(MCA, samples[fitnessarr.index(len(s_neg))])
        print("Automaton with max score found in\n{}\n{} generations \n {} new populations has to be generated".format(correct_auto, count, populations))
        neg_true = pos_false = 0
        for x in s_neg:
            if correct_auto.checkInput(x) == True:
                neg_true += 1
        for x in s_pos:
            if correct_auto.checkInput(x) == False:
                pos_false += 1
        neg_true = pos_false = 0
        for x in u_neg:
            if correct_auto.checkInput(x) == True:
                neg_true += 1
        for x in u_pos:
            if correct_auto.checkInput(x) == False:
                pos_false += 1
        if (pos_false == 0) and (neg_true == 0):
            print("Unknwon Positives rejected = {}/{} \nUnknown Negatives accepted = {}/{}".format(pos_false, u_pos, neg_true, u_neg))
            win = True
        else:
            print("Unknown words not classified correctly")
    if (win == False):
        checkcount = 0
        min1, min2 = find2Min(fitnessarr)
        max = findMax(fitnessarr)
        printFitness(fitnessarr)
        if (checkcount > (samplesize - 2)): #checkcount and this statement is for optimisation purposes and should not be included in the testing stage
            samples = []
            for i in range(samplesize):
                samples.append(flattenMergeList(generateNewSampleElement(MCA.getSize())))
            print("Samples not satisfactory! New Population generated\n{}".format(fitnessarr))
            populations += 1
            count = 0
        crossOver(samples, fitnessarr, min1, min2)
        #if (random.randint(0,totalfitness//2) == 0):
        mutate(samples[max], fitnessarr, max)
        print("Mins were {} and {} Max was {}".format(min1, min2, max))

timed = ("--- %s seconds ---" % (time.time() - start_time))
print("Correct Automaton found!")
print(timed)
with open('genetic_time.txt', 'w') as fh:
    fh.write(timed)
exit()
