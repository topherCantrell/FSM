import sys

file_name = sys.argv[1]
mode = sys.argv[2]

# mode = "Propeller"
# mode = "Python"
# file_name = "seq.txt"

with open(file_name) as f:
    raw = f.readlines()

lines = []
for r in raw:
    r = r.strip()
    if len(r) > 0:
        lines.append(r)
nl = 0

while nl < len(lines):
    firstComment = True
    data = ["", "",
            "", "",
            "", "",
            "", "",
            "", "",
            "", "",
            "", "",
            "", ""]

    while lines[nl].startswith("#"):
        if firstComment and lines[nl] != "#":
            print ""
        firstComment = False
        if mode == "Propeller":
            print "'" + lines[nl][1:]
        else:
            print lines[nl]
        nl = nl + 1
    varName = lines[nl]
    nl = nl + 1
    pos = 0
    for x in xrange(7, -1, -1):
        for y in xrange(8):
            c = lines[nl + y][x]
            if c == 'R':
                data[pos] = '0' + data[pos]
                data[pos + 1] = '1' + data[pos + 1]
            elif c == 'G':
                data[pos] = '1' + data[pos]
                data[pos + 1] = '0' + data[pos + 1]
            elif c == 'Y':
                data[pos] = '1' + data[pos]
                data[pos + 1] = '1' + data[pos + 1]
            else:
                data[pos] = '0' + data[pos]
                data[pos + 1] = '0' + data[pos + 1]
        pos = pos + 2

    if mode == "Prop":
        g = "im_" + varName + " byte "
        for d in data:
            g = g + "$%02X," % int(d, 2)
        g = g[0:-1]

    else:  # Python
        g = "im_" + varName + " = '"
        for d in data:
            g = g + "\\x%02X" % int(d, 2)
        g = g + "'"

    print g
    nl = nl + 8
