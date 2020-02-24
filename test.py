x = 569
sstring = ""
numsymbols = (x//26) + 1
for i in range(numsymbols):
    count = 0
    power = numsymbols - 1 - i
    temp = x
    count = temp//26**power
    temp = temp & (26**power)
    count = chr(65+count)
    sstring += count
print(sstring)
