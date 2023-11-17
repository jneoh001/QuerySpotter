from flask import Flask, render_template, request, send_from_directory
from database import dbquery, extract_result_times, visualise_blocks
from tree import interactive_tree
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query',methods=['POST'])
def query():
    input_query = request.form['queryInput']

    # For Plots 
    result = dbquery(input_query,True)
    result = json.dumps(result[0][0][0]) # Access down to the JSON level. 
    
    #For Tree
    interactive_tree(result)

    # For blocks
    #visualise_blocks(input_query)
    # For Planning vs Execution Time Graph
    planning_time , execution_time, base64_image = extract_result_times(input_query)

    # Debugging print statements 
    # print(f'Planning time: {planning_time} \n Execution time: {execution_time}')
    # print(f'\n Backend.py query results: {result}')

    return render_template('query.html', base64_image=base64_image, result=result)

@app.route('/query/graph',methods=['GET'])
def shopw_graph():
    return send_from_directory('static','execution_plan_interactive.svg')

if __name__ == '__main__':
    app.run(debug=True)