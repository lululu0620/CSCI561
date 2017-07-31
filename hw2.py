# Name: Lu Xie
# USC ID: 2327394360
# CS 561 HW2
# Summer 2017

import time
import sys

class Node:

    visited = {}
    successors = []
    chosen = ()
    SP1 = 0
    SP2 = 0

    def __init__(self, name, color, depth, v, alpha, beta):
        self.name = name
        self.color = color
        self.depth = depth
        self.v = v
        self.alpha = alpha
        self.beta = beta

    def displayState(self):
        return self.name+", "+self.color+", "+str(self.depth)+", "+str(self.v)+", "+str(self.alpha)+", "+str(self.beta)+"\n"


def Successors(graph, domain, nodeColor):
    ChosenDomain = {}
    for node in nodeColor:
        for neighbor in graph[node]:
            if neighbor not in nodeColor:
                if neighbor not in ChosenDomain: ChosenDomain[neighbor] = list(domain)
                if nodeColor[node] in ChosenDomain[neighbor]: ChosenDomain[neighbor].remove(nodeColor[node])
    successors = set()
    for node in ChosenDomain:
        for color in ChosenDomain[node]:
            successors.add((node, color))
    return sorted(list(successors))


def AlphaBetaSearch(state, depth):
    state.v = MaxValue(state, depth)
    return state

def MaxValue(state, depth):
    if state.depth == depth or state.successors == []:
        state.v = state.SP1 - state.SP2
        fo.write(state.displayState())
        return state.v
    for s in state.successors:
        fo.write(state.displayState())
        node = Node(s[0], s[1], state.depth + 1, float("inf"), state.alpha, state.beta)
        node.visited = state.visited.copy()
        node.visited[s[0]] = s[1]
        node.successors = Successors(graph, domain, node.visited)
        node.SP1 = state.SP1 + WP1[s[1]]
        node.SP2 = state.SP2
        minValue = MinValue(node, depth)
        if minValue > state.v:
            state.v = minValue
            state.chosen = (node.name, node.color)
        if state.v >= state.beta:
            fo.write(state.displayState())
            return state.v
        state.alpha = max(state.alpha, state.v)
    fo.write(state.displayState())
    return state.v

def MinValue(state, depth):
    if state.depth == depth or state.successors == []:
        state.v = state.SP1 - state.SP2
        fo.write(state.displayState())
        return state.v
    for s in state.successors:
        fo.write(state.displayState())
        node = Node(s[0], s[1], state.depth+1, float("-inf"), state.alpha, state.beta)
        node.visited = state.visited.copy()
        node.visited[s[0]] = s[1]
        node.successors = Successors(graph, domain, node.visited)
        node.SP1 = state.SP1
        node.SP2 = state.SP2 + WP2[s[1]]
        maxValue = MaxValue(node, depth)
        if  maxValue < state.v:
            state.v = maxValue
            state.chosen = (node.name, node.color)
        if state.v <= state.alpha:
            fo.write(state.displayState())
            return state.v
        state.beta = min(state.beta, state.v)
    fo.write(state.displayState())
    return state.v

start = time.clock()
lines = []
with open("t5.txt") as f:
    lines.extend(f.read().splitlines())
domain = lines[0].replace(" ","").split(",")
MaxDepth = int(lines[2])

WP1 = {}
WP2 = {}
for line in lines[3].replace(" ","").split(","):
    term = line.split(":")
    WP1[term[0]] = int(term[1])
for line in lines[4].replace(" ","").split(","):
    term = line.split(":")
    WP2[term[0]] = int(term[1])

graph = {}
for line in xrange(5, len(lines)):
    splits = lines[line].replace(" ","").split(":")
    graph[splits[0]] = splits[1].split(",")

SP1 = 0
SP2 = 0
explored = []
nodeColor = {}
for line in lines[1].replace(" ","").split(","):
    splits = line.split(",")
    term = splits[0].split(":")
    color = term[1].split("-")
    explored.append(term[0])
    nodeColor[term[0]] = color[0]
    if color[1] == "1":
        SP1 += WP1[color[0]]
    else: SP2 += WP2[color[0]]

initial = Node(explored[-1], nodeColor[explored[-1]], 0, float("-inf"), float("-inf"), float("inf"))
initial.visited = nodeColor.copy()
initial.successors = Successors(graph, domain, initial.visited)
initial.SP1 = SP1
initial.SP2 = SP2

fo= open('output.txt', 'w')
action = AlphaBetaSearch(initial, MaxDepth)
fo.write(action.chosen[0]+", "+action.chosen[1]+", "+str(action.v))
end = time.clock()
print "read: %f s" % (end - start)