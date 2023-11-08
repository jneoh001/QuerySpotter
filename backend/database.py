import psycopg2
import json
import re
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use(
    "Agg"
)  # Need to use this AGG backend thread thing so it doesn't give errors. Dont remove.
import io
import base64
import decimal

""" 
Parent function to 
Take in SQL Query and returns output. 

Other functions will inherit and use to get result.
"""


def dbquery(input):
    result = []
    try:
        # Note: Update these details as accordingly to your details
        connection = psycopg2.connect(
            user="postgres",
            password="root",
            host="localhost",
            port="5432",
            database="TPC-H",
        )

        cursor = connection.cursor()

        cursor.execute(input)

        # Fetch the column names from the cursor description ,
        # 0 - name  ( From docs https://www.psycopg.org/docs/cursor.html)
        column_names = [desc[0] for desc in cursor.description]

        rows = cursor.fetchall()
        for row in rows:
            row_dict = {}
            for i in range(len(column_names)):
                row_dict[column_names[i]] = row[i]
            result.append(row_dict)

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    # return result
    return json.dumps(result, default=decimal_default)


"""
Function to extract 
1. Planning Time
2. Execution Time
want from the QEP Analysis Query such as EXPLAIN / ANALYZE
"""


def extract_result_times(input):
    # Place this at the start to get info about the query
    final_input = "EXPLAIN ( analyze, buffers, costs off )" + input
    result = dbquery(final_input)
    result = json.loads(result)
    # For Debugging
    # print(f'Final input: {final_input}')
    print(f"extract_result_times query: {result}")

    planning_time = 0
    execution_time = 0

    # Example result [ ('Seq Scan on region (actual time=0.008..0.009 rows=5 loops=1)',), ('  Buffers: shared hit=1',), ('Planning:',), ('  Buffers: shared hit=63',), ('Planning Time: 0.308 ms',), ('Execution Time: 0.028 ms',)]

    # We gonna use regex to extract out numerical portion

    for item in result:
        if "QUERY PLAN" in item:
            # Extract the relevant part of the QUERY PLAN
            query_plan = item["QUERY PLAN"]

            if "Planning Time" in query_plan:
                # Extract planning time
                numerical_portion = re.search(r"(\d+\.\d+)", query_plan)
                if numerical_portion:
                    planning_time = float(
                        numerical_portion.group(0)
                    )  # group 0 gives us the entire matched portion i think.
            if "Execution Time" in query_plan:
                # Extract execution time
                numerical_portion = re.search(r"(\d+\.\d+)", query_plan)
                if numerical_portion:
                    execution_time = float(numerical_portion.group(0))  # similarly here

    # Extract the values from the result
    values = [planning_time, execution_time]

    plt.clf() # We need this to clear the previous plot. Else, will have overlapping graphs
    
    plt.bar(["Planning Time", "Execution Time"], values)
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title("Comparison of Planning Time vs Execution Time (Ms)")

    # Annotations
    for i, value in enumerate(values):
        plt.text(i, value, str(value), ha="center", va="bottom", color='red')

    image_stream = io.BytesIO()
    plt.savefig(image_stream, format="png")
    image_stream.seek(0)

    base64_image = base64.b64encode(image_stream.read()).decode("utf-8")

    return planning_time, execution_time, base64_image





''' 
Util Function : Decimal Serializer ; To prevent errors caused by decimals
'''

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError