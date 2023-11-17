import json
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import graphviz


# Create a directed graph
G = nx.DiGraph()

def add_nodes_edges(plan,parent=None,depth=0,unique_id=None):
    node_id = plan['Node Type']

    node_identifier = f"{node_id}_{depth}_{unique_id}_{plan.get('Alias','')}_{plan.get('Strategy','')}"
    label = f"{node_id}\n"
    label += "\n".join([f"{key}: {value}" for key, value in plan.items() if key != 'Plans' and key != 'Parallel Aware' and key != 'Async Capable' and key != 'Actual Startup Time' and key!='Actual Total Time' and key != 'Workers'])

    G.add_node(node_identifier, label=f"{node_id}{'('+plan.get('Relation Name', '')+')' if len(plan.get('Relation Name',''))>0 else ''}",depth=depth,title=label)
    
    if parent is not None:
        G.add_edge(parent,node_identifier)
    
    if 'Plans' in plan:
        for i,child in enumerate(plan['Plans']):
            add_nodes_edges(child, parent=node_identifier,depth=depth+1,unique_id=i)

def interactive_tree(input_json):
    result = json.loads(input_json)
    query_plan = result['Plan']

    add_nodes_edges(query_plan)
    dot = graphviz.Digraph(comment='Query Plan',graph_attr={'rankdir':'TB'})
    for node, attrs in G.nodes(data=True):
        print(node)
        print(attrs)
        try:
            dot.node(node, attrs['label'], tooltip=attrs['title'],href='#')
        except:
            dot.node(node)

    for edge in G.edges():
        dot.edge(edge[1],edge[0])
        
    dot.render("static/execution_plan_interactive", format="svg", cleanup=True)
    dot.render("execution_plan", format="png", cleanup=True)