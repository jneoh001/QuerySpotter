import json
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import graphviz


# Create a directed graph
G = nx.DiGraph()

def add_nodes_edges(plan,parent=None,relation_names=None,depth=0):
    node_id = plan['Node Type']
    relation_name = plan.get('Relation Name', '')
    filter_condition = plan.get('Filter', '')
    hash_condition = plan.get('Hash Cond', '')

    
    if relation_name and relation_names is not None and node_id in relation_names:
        node_id = f"{node_id}_{relation_name}"
        relation_names[node_id] = relation_name
    else:
        relation_names[node_id] = relation_name
    
    label = f"{node_id}\n{relation_name}\n{filter_condition}\n{hash_condition}"
    G.add_node(node_id, label=f"{node_id}\n{relation_name}",depth=depth,title=label)
    
    if parent is not None:
        G.add_edge(parent, node_id)
    
    if 'Plans' in plan:
        for child in plan['Plans']:
            add_nodes_edges(child, parent=node_id, relation_names=relation_names,depth=depth+1)

def interactive_tree(input_json):
    result = json.loads(input_json)
    query_plan = result['Plan']

    add_nodes_edges(query_plan, relation_names={})
    dot = graphviz.Digraph(comment='Query Plan',graph_attr={'rankdir':'TB'})
    for node, attrs in G.nodes(data=True):
        dot.node(node, attrs['label'], tooltip=attrs['title'],href='#')

    for edge in G.edges():
        dot.edge(edge[1],edge[0])
        
    dot.render("static/execution_plan_interactive", format="svg", cleanup=True)
    dot.render("execution_plan", format="png", cleanup=True)