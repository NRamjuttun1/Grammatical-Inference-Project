strings = []
for x in range(1000):
    sstring = ""
    numsymbols = 1
    i = 0
    temp = x
    while(x >= 26**numsymbols):
        numsymbols += 1
    for i in range(1, numsymbols + 1):
        power = numsymbols - i
        print("Power is {}".format(power))
        print("Temp is {}".format(temp))
        count = temp//(26**power)
        print("Count is {}".format(count))
        temp = temp%(26**power)
        print("Temp is now {}".format(temp))
        print("Count before is {}".format(count))
        count = chr(65+count)
        print("New Count is now {}".format(count))
        sstring += count
    if (sstring not in strings):
        strings.append(sstring)
        print("Symbols for {} are {}".format(x, sstring))
    else:
        print("String already exists")
        exit()
