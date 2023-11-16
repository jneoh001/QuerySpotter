import json
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import io
import base64

# def parse_json_plan(json_plan,parent=None):
#     node_label = f"{json_plan['Node Type']} {('('+json_plan.get('Relation Name','')+')' if len(json_plan.get('Relation Name',''))> 0 else '') or json_plan.get('Hash Cond','')}"
#     node = Node(node_label,parent=parent)

#     return node

def create_plan_tree_matplotlib(ax, plan, x, y, parent_text=None):
    node_type = plan.get('Node Type', '')
    node_text = f'{node_type}\nCost: {plan.get("Total Cost", "")}\nRows: {plan.get("Actual Rows", "")}'

    if parent_text:
        node_text = f'{parent_text}\n-->{node_text}'

    ax.text(x, y, node_text, bbox=dict(facecolor='white', alpha=0.8), ha='center', va='center')

    if 'Plans' in plan:
        for i, child_plan in enumerate(plan['Plans']):
            create_plan_tree_matplotlib(ax, child_plan, x + 2 * (i - 0.1), y - 0.1, parent_text=node_text)

def onclick(event):
    plt.close()


def interactive_tree(input_json):
    # fig = go.Figure()

    result = json.loads(input_json)
    query_plan = result['Plan']
    
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.canvas.mpl_connect('button_press_event', onclick)
    ax.set_title('Query Execution Plan')

    create_plan_tree_matplotlib(ax, query_plan, x=1, y=1)
    plt.axis('off')
    plt.show()

    image_stream = io.BytesIO()
    plt.savefig(image_stream, format="png")
    image_stream.seek(0)

    base64_image = base64.b64encode(image_stream.read()).decode("utf-8")

    return base64_image
