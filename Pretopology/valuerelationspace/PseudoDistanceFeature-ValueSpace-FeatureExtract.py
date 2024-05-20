# in this experiment, we consider pretopology in value space
# In here, we calculate a(A)
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
import pymysql


# Connect
db = pymysql.connect(host="localhost",
                     user="root",
                     passwd="***",
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


def read_network_APAPA(period):
    cwd = os.getcwd()
    filename = cwd + "/Net_APAPA_" + str(period)
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
            #print(source_id, target_id)

            indexoflinecontainnbconf = index + 2
            line_nbconfsvalue = lines[indexoflinecontainnbconf].strip()
            # print(line_nbconfsvalue)
            nbconfsvalue = int(line_nbconfsvalue[25])
            #print(nbconfsvalue)

            G.add_edge(source_id, target_id, nbconfs=nbconfsvalue)

    return G


pastperiod = [1995, 2010]
G1_APA = read_network_APA(pastperiod)
G1_AAFA = read_network_AAFA(pastperiod)
G1_APVPA = read_network_APVPA(pastperiod)
G1_APAPA = read_network_APAPA(pastperiod)

'''
def generate_net_APAPA_with_weights(period):
    G = nx.Graph()
    for x in E:
        for y in E:
            if x!=y:
                try:
                    N_x = G1_APA.neighbors(x)
                    N_y = G1_APA.neighbors(y)
                    nb = len(list(set(N_x) & set(N_y)))
                    if nb>0:
                        G.add_edge(x, y, nb_common_authors=nb)
                except:
                    pass
    nx.write_gexf(G, "Net_APAPA_" + str(period))
    return G

G1_APAPA = generate_net_APAPA_with_weights(pastperiod)
'''

'''
def aA(A, s):
    # Calculate a(A) with threshold value s
    # a(A) = { y in X| sum(v(x,y)>s)} union A
    aA = []

    for node_y in set(E).difference(A):
        sum = 0
        for node_x in A:
            # consider relation APVPA
            if G1_APVPA.has_edge(node_y, node_x):
                w = G1_APVPA[node_y][node_x]["nbconfs"]
                sum = sum + w

        if (sum >= s):
            aA.append(node_y)

    aA = list(set(aA) | set(A))

    return aA
'''

def aA(A, s1, s2):
    # Calculate a(A) with threshold value s
    #a(A) = { y in X| sum(v(x,y)>s)} union A
    aA = []

    for node_y in set(E).difference(A):
        sum1 = 0
        sum2 = 0
        sum3 = 0
        for node_x in A:

            #consider relation AAFA
            if G1_AAFA.has_edge(node_y, node_x):
                w = 1
                sum1 = sum1 + w


            #consider relation APVPA
            if G1_APVPA.has_edge(node_y, node_x):
                w = G1_APVPA[node_y][node_x]["nbconfs"]
                sum2 = sum2 + w
            '''
            # consider relation APAPA
            if G1_APAPA.has_edge(node_y, node_x):
                w = G1_APAPA[node_y][node_x]["nb_common_authors"]
                sum3 = sum3 + w
            '''

        if (sum1>=s1) or (sum2>=s2):
            aA.append(node_y)

    aA = list(set(aA) | set(A))

    return aA


#A = ['81452603769']
#pretopo = aA(A, s = 2)
#print(pretopo)


def pseudo_distance(A, B, th1, th2):
    X = A
    Y = B
    k1 = k2 = 0
    stop1 = stop2 = 0
    while True:
        aA_k1 = aA(X, th1, th2)
        k1 += 1
        stop1 += 1
        set1 = set(aA_k1)
        set2 = set(B)
        if set2.issubset(set1) or stop1 == 20:
            break
        else:
            X = aA_k1

    while True:
        aA_k2 = aA(Y, th1, th2)
        k2 += 1
        stop2 += 1
        set1 = set(aA_k2)
        set2 = set(A)
        if set2.issubset(set1) or stop2 == 20:
            break
        else:
            Y = aA_k2

    if stop1 == stop2 == 20:
        return -1

    pseudodistance = min(k1, k2)

    return pseudodistance
