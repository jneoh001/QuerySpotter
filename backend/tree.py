import igraph
from igraph import Graph, EdgeSeq

def nodes(input_text):
    operations = []

    # seperate planning portion from operations portion
    counter_planning = 0
    for i in range(len(input_text)):
        if 'Planning:' in input_text[i][0]:
            counter_planning = i
            break

    filtered_input_text = input_text[:counter_planning]

    # Dealing with operations portion
    operation_list = [0]
    for i in range(len(filtered_input_text)):
        if '->' in filtered_input_text[i][0]:
            operation_list.append(i)
    
    print(operation_list)
    for i in range(len(operation_list)-1):
        operations.append(filtered_input_text[operation_list[i]:operation_list[i+1]])
    
    operations.append(filtered_input_text[operation_list[-1]:])
    return operations

def tree(input_text):
    operations = nodes(input_text)
    num_nodes = len(operations)

    return operations