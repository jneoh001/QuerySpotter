import json
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

# Create a directed graph
G = nx.DiGraph()
G.graph['rankdir'] = 'TB'

def add_nodes_edges(plan,parent=None,relation_names=None):
    node_id = plan['Node Type']
    relation_name = plan.get('Relation Name', '')
    
    if relation_name and relation_names is not None and node_id in relation_names:
        node_id = f"{node_id}_{relation_name}"
        relation_names[node_id] = relation_name
    else:
        relation_names[node_id] = relation_name
    
    G.add_node(node_id, label=f"{node_id}\n{relation_name}")
    
    if parent is not None:
        G.add_edge(parent, node_id)
    
    if 'Plans' in plan:
        for child in plan['Plans']:
            add_nodes_edges(child, parent=node_id, relation_names=relation_names)

def interactive_tree(input_json):
    result = json.loads(input_json)
    query_plan = result['Plan']

    # Add nodes recursively
    G.add_node(query_plan['Node Type'],label=query_plan['Node Type'])
    add_nodes_edges(query_plan['Plans'][0],query_plan['Node Type'],relation_names={})

    # Draw Directed graph
    pos = nx.circular_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=1000, node_color='lightblue')
    nx.draw_networkx_edges(G, pos, edge_color='black',width=2.0, arrows=True,arrowstyle='-|>')
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
    plt.show()

    
    # Making it interactive using plotly
    pos = nx.circular_layout(G)
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        mode='lines',
    )
    
    node_x = []
    node_y = []
    node_text = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        marker=dict(
            symbol='square',
            showscale=True,
            reversescale=True,
            size=10,
        ),
        text=node_text,
        textposition="bottom center",
    )

    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(edge_trace)
    fig.add_trace(node_trace)

    fig.update_layout(
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=0),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    )

    image_path = 'static/images/interactive_tree.png'
    pio.write_image(fig, image_path,format='png')

    return image_path
