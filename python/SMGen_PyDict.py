

def _popListTerm(g):
    g = g.strip()
    lev = 0
    pos = 0
    while True:
        c = g[pos]
        pos += 1
        if c == "[":
            lev += 1
        elif c == "]":
            lev -= 1
            if lev == 0:
                return (g[1:pos - 1].strip(), g[pos:].strip())


def _stringifyList(fns):
    ret = []

    while True:
        fns = fns.strip()
        if fns == "":
            return ret
        if fns.startswith("["):
            i = fns.index("]")
            sub = fns[1:i]
            ret.append(_stringifyList(sub))
            fns = fns[i + 1:].strip()
            if fns.startswith(","):
                fns = fns[1:].strip()
        else:
            if "," in fns:
                i = fns.index(",")
                a = fns[0:i].strip()
                if a.startswith('"') or a.startswith("'"):
                    a = a[1:-1]
                ret.append(a)
                fns = fns[i + 1:]
            else:
                if fns.startswith('"') or fns.startswith("'"):
                    fns = fns[1:-1]
                ret.append(fns)
                fns = ""


def _parseState(stateStr):
    ret = {}

    while True:
        if ":" not in stateStr:
            return ret
        i = stateStr.index(":")
        ii = stateStr.index('"')
        jj = stateStr.index('"', ii + 1)
        eventName = stateStr[ii + 1:jj]

        (fns, stateStr) = _popListTerm(stateStr[i + 1:])
        ret[eventName] = _stringifyList(fns)

        # print eventName + "   " + str(ret[eventName])


def loadStates(name):

    with open(name) as f:
        raw = f.readlines()

    smText = ""
    fnd = False
    for r in raw:
        if fnd:
            if(r.startswith(")")):
                break
            if "#" in r:
                r = r[0:r.index("#")]
            smText = smText + r.strip()
        else:
            if r.startswith("stateMachineStates"):
                fnd = True

    ret = {}
    orgOrder = []

    while True:
        if "{" not in smText:
            break
        i = smText.index("{")
        j = smText.index("}")

        stateText = smText[i + 1:j]

        stateName = smText[0:i]
        ii = stateName.index('"')
        jj = stateName.index('"', ii + 1)
        stateName = stateName[ii + 1:jj]

        smText = smText[j + 1:]

        state = _parseState(stateText)
        ret[stateName] = state
        orgOrder.append(stateName)

    return (ret, orgOrder)


def _get_func_string(fns):
    ret = ""
    for fn in fns:
        ret = ret + "("
        for term in fn:
            ret = ret + term + ","
        ret = ret + "),"
    return ret


def _print_state(name, state):
    pass


def print_states(sm, org):
    pass
