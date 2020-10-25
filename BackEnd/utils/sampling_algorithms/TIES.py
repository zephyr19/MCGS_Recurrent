import random
import networkx as nx

class TIES():
    def __init__(self, param_settings=None):
        pass

    def run_samping(self, G, rate):
        size = round(len(G) * rate)
        edges_list = list(G.edges())
        Vs_list = set()
        while (len(Vs_list)) < size:
            edges_sample = random.choice(edges_list)
            Vs_list.add(edges_sample[0])
            Vs_list.add(edges_sample[1])
        Gs = G.subgraph(Vs_list)
        return Gs

import csv
import re
from utils.json_generator import JSON_Generator

def loadGraph():
    with open('cpan_node.csv', 'r', encoding='utf-8')as fp:
        reader = csv.reader(fp)
        source_nodes = list(int(_[0]) for _ in reader)
    with open('cpan_edge.csv', 'r', encoding='utf-8')as fp:
        reader = csv.reader(fp)
        source_edges = list((int(_[0]), int(_[1])) for _ in reader if _[0] != _[1])
    G = nx.Graph()
    G.add_nodes_from(source_nodes)
    G.add_edges_from(source_edges)
    return G




if __name__ == '__main__':
    G = loadGraph()
    my_algorithm = TIES()
    Gs = my_algorithm.run_samping(G, 0.3)
    Gs_nodes = set(list(_ for _ in Gs.nodes()))
    Gs_edges = set(list(_ for _ in Gs.edges()))
    # 重写采样svg
    # 获取svg头信息
    with open('origin_cpan.svg', 'r', encoding='utf-8')as fp:
        svg_text = fp.readline()
        svg_header = ''
        while ('version="1.1"' not in svg_text):
            svg_header += svg_text
            svg_text = fp.readline()
        svg_header += svg_text
    # 获取采样svg_edge和svg_node
    with open('origin_cpan.svg', 'r', encoding='utf-8')as fp:
        svg_text = fp.read()
        edges = re.findall('<path .*\n.*\n.*/>', svg_text)
        nodes = re.findall('<circle .*\n.*\n.*/>', svg_text)
        edges_list = re.findall('class="id_([0-9]*) id_([0-9]*)"', svg_text)
        nodes_list = re.findall('class="id_([0-9]*)"', svg_text)
        edge_svg_text = []
        for edge, source_edge in zip(edges_list, edges):
            if (int(edge[0]), int(edge[1])) in Gs_edges or (int(edge[1]), int(edge[0])) in Gs_edges:
                edge_svg_text.append(source_edge)
        node_svg_text = []
        for node, source_node in zip(nodes_list, nodes):
            if int(node) in Gs_nodes:
                node_svg_text.append(source_node)
    g_edges = '<g id="edges">\n' + "\n".join(edge_svg_text) + '</g>'
    g_nodes = '<g id="nodess">\n' + "\n".join(node_svg_text) + '</g>'
    sampling_svg_content = svg_header + g_edges + g_nodes + '</svg>'
    with open('../../frontend/public/static/graph_set/svg/Cpan/ties_0.3.svg', 'w', encoding='utf-8')as fp:
        fp.write(sampling_svg_content)
    generator = JSON_Generator()
    source_svg_path = '../../frontend/public/static/graph_set/svg/Cpan/ties_0.3.svg'
    target_json_path = '../../frontend/public/static/graph_set/json/Cpan/TIES_0.3.json'
    generator.convertion(source_svg_path, target_json_path)