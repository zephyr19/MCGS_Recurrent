import csv
import math
import os

import numpy as np
import networkx as nx

from django.conf import settings


def flat(multi_list):
    result = []
    for item in multi_list:
        if isinstance(item, list):
            result.extend(flat(item))
        else:
            result.append(item)
    return result


class Classic_Model():
    def __init__(self, G):
        self.__init_settings(G)
        self.__run_detection()
        self.__flat_sort_minority()

    def __init_settings(self, G):
        self.G = G
        self.__G_node_degree_dict = {item[0]: item[1] for item in self.G.degree()}
        self.__G_neighbors_dict = {_: set(self.G.neighbors(_)) for _ in
                                   self.G.nodes()}
        self.__G_minority_structures_set = set()
        self.anomaly_total = {'Super Pivot': [], 'Huge Star': [], 'Rim': [],
                              'Tie': []}

    def __flat_sort_minority(self):
        for key, value in self.anomaly_total.items():
            if key =='Rim':
                flat_set = sorted(set(flat(value)),
                                  key=lambda x: self.__G_node_degree_dict[x],
                                  reverse=True)
                self.anomaly_total[key] = list(flat_set)
            if key == 'Tie':
                tie_list = []
                for item in value:
                    sorted_list = set(sorted(set(item),
                           key=lambda x: self.__G_node_degree_dict[x],
                           reverse=True))
                    for _ in sorted_list:
                        tie_list.append(_)
                self.anomaly_total[key] = tie_list

    def __run_detection(self):
        self.__detect_Star_Pivot()
        # self.__detect_Tie_Rim()
        self.__new_detect_Tie_Rim()

    def __detect_Star_Pivot(self):
        G = self.G
        original_nodes = set(G.nodes())
        sorted_node_by_degree = sorted(original_nodes,
                                       key=lambda x: self.__G_node_degree_dict[x],
                                       reverse=True)
        nodes_5 = list(sorted_node_by_degree)[:math.ceil(len(original_nodes) * 0.05)]
        for node in nodes_5:
            neis = self.__G_neighbors_dict[node]
            connect = False
            for nei in neis:
                if len(self.__G_neighbors_dict[nei] & neis):
                    connect = True
                    break
            if connect:
                self.anomaly_total['Super Pivot'].append(node)

        degree_average = np.average(list(self.__G_node_degree_dict.values()))
        nodes_average = set(
            filter(lambda item: self.__G_node_degree_dict[item] >= degree_average,
                   original_nodes))
        for node in nodes_average:
            neis = self.__G_neighbors_dict[node]
            connect = False
            for nei in neis:
                if len(self.__G_neighbors_dict[nei] & neis):
                    connect = True
                    break
            if not connect:
                self.anomaly_total['Huge Star'].append(node)

    def __bridge_merge(self, inner, s=0):
        if s == 0:
            inner_tuple = []
            merge = []
            copyinner = inner.copy()
            for i in range(len(inner) - 1):
                for j in range(i + 1, len(inner)):
                    if inner[i][0] in copyinner[j] or inner[i][1] in copyinner[j]:
                        tmp = tuple(set(inner[i] + copyinner[j]))
                        copyinner[j] = tmp
                        merge.append(inner[i])
                        merge.append(inner[j])
                        inner_tuple.append(tmp)
            inner = set(copyinner) - set(merge)
            sort_inner = sorted(inner, key=lambda d: len(d), reverse=True)
            return (sort_inner)

        if s == 1:
            inner_tuple = []
            merge = []
            copyinner = inner.copy()
            count_node = {}
            for i in inner:
                if i[0] in count_node:
                    count_node[i[0]] += 1
                else:
                    count_node[i[0]] = 1
                if i[1] in count_node:
                    count_node[i[1]] += 1
                else:
                    count_node[i[1]] = 1
            for i in range(len(inner) - 1):
                for j in range(i + 1, len(inner)):
                    if (inner[i][0] in copyinner[j] and count_node[
                        inner[i][0]] < 3) or (
                            inner[i][1] in copyinner[j] and count_node[
                        inner[i][0]] < 3):
                        tmp = tuple(set(inner[i] + copyinner[j]))
                        copyinner[j] = tmp
                        merge.append(inner[i])
                        merge.append(inner[j])
                        inner_tuple.append(tmp)
            inner = set(copyinner) - set(merge)

            # keep some structures
            # rule-1: sort by length
            sort_inner = sorted(inner, key=lambda d: len(d), reverse=True)
            # rule-2: sort by repeat
            two_tuple = list(filter(lambda d: len(d) <= 2, inner))
            parachute = set()
            for i in two_tuple:
                if count_node[i[0]] > 2:
                    parachute.add(i[0])
                if count_node[i[1]] > 2:
                    parachute.add(i[1])
            balloon = list(
                filter(lambda d: d[0] not in parachute and d[1] not in parachute,
                       two_tuple))
            # merge
            rm = list(filter(lambda d: d not in two_tuple, sort_inner))
            final_outer = rm + list(parachute) + balloon
            return (final_outer)

    def __detect_Tie_Rim(self):
        G, anomaly_total = self.G, self.anomaly_total

        # get bridges and articulation points
        l = list(nx.articulation_points(G))
        b = list(nx.bridges(G))

        # get both and remainder
        both = list(filter(lambda d: d[0] in l and d[-1] in l, b))
        remainder = [i for i in b if i not in both]

        # filter-find chain
        s = set()
        for r in remainder:
            if G.degree(r[0]) == 1 and G.degree(r[1]) == 2:
                s.add(r[1])
            if G.degree(r[1]) == 1 and G.degree(r[0]) == 2:
                s.add(r[0])

        # get inner and outer edge-pair
        inner = list(filter(lambda d: d[0] not in s and d[1] not in s, both))
        outer = [i for i in b if i not in inner]

        # marge
        sort_inner = self.__bridge_merge(inner)
        sort_outer = self.__bridge_merge(outer, s=1)

        for i in sort_inner:
            if type(i) == int:
                continue
            for j in i:
                if j in l:
                    self.anomaly_total['Tie'].append(j)
        for i in sort_outer:
            if type(i) == int:
                if i in l and i not in self.anomaly_total['Rim']:
                    self.anomaly_total['Rim'].append(i)
            else:
                for j in i:
                    if j in l and i not in self.anomaly_total['Rim']:
                        self.anomaly_total['Rim'].append(j)

    def __new_detect_Tie_Rim(self):
        G = self.G
        # one-degree node set in the original graph
        one_degree_node_set = set(
            filter(lambda item: self.__G_node_degree_dict[item] == 1,
                   self.__G_node_degree_dict.keys()))

        # cut point set in original graph
        cut_points = set(nx.articulation_points(G))
        # induced subgraph from the original graph based on cut points
        cut_points_graph = G.subgraph(cut_points)

        # dictionary recording the degree of each cut point in the induced subgraph
        cut_point_degree_dict = {_[0]: _[1] for _ in cut_points_graph.degree()}
        # dictionary recording the neighbor nodes of each cut points in the induced subgraph
        cut_point_neighbors_records = {_: list(cut_points_graph.neighbors(_)) for _
                                       in cut_points}
        # dictionary recording the neighbors of each cut point in the original graph
        cut_point_neighbors_records_in_G = {_: set(G.neighbors(_)) for _ in
                                            cut_points}

        chains_list = []
        parachute_set = set()

        # start from cut points with degrees lower than 1 as end points of chain structures,
        # and traverse all cut points
        iter_nodes = list(
            filter(lambda item: cut_point_degree_dict[item] <= 1, cut_points))
        seen = set()
        while len(cut_points - seen) > 0:
            for node in iter_nodes:
                if node not in seen:
                    seen.add(node)
                    temp_chain = [node]
                    current_node = node

                    while 1:
                        # detect parachute structure nodes
                        if cut_point_neighbors_records_in_G[current_node]-set(cut_point_neighbors_records[current_node]):
                            parachute_set.add(current_node)
                        neighbors = cut_point_neighbors_records[current_node]

                        # the loop exits when the current cut point does not have cut point neighbors,
                        # or else, move to next node and continue traversal
                        if not neighbors or len(set(neighbors) - seen) >= 2:
                            break
                        else:
                            other = neighbors[0]
                            for _ in neighbors:
                                if _ not in seen:
                                    other = _
                                    break
                            if other not in seen:
                                seen.add(other)
                                temp_chain.append(other)
                                current_node = other
                            else:
                                break

                    if len(temp_chain) > 1: chains_list.append(temp_chain)

            remaining_cut_points = cut_points - seen
            cut_point_degree_dict = {_[0]: _[1] for _ in
                                     G.subgraph(remaining_cut_points).degree()}
            iter_nodes = set(
                filter(lambda item: cut_point_degree_dict[item] <= 1,
                       remaining_cut_points))
            if not iter_nodes:
                for cut_point in remaining_cut_points:
                    if cut_point_neighbors_records_in_G[cut_point]-set(cut_point_neighbors_records[cut_point]):
                        parachute_set.add(cut_point)
                break

        # sort the chains according to their length
        chains_list.sort(key=lambda chain: len(chain), reverse=True)

        for chain_item in chains_list:
            # get the set of one-degree neighbor nodes of the end nodes of each chain
            a_one_nodes = cut_point_neighbors_records_in_G[
                              chain_item[0]] & one_degree_node_set
            b_one_nodes = cut_point_neighbors_records_in_G[
                              chain_item[-1]] & one_degree_node_set

            # if any end node of the chain has one and only one neighbor with degree 1 in G,
            # then the chain is a rim, else a tie.
            if len(a_one_nodes) == 1 or len(b_one_nodes) == 1:
                self.anomaly_total['Rim'].append(chain_item)
            else:
                self.anomaly_total['Tie'].append(chain_item)

        # sort the parachute-shaped rims according to degrees and add them to rim records
        parachute_sorted = sorted(parachute_set,
                                  key=lambda item: self.__G_node_degree_dict[item],
                                  reverse=True)

        self.anomaly_total['Rim'].extend(list(parachute_sorted))
