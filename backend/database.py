import psycopg2
import json

''' 
Takes in SQL Query and Returns JSON of output.
'''

def dbquery( input ):
    result = []
    try:
        # Note: Update these details as accordingly to your details
        connection = psycopg2.connect(user="postgres",
                                      password="root",
                                      host="localhost",
                                      port="5432",
                                      database="TPC-H")

        cursor = connection.cursor()

        cursor.execute(input)

        rows = cursor.fetchall()
        for row in rows:
            result.append(row)

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    
    return result
    # return json.dumps(result)
