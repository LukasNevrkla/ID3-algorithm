###############################š##
# Author:           Lukáš Nevrkla
# Auto-testSets:    @Matej
##################################

import json
import sys
import os
import math
import logging


CGREEN  = '\33[32m'
CRED = '\033[91m'
CEND = '\033[0m'

log = logging.getLogger("logger")
log.disabled = True
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

class Node:
    def __init__(self, val, str = "", leaf = False):
        self.val = val
        self.leaf = leaf
        self.str = str
        self.nexts = []

def get_final_class(tree,data):

    while (not tree.leaf):
        for attribute in data:
            for n in tree.nexts:
                if (n[0] == attribute):
                    tree = n[1]
    return tree.val

def compare_test_examples(final_val, exp_val):
    fin_val = "{'" + final_val + "'}"
    if fin_val == str(exp_val):
        return (CGREEN + "OK" + CEND)
    else:
        return (CRED + "FAIL" + CEND)


def ResultClasses(examples):
    classes = [e[1] for e in examples]
    return set(classes)

def ExamplesWithVal(examples, val, prop, allProps):
    propIndex = list(allProps.keys()).index(prop)
    #log.info("{0} {1} {2} {3}".format(val, prop, allProps, str(propIndex)))
    log.info([e[propIndex + 2] for e in examples])
    return [e for e in examples if e[propIndex + 2] == val]

def Entropy(examples, classes):
    if len(examples) == 0:
        return 0.0

    res = 0
    for c in classes:
        currClasses = len([e for e in examples if e[1] == c])
        p = currClasses / len(examples)
        log.info("ent-p {0}".format(str(p)))
        if p != 0:
            res -= p * math.log(p, 2)

    return res

def InformationGain(examples, prop, allProps, classes):
    total = Entropy(examples, classes)
    log.info("total = {0}".format(str(total)))
    partial = 0

    for v in prop[1]:
        subExamples = ExamplesWithVal(examples, v, prop[0], allProps)
        k = len(subExamples) / len(examples)
        e = k * Entropy(subExamples, classes)
        partial += e
        log.info("partial {0} = {1}".format(v, str(e)))
        #log.info("{0} / {1}".format(subExamples, examples))

    return total - partial

def InduceTree(examples, props, allProps, classes):
    newProps = props.copy()
    res = [newProps.popitem(), newProps, ""]
    return res

def ID3Tree(examples, props, allProps, classes):
    newProps = props.copy()

    maxIG = -1
    bestProp = None
    txt = ""
    for k, v in newProps.items():
        ig = InformationGain(examples, (k,v), allProps, classes)
        log.info("IG {0} = {1}\n---".format(k, str(ig)))
        if (ig > maxIG):
            bestProp = k
            maxIG = ig 
        txt += "{0} = {1}\n".format(k.ljust(10), "{:.3f}".format(ig))

    bestProp = (bestProp, newProps.pop(bestProp))
    #print(bestProp, newProps)
    return [bestProp, newProps, txt]

def DecisionTree(examples, props, origProps, classes, alg):
    # print("-" * 10)
    # print("Examples: ", examples)
    # print("Props: ", list(props.keys()))
    # print("-" * 10)

    c = ResultClasses(examples)
    if len(c) < 2:
        return Node(c, leaf=True)
    if (len(props) == 0):
        return Node(c, leaf=True)

    prop, newProps, nodeStr = alg(examples, props, origProps, classes)
    root = Node(prop[0], str=nodeStr)

    for value in prop[1]:
        edge = value
        subExamples = ExamplesWithVal(examples, value, prop[0], origProps)
        subExamplesIndexes = [e[0] for e in subExamples]
        node = DecisionTree(subExamples, newProps, origProps, classes, alg)
        root.nexts.append([edge, node, subExamplesIndexes])

    log.info("root = {0}\n---------------".format(root.val))
    return root

def PrintTree(root, indent = "|"):
    if root == None:
        return 

    newIndent = indent + "    |"
    txt = root.str
    tl = txt.split("\n")
    tl = [newIndent + i + "|" for i in tl]
    txt = "\n" + "\n".join(tl[0:-1])

    if not root.leaf:
        print("{0} [{1}] {2}".format(indent, root.val, txt))
    else:
        print(indent, root.val)

    if not root.leaf:
        for n in root.nexts:
            print("{0} => {1} {2}".format(indent, n[0], n[2]))
            PrintTree(n[1], newIndent)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            data = json.load(f)
    else:
        print("No input")
        sys.exit(1)

    examples = data["objects"]
    props = data["attributes"]
    classes = data["classes"]

    #print("Induce-tree")
    #root = DecisionTree(examples, props, props, classes, InduceTree)
    #PrintTree(root)

    runBatches = [
        {
            "trainSet" : [3, 12],
            "testSet"  : [0, 3]
        },
        {
            "trainSet" : [0, 9],
            "testSet"  : [9, 12]
        }
    ]

    for b in runBatches:
        print("Train set = examples [{0}, {1}]".format(b["trainSet"][0], b["trainSet"][1]))
        print("-" * 25)

        root = DecisionTree(
            examples[b["trainSet"][0] : b["trainSet"][1]], 
            props, props, classes, ID3Tree)
        PrintTree(root)
        print("-" * 25)

        print("Test set = examples [{0}, {1}]".format(b["testSet"][0], b["testSet"][1]))
        for t in range(b["testSet"][0], b["testSet"][1]):
            res = compare_test_examples(examples[t][1], get_final_class(root, examples[t]))
            print(str(t) + ":", examples[t], " => ", get_final_class(root, examples[t]), res)
            print()
