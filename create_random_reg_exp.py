from classes import Automaton, Node, Transition, buildAutomatonFromStrings, _buildAutomatonFromString, mergeAutomaton, buildAutomatonFromMergeList, flattenMergeList, getListPos
import random

def getAlphabet():
    alphabet = []
    msg = "Enter Character for alphabet (Press Enter To Finish):\n"
    value = input(msg)
    while(not value == ''):
        if (value[0] not in alphabet):
            alphabet.append(value[0])
        else:
            print("Character already exists in Alphabet\n")
        value = input(msg)
    return alphabet

def tryParse(input):
    try:
        newint = int(input)
        return True
    except ValueError:
        return False

def getSize():
    value = ''
    while(not tryParse(value)):
        value = input("Enter the size of the Automaton: \n")
    return int(value)


alphabet = getAlphabet()
poswords = []
negwords = []
exampleAuto = Automaton("E")
size = getSize()
for i in range(size):
    exampleAuto.addNode()
exampleAuto.end.append(exampleAuto.nodes[-1])
#for x in range(size * 2):
failed = 0
while(not failed == 5):
    newtrans = Transition(random.choice(exampleAuto.nodes), random.choice(exampleAuto.nodes), random.choice(alphabet))
    if ((not exampleAuto.checkTransExists(newtrans)) and (exampleAuto.checkNoRepeatSymbol(newtrans))):
        exampleAuto.addNewTrans(newtrans)
        failed = 0
    else:
        failed += 1
print(alphabet)
print(exampleAuto)
print("Determinism = {}".format(exampleAuto.checkDeterministic()))
#print("Positive words -> {}".format(poswords))
#print("Negative words -> {}".format(negwords))
