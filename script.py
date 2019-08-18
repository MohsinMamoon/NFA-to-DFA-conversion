import json
import itertools
import queue
from functools import reduce
from pip._internal import main as pipmain
pipmain(['install', 'tabulate'])
from tabulate import tabulate


dfa = {}
nfa = {}


file = open("input.json")
inp = json.load(file)
file.close()
out = {
    "states": 0,
    "letters": inp["letters"],
    "t_func": [],
    "start": inp["start"],
    "final": []
}


def fz(SET):
    if type(SET) == int:
        return frozenset([SET])
    else:
        return frozenset(SET)


def union(states):
    if len(states) == 0:
        state = fz({'phi'})
    else:
        state = fz(states)
    if(state not in dfa):
        dfa[state] = State(state, [])
    return state


def trans_union(letter, states):
    final = set([])
    for i in states:
        if letter in dfa[fz([i])].transitions:
            if(dfa[fz([i])].transitions[letter]) != fz({'phi'}):
                final = final.union(set(dfa[fz([i])].transitions[letter]))
    if len(final) == 0:
        return ['phi']
    else:
        return list(final)


class State:
    def __init__(self, name, func=[], automata='dfa'):
        if automata == 'dfa':
            self.name = set(name)
        else:
            self.name = name
        self.In = []
        self.Out = []
        self.transitions = {}

    def addTransition(self, letter, output, automata='dfa'):
        if automata == 'dfa':
            uni = union(output)
            self.transitions[letter] = uni
            if fz(self.name) not in dfa[uni].In:
                dfa[uni].In.append(fz(self.name))
            if uni not in self.Out:
                self.Out.append(uni)
        else:
            self.transitions[letter] = output
            if type(output) == list:
                for i in output:
                    if self.name not in nfa[i].In:
                        nfa[i].In.append(self.name)
                    if i not in self.Out:
                        self.Out.append(i)
            else:
                if self.name not in nfa[output].In:
                    nfa[output].In.append(self.name)
                    if output not in self.Out:
                        self.Out.append(output)


def findsubsets(s, n):
    return [set(i) for i in itertools.combinations(s, n)]


def isfinal(state):
    for i in state:
        if i in inp["final"]:
            out["final"].append(list(state))
            break


def b_s(states):
    states = list(states)
    if len(states) == 1:
        return states[0]
    else:
        return states


def State_construction():
    dfa[fz(["phi"])] = State(["phi"], [])
    s = set([i for i in range(inp["states"])])
    for i in range(1, inp["states"]+1):
        s_temp = findsubsets(s, i)
        for j in s_temp:
            if fz(j) not in dfa:
                dfa[fz(j)] = State(j, [])
                if i == 1:
                    nfa[list(j)[0]] = State(list(j)[0], [], 'nfa')
                isfinal(j)


def Transition_construction():
    for i in inp["letters"]:
        dfa[fz(['phi'])].addTransition(i, ['phi'])

    for transition in inp["t_func"]:
        curr_state = []
        curr_state.append(transition[0])
        curr_state = fz(curr_state)
        let_inp = str(transition[1])
        new_state = transition[2]
        dfa[curr_state].addTransition(let_inp, new_state)
        nfa[b_s(curr_state)].addTransition(let_inp, b_s(new_state), 'nfa')

    for state in dfa:
        inp_s = dfa[state].name
        for inp_l in inp["letters"]:
            if(len(inp_s) > 1):
                dfa[state].addTransition(inp_l, trans_union(inp_l, inp_s))
            if inp_l not in dfa[state].transitions:
                dfa[state].addTransition(inp_l, ['phi'])


def State_reduction():
    empty = queue.Queue(maxsize=pow(pow(2, inp["states"]),2))
    for state in dfa:
        incoming = dfa[state].In
        if(len(incoming) == 0):
            empty.put(state)
        elif(len(incoming) == 1 and incoming[0] == state):
            empty.put(state)

    while (not empty.empty()):
        state = empty.get()
        if state in dfa and state != fz([inp["start"]]):
            inn = dfa[state].In
            if len(inn) == 0 or (len(inn) == 1 and inn[0] == state):
                for i in dfa[state].Out:
                    empty.put(i)
                    dfa[i].In.remove(state)
                dfa.pop(state)
                if(list(state) in out["final"]):
                    out["final"].remove(list(state))


def Generate_output(reduce=0):
    if(reduce):
        State_reduction()
    for s in dfa:
        for let, trans in dfa[s].transitions.items():
            out["t_func"].append([list(dfa[s].name), let, list(dfa[trans].name)])
    out["states"] = len(dfa)


def Print_Table():
    table = []
    for S in dfa:
        row = [".     .     .     .     .     .", dfa[S].name]
        for l in inp["letters"]:
            row.append(set(dfa[S].transitions[l]))
        row.append(".     .     .     .     .     .")
        table.append(row)
    print(tabulate(table, headers=[""] + [x for x in ["State"] + inp["letters"]] + [""]))


def nfa_run(In, curr_state=inp["start"]):
    if not len(In):
        if curr_state in inp["final"]:
            return True
        else:
            return False
    else:
        if In[0] in nfa[curr_state].transitions:
            new_states = nfa[curr_state].transitions[In[0]]
            if type(new_states) == int:
                return nfa_run(In[1:], new_states)
            else:
                return reduce(lambda a, b: a or b, [nfa_run(In[1:], x) for x in new_states])
        else:
            return False


def dfa_run(In):
    curr_state = fz(inp["start"])
    while(len(In)):
        curr_state = dfa[curr_state].transitions[In[0]]
        In = In[1:]
    if dfa[curr_state].bin in out["final"]:
        return True
    else:
        return False
    
    
def testNFA_DFA():
    number = int(input("How many inputs? "))
    while(number):
        In = input("Enter input string: ")
        if(nfa_run(In)):
            print("Accepted by NFA!")
        else:
            print("Not Accepted by NFA!")

        if(dfa_run(In)):
            print("Accepted by DFA!")
        else:
            print("Not Accepted by DFA!")

        number = number - 1


State_construction()
Transition_construction()
Generate_output()
print("\nRAW Table:")
Print_Table()

file = open("output.json", 'w')
json.dump(out, file, indent=2)
file.close()

State_reduction()
print("\nFinal Table:")
Print_Table()
# testNFA_DFA()
