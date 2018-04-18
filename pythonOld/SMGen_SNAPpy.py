

functionsCalled = []


def _get_func_string(event):
    if event[0] not in functionsCalled:
        functionsCalled.append(event[0])
    ret = "("
    for e in event:
        ret = ret + e + ", "
    return ret + ")"


def _print_event(name, event):
    s = '        ("' + name + '", '
    pos = 0
    if name == "T":
        s = s + event[pos] + ",  "
        pos += 1
    if name != "@":
        s = s + '"' + event[pos] + '",'
        pos += 1

    if pos < (len(event)):
        if type(event[pos]) == list:
            for e in event[pos:]:
                s = s + _get_func_string(e) + ", "
        else:
            s = s + _get_func_string(event[pos:])

    print s + "),"


def _print_state(name, state):
    print '    ("' + name + '",'

    if "@" in state:
        _print_event("@", state["@"])

    if "T" in state:
        _print_event("T", state["T"])

    for n, e in state.iteritems():
        if n != "@" and n != "T":
            _print_event(n, e)

    print '    ),'


def print_states(sm, org):
    print "stateMachineStates = ("
    for name in org:
        state = sm[name]
        _print_state(name, state)
    print ")"
    print ''
    for f in functionsCalled:
        print "# " + f
