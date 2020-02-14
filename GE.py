from classes import Automaton, Node, Transition, buildAutomatonFromStrings, _buildAutomatonFromString, mergeAutomaton, buildAutomatonFromMergeList, flattenMergeList, getListPos
import random


def test():
    strs = ["cars", "drives", "good"]
    auto = buildAutomatonFromStrings(strs, "G")
    print(auto.checkInput("drives"))
    print(mergeAutomaton(auto, [0,1,1,2,5,5,1,3,6,6,2,6,2,3,4]))
    tempauto = mergeAutomaton(auto, [6,4,7,0,2,3,5,4,1,0,2,7,6,5,5])
    print(tempauto)
    print(tempauto.checkInput("good"))





def testFitness(auto, s_neg):
    performance = 0
    for i in s_neg:
        if (not(auto.checkInput(i))):
            performance += 1
    return performance

def buildAndTest(arr, MCA, s_neg):
    newauto = mergeAutomaton(MCA, arr)
    fitness = testFitness(newauto, s_neg)
    print("Correctly rejected {} incorrect words out of 5".format(fitness))
    return fitness

def crossOver(arr, arr2):
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
    listno = random.randint(0,1)
    if (random.randint(0,20) == 0):
        returnarr[listno] = mutate(returnarr[listno])
    return returnarr

def generateNewSampleElement(ssize):
    arr = []
    for x in range(ssize):
        arr.append(random.randint(0, ssize - 1))
    return arr

def mutate(arr):
    pos = random.randint(0, len(arr) - 1)
    arr[pos] = random.randint(0, len(arr) - 1)
    return flattenMergeList(arr)

try:
    _s_pos = open("regex.txt", "r")
    _s_neg = open("regex-.txt", "r")
    s_pos = s_neg = []
    s_pos = [line.rstrip('\n') for line in _s_pos]
    s_neg = [line.rstrip('\n') for line in _s_neg]
    _s_pos.close()
    _s_neg.close()
except:
    print("File not found!")
    exit()
MCA = buildAutomatonFromStrings(s_pos, "Q")

samples = []
for i in range(10):
    samples.append(flattenMergeList(generateNewSampleElement(MCA.getSize())))


fitnessarr = [0 for i in range(len(samples))]

for i in range(100):
    for x in range(len(samples)):
        fitnessarr[x] = buildAndTest(samples[x], MCA, s_neg)
    if (len(s_neg) in fitnessarr):   #    WIN CONDITION
        print("Correct Automaton Found \n{}".format(mergeAutomaton(MCA, samples[fitnessarr.index(len(s_neg))])))
        exit()
    pos1 = pos2 = random.randint(0,len(samples) - 1)
    while(pos2 == pos1):
        pos2 = random.randint(0, len(samples) - 1)
    temparr = crossOver(samples[pos1], samples[pos2])
    samples[pos1] = flattenMergeList(temparr[0])
    samples[pos2] = flattenMergeList(temparr[1])
