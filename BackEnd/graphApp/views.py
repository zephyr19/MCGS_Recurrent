from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.conf import settings
import re, json, os, csv
import networkx as nx
from utils.sampling_program import Run_Sampling_Model
from utils.json_generator import JSON_Generator
from utils.minority_structure_detection import Classic_Model
import community as community_louvain

# Create your views here.
def getGraphInfo(request):
    parameters = json.loads(request.body)
    graph_name = parameters['graphName']
    G = loadGraph(graph_name)
    classic_model = Classic_Model(G)
    anomaly_total = classic_model.anomaly_total
    graph_record = {
        'node_num': len(G.nodes()),
        'edge_num': len(G.edges()),
        'minority': anomaly_total
    }
    return HttpResponse(
        json.dumps({'state': "success", 'graph_record': graph_record}),
        content_type='application/json')


def runSampling(request):
    parameters = json.loads(request.body)
    graph_name = parameters['graphName']
    algorithm_name = parameters['algorithm']
    float_param_settings = {
        'rate': float(parameters['params']['rate']),
        'alpha': float(parameters['params']['alpha']),
        'beta': float(parameters['params']['beta']),
        'loss weight': list(float(_) for _ in re.findall('([0-9]*\.{0,1}[0-9]*)',
                                                         parameters[
                                                             'params'][
                                                             'loss weight'])[::2])
    }

    print(parameters)

    run_model = Run_Sampling_Model(graph_name, algorithm_name, float_param_settings)
    Gs = run_model.run()
    Gs_nodes = set(list(_ for _ in Gs.nodes()))
    Gs_edges = set(list(_ for _ in Gs.edges()))

    classic_model = Classic_Model(Gs)
    anomaly_total = classic_model.anomaly_total

    graph_record = {
        'node_num': len(Gs.nodes()),
        'edge_num': len(Gs.edges()),
        'minority': anomaly_total,
    }

    partition = community_louvain.best_partition(Gs)
    # print(partition)
    formatNodes = [{
        "id": str(item[0]),
        "group": str(item[1]),
    } for item in partition.items()]

    formatEdges = [{
        "source": str(edge[0]),
        "target": str(edge[1]),
    } for edge in Gs_edges]

    graph_data = {
        'nodes': formatNodes,
        'edges': formatEdges
    }

    return HttpResponse(
        json.dumps({'state': "success", 'graph_record': graph_record, 'graph_data': graph_data}),
        content_type='application/json')



def not_used():
    # # # 重写采样svg文件
    # # 获取svg头信息
    with open(
            os.path.join(settings.BASE_DIR,
                         'utils/dataset/svg_files/origin_{}.svg'.format(graph_name)),
            'r', encoding='utf-8')as fp:
        svg_text = fp.readline()
        svg_header = ''
        while ('version="1.1"' not in svg_text):
            svg_header += svg_text
            svg_text = fp.readline()
        svg_header += svg_text
    # 获取采样svg_edge和svg_node
    with open(
            os.path.join(settings.BASE_DIR,
                         'utils/dataset/svg_files/origin_{}.svg'.format(graph_name)),
            'r', encoding='utf-8')as fp:
        svg_text = fp.read()
        edges = re.findall('<path .*\n.*\n.*/>', svg_text)
        nodes = re.findall('<circle .*\n.*\n.*/>', svg_text)
        edges_list = re.findall('class="id_([0-9]*) id_([0-9]*)"', svg_text)
        nodes_list = re.findall('class="id_([0-9]*)"', svg_text)
        edge_svg_text = []
        for edge, source_edge in zip(edges_list, edges):
            if (int(edge[0]), int(edge[1])) in Gs_edges or (
                    int(edge[1]), int(edge[0])) in Gs_edges:
                edge_svg_text.append(source_edge)
        node_svg_text = []
        for node, source_node in zip(nodes_list, nodes):
            if int(node) in Gs_nodes:
                node_svg_text.append(source_node)
    g_edges = '<g id="edges">\n' + "\n".join(edge_svg_text) + '</g>'
    g_nodes = '<g id="nodess">\n' + "\n".join(node_svg_text) + '</g>'
    sampling_svg_content = svg_header + g_edges + g_nodes + '</svg>'

    # 保存svg开发环境下
    # with open(os.path.join(settings.BASE_DIR,
    #                        'frontend_dist/static/sampling_result.svg'), 'w',
    #           encoding='utf-8')as fp:
    #     fp.write(sampling_svg_content)

    # 将svg文件转化为json文件(辅助鱼眼特效)
    generator = JSON_Generator()
    source_svg_path = os.path.join(settings.BASE_DIR,
                                   'frontend_dist/static/sampling_result.svg')
    target_json_path = os.path.join(settings.BASE_DIR,
                                    'frontend_dist/static/sampling_result.json')
    graph_data = generator.convertion(source_svg_path, target_json_path)

    classic_model = Classic_Model(Gs)
    anomaly_total = classic_model.anomaly_total

    graph_record = {
        'node_num': len(Gs.nodes()),
        'edge_num': len(Gs.edges()),
        'minority': anomaly_total,
    }

    return HttpResponse(
        json.dumps({'state': "success", 'graph_record': graph_record, 'graph_data': graph_data}),
        content_type='application/json')


def loadGraph(graph_name):
    with open(os.path.join(settings.BASE_DIR,
                           'utils/dataset/csv_files/{}_node.csv'.format(
                               graph_name)), 'r',
              encoding='utf-8') as fp:
        reader = csv.reader(fp)
        nodes = list(int(_[0]) for _ in reader)
    with open(os.path.join(settings.BASE_DIR,
                           'utils/dataset/csv_files/{}_edge.csv'.format(
                               graph_name)), 'r',
              encoding='utf-8') as fp:
        reader = csv.reader(fp)
        edges = list((int(_[0]), int(_[1])) for _ in reader if _[0] != _[1])
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    return G
