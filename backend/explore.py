import psycopg2
import json
import re
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import plotly.express as px
import plotly.offline as pyo
import plotly.graph_objects as go

matplotlib.use(
    "Agg"
)  # Need to use this AGG backend thread thing so it doesn't give errors. Dont remove.
import io
import base64
import decimal

from blockUtils import modify_query

""" 
Parent function to 
Take in SQL Query and returns output. 

input : input query
return_json :  Return in JSON or Text
headers : True if want to manually input headers

Other functions will inherit and use to get result.
"""


# Takes in an argument input_json to format whether the EXPLAIN call needs to return in JSON format or not
def dbquery(input, return_json=False, headers=None):
    result = []
    try:
        # Note: Update these details as accordingly to your details
        connection = psycopg2.connect(
            user="postgres",
            password="Alphate217",
            host="localhost",
            port="5432",
            database="TPCH",
        )

        cursor = connection.cursor()

        # Execute the query

        if headers is not None:
            sql_command = headers + input
        else:
            if return_json:
                sql_command = "EXPLAIN ( ANALYSE, BUFFERS, FORMAT JSON) " + input
            else:
                sql_command = "EXPLAIN ( ANALYSE, BUFFERS, FORMAT TEXT) " + input

        cursor.execute(sql_command)

        # Fetch the column names from the cursor description ,
        # 0 - name  ( From docs https://www.psycopg.org/docs/cursor.html)
        global column_names
        column_names = [desc[0] for desc in cursor.description]

        result = cursor.fetchall()

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            # connection.close()
            # print("PostgreSQL connection is closed")

    return result


"""
Uses the raw text instead of JSON.

Function to extract 
1. Planning Time
2. Execution Time
want from the QEP Analysis Query such as EXPLAIN / ANALYZE
"""


def extract_result_times(input):
    result = dbquery(input, False)
    # print(f"extract_result_times query: {result}")

    planning_time = 0
    execution_time = 0

    # Example result [ ('Seq Scan on region (actual time=0.008..0.009 rows=5 loops=1)',), ('  Buffers: shared hit=1',), ('Planning:',), ('  Buffers: shared hit=63',), ('Planning Time: 0.308 ms',), ('Execution Time: 0.028 ms',)]

    # We gonna use regex to extract out numerical portion
    for item in result:
        portion = item[0]
        if "Planning Time" in portion:
            # Extract planning time
            numerical_portion = re.search(r"(\d+\.\d+)", portion)
            if numerical_portion:
                planning_time = float(
                    numerical_portion.group(0)
                )  # group 0 gives us the entire matched portion i think.
        if "Execution Time" in portion:
            # Extract execution time
            numerical_portion = re.search(r"(\d+\.\d+)", portion)
            if numerical_portion:
                execution_time = float(numerical_portion.group(0))  # similarly here

    # Extract the values from the result
    values = [planning_time, execution_time]

    plt.clf()  # We need this to clear the previous plot. Else, will have overlapping graphs

    plt.bar(["Planning Time", "Execution Time"], values)
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title("Comparison of Planning Time vs Execution Time (Ms)")

    # Annotations
    for i, value in enumerate(values):
        plt.text(i, value, str(value), ha="center", va="bottom", color="red")

    image_stream = io.BytesIO()
    plt.savefig(image_stream, format="png")
    image_stream.seek(0)

    base64_image = base64.b64encode(image_stream.read()).decode("utf-8")

    return planning_time, execution_time, base64_image

def query_analysis(input_json):
    result = json.loads(input_json)
    query_plan = result['Plan']

    nodes = []
    shared_blocks_hit = []
    shared_blocks_read = []

    def extract_data(plan):
        nodes.append(plan['Node Type'])
        shared_blocks_hit.append(plan.get('Shared Hit Blocks', 0))
        shared_blocks_read.append(plan.get('Shared Read Blocks', 0))

        if 'Plans' in plan:
            for child in plan['Plans']:
                extract_data(child)

    extract_data(query_plan)

    # Plotting
    fig, ax = plt.subplots(figsize=(10,6))
    bar_width = 0.35
    index = range(len(nodes))

    bars_hit = plt.barh(index, shared_blocks_hit, bar_width, label='Shared Blocks Hit', color='b')
    bars_read = plt.barh([i + bar_width for i in index], shared_blocks_read, bar_width, label='Shared Blocks Read', color='g')

    plt.ylabel('Node Type')
    plt.xlabel('Number of Blocks')
    plt.title('Shared Blocks Hit and Read for Each Node Type')
    plt.yticks([i + bar_width/2 for i in index], nodes)
    plt.legend()

    # Display values on the right of the bars
    for bar in bars_hit:
        xval = bar.get_width()
        plt.text(xval, bar.get_y() + bar_width/2, round(xval, 2), ha='left', va='center', color='red')

    for bar in bars_read:
        xval = bar.get_width()
        plt.text(xval, bar.get_y() + bar_width/2, round(xval, 2), ha='left', va='center', color='red')

    plt.tight_layout()
    
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format="png")
    image_stream.seek(0)

    base64_image = base64.b64encode(image_stream.read()).decode("utf-8")

    return base64_image
"""
    Block Visualisation Function

    Note : we get column names as a global variable retreived in dbquery function.
"""
# Original one, working for only one table.
# def visualise_blocks(input):
#     # Creating Dataframe from the result of user query
#     modified_input = modify_query(input)
#     print(f'Modified Input (database.py) : {modified_input}')
#     result = dbquery(modified_input, False, headers="")
#     # print(f'blocks.py: result: {result}')
#     df = pd.DataFrame(result, columns = column_names)
#     df.to_clipboard()
#     print(f'\n Dataframe: {df}')


#     df['ctid'] = df['ctid'].str.replace('[()]', '', regex=True)
#     df[['block_number', 'tuple_index']] = df['ctid'].str.split(',', expand=True)
#     df_blocks = df[['block_number', 'tuple_index']]
#     df_blocks = df_blocks.astype(int)
#     blocks_accessed = df_blocks['block_number'].unique()
#     tuples_accessed = df_blocks['tuple_index'].unique()
#     print('Blocks accessed:', blocks_accessed)
#     print('Tuples accessed:', tuples_accessed)
#     fig = px.scatter(df_blocks, x='block_number', y='tuple_index', facet_col="block_number", title='Blocks and Tuples Visualization')
#     fig.show()


def visualise_blocks(input):
    modified_input, tableNames = modify_query(input)
    print(f"Modified Input (database.py) : {modified_input}")
    result = dbquery(modified_input, False, headers="")
    # print(f'blocks.py: result: {result}')
    df = pd.DataFrame(result, columns=column_names)
    df.to_clipboard()
    # print(f"\n Dataframe: {df}")

    for table in tableNames:
        table = table.strip()
        df[f"{table}_ctid"] = df[f"{table}_ctid"].str.replace("[()]", "", regex=True)
        df[["block_number", "tuple_index"]] = df[f"{table}_ctid"].str.split(
            ",", expand=True
        )
        df_blocks = df[["block_number", "tuple_index"]]
        df_blocks = df_blocks.astype(int)
        blocks_accessed = df_blocks["block_number"].unique()
        tuples_accessed = df_blocks["tuple_index"].unique()
        print("Blocks accessed:", blocks_accessed)
        print("Tuples accessed:", tuples_accessed)

        facet_col_spacing = 0.02
        # Use Plotly Express for scatter plot matrix (2d)
        fig = px.scatter_matrix(
            df_blocks,
            dimensions=["block_number", "tuple_index"],
            labels={"block_number": "Block Number", "tuple_index": "Tuple Index"},
        )
        fig.update_layout(title=f"Scatter Matrix for {table}")
        fig.show()

    return df_blocks

# Working but only for Customers , Not Orders. Not cummalative i think
# def visualise_blocks_3d(input):
#     modified_input, tableNames = modify_query(input)
#     print(f"Modified Input (database.py): {modified_input}")
#     result = dbquery(modified_input, False, headers="")
#     df = pd.DataFrame(result, columns=column_names)
#     df.to_clipboard()
#     print(f"\nDataframe: {df}")

#     for table in tableNames:
#         table = table.strip()
#         print(f'database.py: table in tablenames: {table}')
#         df[f"{table}_ctid"] = df[f"{table}_ctid"].str.replace("[()]", "", regex=True)
#         df[["block_number", "tuple_index"]] = df[f"{table}_ctid"].str.split(
#             ",", expand=True
#         )
#         df_blocks = df[["block_number", "tuple_index"]]
#         df_blocks = df_blocks.astype(int)

#         # print(f"Df_blocks before dropping(db.py): {df_blocks}")
#         df_blocks = df_blocks.drop_duplicates()
#         # print(f"Df_blocks after dropping(db.py): {df_blocks}")
#         # Use Plotly Express for 3D scatter plot
#         fig = px.scatter_3d(
#             df_blocks,
#             x="block_number",
#             y="tuple_index",
#             z=df_blocks.index,
#             labels={"block_number": "Block Number", "tuple_index": "Tuple Index"},
#             title="3D Scatter Plot of Blocks and Tuples",
#         )
#         fig.update_layout(
#             width=1000,
#             height=1000,
#         )
#         fig.show()

#         # WE save to HTML file rather than show
#         figure_html = fig.to_html()
#     return figure_html


# Seesm to be cummalative but doesnt work
# def visualise_blocks_3d(input):
#     modified_input, tableNames = modify_query(input)
#     print(f"Modified Input (database.py): {modified_input}")
#     result = dbquery(modified_input, False, headers="")
#     df = pd.DataFrame(result, columns=column_names)
#     df.to_clipboard()
#     print(f"\nDataframe: {df}")

#     df_blocks = pd.DataFrame(columns=["block_number", "tuple_index"])

#     for table in tableNames:
#         table = table.strip()
#         print(f'database.py: table in tablenames: {table}')
#         df[f"{table}_ctid"] = df[f"{table}_ctid"].str.replace("[()]", "", regex=True)
#         df[["block_number", "tuple_index"]] = df[f"{table}_ctid"].str.split(",", expand=True)
#         df_current_blocks = df[["block_number", "tuple_index"]].astype(int)

#         # Keep only the unique combinations that are not already in df_blocks
#         df_current_blocks = df_current_blocks.drop_duplicates()
#         df_current_blocks = df_current_blocks[~df_current_blocks.isin(df_blocks).all(axis=1)]

#         df_blocks = pd.concat([df_blocks, df_current_blocks])

#     df_blocks = df_blocks.drop_duplicates() # remove dupes 
#     print(f"Df_blocks (db.py): {df_blocks}")
    
#     # Use Plotly Express for 3D scatter plot
#     fig = px.scatter_3d(
#         df_blocks,
#         x="block_number",
#         y="tuple_index",
#         z=df_blocks.index,
#         labels={"block_number": "Block Number", "tuple_index": "Tuple Index"},
#         title="3D Scatter Plot of Blocks and Tuples",
#         size_max=18,
#         opacity=0.7,
#     )
#     fig.update_layout(
#         width=1000,
#         height=1000,
#     )
    
#     # WE save to HTML file rather than show
#     figure_html = fig.to_html()
#     return figure_html




""" try"""

def visualise_blocks_3d(input):
    modified_input, tableNames = modify_query(input)
    print(f"Modified Input (database.py): {modified_input}")
    result = dbquery(modified_input, False, headers="")
    df = pd.DataFrame(result, columns=column_names)
    df.to_clipboard()
    print(f"\nDataframe: {df}")

    df_blocks = pd.DataFrame(columns=["block_number", "tuple_index"])

    for table in tableNames:
        table = table.lower()
        table = table.strip()
        print(f'database.py: table in tablenames: {table}')
        
        # Extract block and tuple information for the current table
        print(df.columns)
        df[f"{table}_ctid"] = df[f"{table}_ctid"].str.replace("[()]", "", regex=True)
        df_current_blocks = df[f"{table}_ctid"].str.split(",", expand=True)
        df_current_blocks.columns = ["block_number", "tuple_index"]
        df_current_blocks = df_current_blocks.astype(int)

        # Keep only the unique combinations that are not already in df_blocks
        df_current_blocks = df_current_blocks.drop_duplicates()
        df_current_blocks = df_current_blocks[~df_current_blocks.isin(df_blocks).all(axis=1)]
        print(f'df_current_blocks (database.py): {df_current_blocks}')

        df_blocks = pd.concat([df_blocks, df_current_blocks])


    df_blocks = df_blocks.drop_duplicates()  # remove dupes 
    print(f"Df_blocks (db.py): {df_blocks}")

    # Use Plotly Express for 3D scatter plot
    fig = px.scatter_3d(
        df_blocks,
        x="block_number",
        y="tuple_index",
        z=df_blocks.index,
        labels={"block_number": "Block Number", "tuple_index": "Tuple Index"},
        title="3D Scatter Plot of Blocks and Tuples",
        size_max=18,
        opacity=0.7,
    )
    fig.update_layout(
        width=1000,
        height=1000,
    )

    # Save to HTML file rather than show
    figure_html = fig.to_html()
    return figure_html


""" 
Util Function : Decimal Serializer ; To prevent errors caused by decimals
"""


def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError