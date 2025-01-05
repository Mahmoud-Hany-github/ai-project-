import json

def parse_graph_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data['nodes'], data['edges']

def validate_graph(nodes, edges):
    for edge in edges:
        if edge[0] not in nodes or edge[1] not in nodes:
            raise ValueError(f"Invalid edge: {edge}")
    return True

def preprocess_graph(nodes, edges):
    node_map = {node: idx for idx, node in enumerate(nodes)}
    processed_edges = [(node_map[edge[0]], node_map[edge[1]], edge[2]) for edge in edges]
    return list(node_map.values()), processed_edges
