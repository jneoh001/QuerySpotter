import re 

''' File containing utility functions for block visualisation'''


# input_query = " SELECT * FROM customer as c, orders as o WHERE c.c_custkey = o.o_custkey"
# input_query = " SELECT * FROM customer, orders WHERE customer.c_custkey = orders.o_custkey "
# input_query = "SELECT * FROM region, customer, orders"

''' Function to add CTID query commands to SQL Query. 
    Returns 1. Modified Query 2. Table Names 
'''

def modify_query(input_query):

    from_split = input_query.split("FROM")
    select_part = from_split[0]
    # print(from_split)

    if re.search(r'\bWHERE\b', from_split[1], re.IGNORECASE):
        where_split = from_split[1].split("WHERE")
        tableNames = extract_tables_or_aliases(where_split[0])
        # print(tableNames)
    else:
        tableNames = from_split[1] # dont need to split by WHERE here.
        tableNames = tableNames.split(", ")
        # print(tableNames)

    for table in tableNames:
        select_part += f", {table}.ctid as {table}_ctid"   
    
    # print(select_part)
    
    modified_query = select_part + " FROM" + from_split[1]
    # print(modified_query)
    return modified_query, tableNames


''' Helper to  Extract table name or aliases '''

def extract_tables_or_aliases(input_string):
    # Try to find aliases
    aliases = re.findall(r'\bAS\s+(\w+)', input_string, re.IGNORECASE)
    if aliases:
        return aliases

    # If no aliases, find table names
    tables = re.findall(r'\b(\w+)\b', input_string)
    return tables




# result = modify_query(input_query)
# print(result)