# in this experiment, we consider 3 relations: AAFA, APAPA and APVPA.
# I_n = {1, 2, 3}; I is subset of I_n
# With |I| = 1: I = {1}, {2} or {3}
# With |I| = 2: I = {1, 2} ; {2, 3} or {1, 3}
# |I| = 3: I={1, 2, 3}
# In here, we calculate a(A) with different strong levels
import networkx as nx
from random import randint
import random
import numpy as np
from itertools import combinations
import math
from scipy.stats import entropy
from numpy.linalg import norm
from math import sqrt, log
import json, os
import itertools


import MySQLdb


# Connect
db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="****",
                     db="dblpdatabase")
cursor = db.cursor()

E = []

def read_all_nodes_in_network():
    # get all authors in full dataset: 13605 authors(7993 papers)
    cursor.execute("SELECT distinct(author_id) FROM paper_authors")
    for x in range(0, cursor.rowcount):
        row = cursor.fetchone()
        E.append(str(row[0]))

read_all_nodes_in_network()


def read_network_APA(period):
    cwd = os.getcwd()
    filename = cwd + "/Net_APA_" + str(period)
    net = nx.read_gexf(filename)
    return net


def read_network_AAFA(period):
    cwd = os.getcwd()
    filename = cwd + "/Net_AAFA_" + str(period)
    net = nx.read_gexf(filename)
    return net


def read_network_APVPA(period):
    cwd = os.getcwd()
    with open("Net_APVPA_[1995, 2010]", "r")as f:
        lines = f.readlines()

    G = nx.Graph()
    for index, line in enumerate(lines):
        data = line.strip()
        if "<edge id" in data:
            # print(data)
            source = data.split(" ")[2].split("=")[1]
            source_id = source[1:len(source) - 1]

            target = data.split(" ")[3].split("=")[1]
            target_id = target[1:len(target) - 2]
            # print(source_id, target_id)

            indexoflinecontainnbconf = index + 2
            line_nbconfsvalue = lines[indexoflinecontainnbconf].strip()
            # print(line_nbconfsvalue)
            nbconfsvalue = int(line_nbconfsvalue[25])
            # print(nbconfsvalue)

            G.add_edge(source_id, target_id, nbconfs=nbconfsvalue)

    return G


pastperiod = [1995, 2010]
G1_APA = read_network_APA(pastperiod)
G1_AAFA = read_network_AAFA(pastperiod)
G1_APVPA = read_network_APVPA(pastperiod)


def aA(A, k):
    # Calculate a(A) with strong level k
    aA = []
    I_n = range(1, 4)  # relation index i i=1(AAFA), i=2(APAPA), i=3(APVPA)
    # I_List = map(list, combinations(I_n, k))
    I_List = list(set(itertools.combinations(I_n, k)))

    for node_x in set(E).difference(A):
        for I in I_List:
            # If exist a subset I from I_n, |I|=k
            # Voi every relation index i in I, Vi(x) intersect A # empty
            Accept = True
            for i in I:
                Vi_x = []
                try:
                    if i == 1:
                        Vi_x = G1_AAFA.neighbors(node_x)
                    if i == 2:
                        H = G1_APA.neighbors(node_x)
                        for node in H:
                            Vi_x.append(node)
                        for node in H:
                            neis_node = G1_APA.neighbors(node)
                            for nei_node in neis_node:
                                if nei_node not in Vi_x:
                                    Vi_x.append(nei_node)

                    if i == 3:
                        Vi_x = G1_APVPA.neighbors(node_x)
                except:
                    pass
                if len(list(set(Vi_x) & set(A))) == 0:
                    Accept = False

            if Accept:
                # print("Accept")
                aA.append(node_x)
                break

        # print("----------------------------------------------------------------")

    aA = list(set(aA) | set(A))

    return aA


def pseudo_distance(A, B, k):
    X = A
    Y = B
    k1 = k2 = 0
    stop1 = stop2 = 0
    while True:
        aA_k1 = aA(X, k)
        k1 += 1
        stop1 += 1
        set1 = set(aA_k1)
        set2 = set(B)
        if set2.issubset(set1) or stop1 == 50:
            break
        else:
            X = aA_k1

    while True:
        aA_k2 = aA(Y, k)
        k2 += 1
        stop2 += 1
        set1 = set(aA_k2)
        set2 = set(A)
        if set2.issubset(set1) or stop2 == 50:
            break
        else:
            Y = aA_k2

    if stop1 == stop2 == 50:
        return -1

    pseudodistance = min(k1, k2)

    return pseudodistance

