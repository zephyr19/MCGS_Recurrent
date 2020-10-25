import csv, os
from django.conf import settings
import networkx as nx
from utils.sampling_algorithms.BF import BF
from utils.sampling_algorithms.FF import FF
from utils.sampling_algorithms.MCGS import MCGS
from utils.sampling_algorithms.RAS import RAS
from utils.sampling_algorithms.RDN import RDN
from utils.sampling_algorithms.RMSC import RMSC
from utils.sampling_algorithms.TIES import TIES


class Run_Sampling_Model():
    def __init__(self, graph_name, algorithm_name, param_settings):
        self.G = self.load_graph(graph_name)
        self.Algorithm_Model = self.load_algorithm(algorithm_name, param_settings)
        self.rate = param_settings['rate']

    def load_graph(self, file_name):
        with open(os.path.join(settings.BASE_DIR,
                               'utils/dataset/csv_files/{}_node.csv'.format(
                                       file_name)),
                  'r')as fp:
            reader = csv.reader(fp)
            nodes = list(int(_[0]) for _ in reader)
        with open(os.path.join(settings.BASE_DIR,
                               'utils/dataset/csv_files/{}_edge.csv'.format(
                                       file_name)),
                  'r')as fp:
            reader = csv.reader(fp)
            edges = list([int(_[0]), int(_[1])] for _ in reader if _[0] != _[1])
        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        return G

    def load_algorithm(self, algorithm_name, param_settings):
        if algorithm_name == 'BF':
            return BF(param_settings)
        if algorithm_name == 'FF':
            return FF(param_settings)
        if algorithm_name == 'MCGS':
            return MCGS(param_settings)
        if algorithm_name == 'RAS':
            return RAS(param_settings)
        if algorithm_name == 'RDN':
            return RDN(param_settings)
        if algorithm_name == 'RMSC':
            return RMSC(param_settings)
        if algorithm_name == 'TIES':
            return TIES(param_settings)

    def run(self):
        Gs = self.Algorithm_Model.run_samping(self.G, self.rate)
        return Gs
