from classes import Automaton, Node, Transition, ColourAutomaton, colourNode
import random

def tryParse(input):
    try:
        newint = int(input)
        return True
    except ValueError:
        return False

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
msg = "Enter Selection: \n1) Add Node(s) \n2) Add Transition \n3) Add End Nodes \n4) Print and Save Examples\n"
value = input(msg)
while(not value == '4'):
    if value == '1':
        num_nodes = "Enter number of nodes to add : \n"
        value1 = input(num_nodes)
        while(not tryParse(value1)):
            value1 = input(num_nodes)
        for i in range(int(value1)):
            a.addNode()
    elif value == '2':
        add_start = "Enter Node to be start node : \n"
        value2 = input(add_start)
        while(not tryParse(value2)):
            value2 = input(add_start)
        start_node = value2
        add_end = "Enter Node to be end node : \n"
        value3 = input(add_end)
        while(not tryParse(value3)):
            value3 = input(add_end)
        end_node = value3
        add_symbol = "Enter symbol for transition : \n"
        value4 = input(add_symbol)
        ssymbol = value4[0]
        a.addTransition(a.findNode(int(value2)), a.findNode(int(value3)), ssymbol)
    elif value == '3':
        add_to_end = "Enter Node to be accepting state"
        value5 = input(add_to_end)
        while(not tryParse(value5)):
            value5 = input(add_to_end)
        accepting_node = value5
        a.addEnd(a.findNode(int(value5)))
    value = input(msg)
words = []
while(len(words) < a.getSize() + 5):
    words += getPosWords(a, words)
neg_words = getNegWords(a, [])
while(len(neg_words) < a.getSize() + 5):
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
print(a)
