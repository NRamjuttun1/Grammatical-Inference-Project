from classes import Automaton, Node, Transition, buildAutomatonFromStrings, _buildAutomatonFromString, mergeAutomaton, buildAutomatonFromMergeList, flattenMergeList, getListPos
import random

def getAlphabet():
    alphabet = []
    msg = "Enter Character for alphabet (Enter blank to finish):\n"
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

def getPosWords(_auto):
    auto, terminating = _auto.getComplementAutomaton(True)
    words = []
    for x in range(auto.getSize()):
        current = auto.start
        word = ""
        count = 0
        end = False
        while(end == False) and (count < auto.getSize() * 10):
            count += 1
            if (current not in auto.end):
                if (word not in words):
                    words.append(word)
            if (len(words) < auto.getSize() * 2):
                trans = auto.findTransFromNode(current)
                if (not len(trans) == 0):
                    delete_list = []
                    for x in trans:
                        if (x.getEnd() == terminating):
                            delete_list.append(x)
                    for x in delete_list:
                        trans.remove(x)
                if (not len(trans) == 0):
                    random_trans = random.choice(trans)
                    if (not random_trans.getEnd() == terminating):
                        current = random_trans.getEnd()
                        word += random_trans.getSymbol()
                else:
                    end = True
            else:
                end = True
    return words

def getNegWords(auto):
    words = []
    for x in range(auto.getSize() * 2):
        word = ""
        for x in range(auto.getSize()):
            if (random.randint(0,1)):
                word += random.choice(alphabet)
                if (not auto.checkInput(word)):
                    if (word not in words):
                        words.append(word)
    return words

def checkUniqueSymbols(sstring, list):
    str_ls = []
    for letter in sstring:
        str_ls.append(letter)
    done = False
    i = 0
    j = -1
    while(done == False):
        j += 1
        if (len(str_ls) == 0):
            return False
        if (j == len(list[i])):
            i += 1
            j = 0
        if (i == len(list)):
            done = True
        if (done == False):
            if (list[i][j] in str_ls):
                str_ls = removeAllFromList(list[i][j], str_ls)
    return True

def removeAllFromList(el, arr):
    ls = []
    for x in arr:
        if (not x==el):
            ls.append(x)
    return ls




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
print(exampleAuto)
print("Determinism = {}".format(exampleAuto.checkDeterministic()))
poswords = getPosWords(exampleAuto)
if (len(poswords) < 10):
    print("Positive words found is {} regular expression may not be inferred from examples".format(len(poswords)))
u_poswords = []
while(not len(u_poswords) == 5):
    ran_pos = random.choice(poswords)
    if (checkUniqueSymbols(ran_pos, poswords) == False):
        u_poswords.append(ran_pos)
        poswords.remove(ran_pos)
negwords = getNegWords(exampleAuto)
u_negwords = negwords[-5:]
negwords = negwords[:-5]
print(poswords)
print(u_poswords)
try:
    pos_file = open("regex+.txt", "w")
    neg_file = open("regex-.txt", "w")
    u_pos_file = open("regex+_u.txt", "w")
    u_neg_file = open("regex-_u.txt", "w")
    sstring = ""
    for x in poswords:
        sstring += x + "\n"
    pos_file.write(sstring)
    sstring = ""
    for x in negwords:
        sstring += x + "\n"
    neg_file.write(sstring)
    sstring = ""
    for x in u_poswords:
        sstring += x + "\n"
    u_pos_file.write(sstring)
    for x in u_negwords:
        sstring += x + "\n"
    u_neg_file.write(sstring)
    u_neg_file.close()
    u_pos_file.close()
    pos_file.close()
    neg_file.close()
except:
    print("File not found!")
    exit()
#print("Positive words -> {}".format(poswords))
#print("Negative words -> {}".format(negwords))
i = 0
for x in poswords:
    if (exampleAuto.checkInput(x) == False):
        print("OH BOY")
        i+=1
