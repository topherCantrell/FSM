
def _isNumeric(s):
    for c in s:
        if c < "0" or c > "9":
            return False
    return True

functionsCalled = []


def _get_func_string(fns):

    ret = ""
    firstFunction = True

    while len(fns) > 0:
        if type(fns[0]) == list:
            a = _get_func_string(fns[0])
            if not firstFunction:
                ret = ret + ', "%%"'
            ret = ret + a
            firstFunction = False
            fns = fns[1:]
        else:
            if not firstFunction:
                ret = ret + ', "%%"'
            if fns[0] not in functionsCalled:
                functionsCalled.append(fns[0])
            firstFunction = False
            ret = ret + ", FN_" + fns[0]
            fns = fns[1:]
            while len(fns) > 0:
                if type(fns[0]) == list:
                    break
                ret = ret + ", " + fns[0]
                fns = fns[1:]

    return ret


def _print_state(name, state):
    print name

    if "@" in state:
        ts = state["@"]
        print '  word "##!##"' + _get_func_string(ts)

    if "T" in state:
        ts = state["T"]
        tm = ts[0]
        ns = ts[1]
        print '  word "##T##",' + tm + ',@' + ns + _get_func_string(ts[2:])

    for evt in state:
        if evt == "@" or evt == "T":
            continue
        ts = state[evt]
        ns = ts[0]
        print '  word "##' + evt + '##", @' + ns + _get_func_string(ts[1:])
    print '  word "@@"'


def print_states(sm, org):
    print "' ----- ---------------------------- -----"
    print "' ----- FSM GENERATED CODE HERE DOWN -----"
    print "' ----- ---------------------------- -----"
    print ""
    print "PRI mainLoop(state) | fn, retVal"
    print ""
    print "  FSM.init(state,@@0)"
    print "  repeat"
    print "    ' Wait for a function request"
    print "    repeat while FSM.isFunctionRequest == 0"
    print ""
    print "    ' Dispatch the function"
    print "    fn := FSM.getFunctionNumber"
    print "    retVal := dispatch(fn)"
    print ""
    print "    ' Return any response"
    print "    FSM.replyToFunctionRequest(retVal)"
    print ""
    print "DAT"
    print ""
    print "fsmData"
    print ""
    for s in org:
        v = sm[s]
        _print_state(s, v)
        print ""

    print "CON"
    x = 256
    print "'  GetEvent"
    for f in functionsCalled:
        print "'  " + f
    print ""
    for f in functionsCalled:
        print "  FN_" + f + " = " + str(x)
        x = x + 1

    print ""
    print "PRI dispatch(fn)"
    print "  CASE fn"
    print "    0:"
    print "      return GetEvent"
    for f in functionsCalled:
        print "    FN_" + f + ":"
        print "      return " + f
