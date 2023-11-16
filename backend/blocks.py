from database import dbquery
import pandas as pd
import json

def visualise_blocks(input):
    # modified_input = modify_query(input)
    # result = dbquery(modified_input, True)
    # data = result[0]  # Get the list of dictionaries
    # print(f'blocks.py: data: {data}')
    # df = pd.read_json(data)  # Create a DataFrame from the list
    # print(f'\n Dataframe: {df}')
    print("hi")

def modify_query(input_query):
    # Split the query into parts
    parts = input_query.split("FROM")

    # Add 'ctid,' to the select part
    select_part = parts[0].strip() + ",ctid"

    # Combine the parts back into a single query
    modified_query = " FROM".join([select_part, parts[1]])

    return modified_query
