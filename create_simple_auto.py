from classes import Automaton, Node, Transition, cAutomaton, colourNode
import random

def getPosWords(_auto, ls):
    auto, terminating = _auto.getComplementAutomaton(True)
    words = []
    for x in range(auto.getSize() * 100):
        current = auto.start
        word = ""
        count = 0
        end = False
        while(end == False) and (count < auto.getSize() * 3):
            count += 1
            if (current not in auto.end):
                if (word not in words):
                    if (word not in ls):
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

def getNegWords(auto, ls, i = 2):
    words = []
    for x in range(auto.getSize() * i):
        word = ""
        for x in range(auto.getSize() * (i-1)):
            if (random.randint(0,1)):
                word += random.choice(auto.getAlphabet())
                if (not auto.checkInput(word)):
                    if (word not in words) and (word not in ls):
                        words.append(word)
    return words

a = Automaton("A")
for x in range(2):
    a.addNode()
a.addTransition(a.start, a.findNode(1), "b")
a.addTransition(a.findNode(1), a.findNode(2), "b")
a.addTransition(a.findNode(1), a.findNode(1), "a")
a.addTransition(a.findNode(2), a.findNode(1), "a")
a.addTransition(a.findNode(2), a.findNode(2), "b")
a.addEnd(a.findNode(2))
words = []
while(len(words) < 25):
    words += getPosWords(a, words)
neg_words = getNegWords(a, [])
while(len(neg_words) < 25):
    neg_words += getNegWords(a, neg_words, len(neg_words))
try:
    pos_file = open("ex+.txt", "w")
    neg_file = open("ex-.txt", "w")
    sstring = ""
    for x in words:
        sstring += x + "\n"
    pos_file.write(sstring)
    sstring = ""
    for x in neg_words:
        sstring += x + "\n"
    neg_file.write(sstring)
    pos_file.close()
    neg_file.close()
except:
    print("ERROR")
