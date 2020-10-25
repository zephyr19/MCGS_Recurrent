import networkx as nx
import random
from itertools import *


class RDN():
    def __init__(self, param_settings=None):
        pass

    def run_samping(self, G, rate):
        size = round(len(G) * rate)
        Gs = nx.Graph()
        d = nx.degree(G)
        deg = {}
        for i in d:
            deg[i[0]] = i[1]

        maxpr = max(deg.items(), key=lambda x: x[1])[1]
        minpr = min(deg.items(), key=lambda x: x[1])[1]

        for u, v in deg.items():
            # MaxMinNormalization
            a = (v-minpr)/(maxpr-minpr)
            deg[u] = a
        node = list(G.nodes())
        cycle_n = cycle(node)
        Gs_check = set()
        while len(Gs) < size:
            p = random.random()
            n = next(cycle_n)
            if p < deg[n] and n not in Gs_check:
                Gs.add_node(n)
                Gs_check.add(n)

        Gs_induce = G.subgraph(Gs.nodes())
        return (Gs_induce)