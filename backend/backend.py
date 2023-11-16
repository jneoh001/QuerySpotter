from flask import Flask, render_template, request, jsonify
from database import dbquery, extract_result_times
from tree import interactive_tree
from blocks import visualise_blocks
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
    image_path = interactive_tree(result)

    #For Blocks
    visualise_blocks(input_query)

    # For Planning vs Execution Time Graph
    planning_time , execution_time, base64_image = extract_result_times(input_query)

    # Debugging print statements 
    # print(f'Planning time: {planning_time} \n Execution time: {execution_time}')
    # print(f'\n Backend.py query results: {result}')

    return render_template('query.html', base64_image=base64_image, result=result,image_path=image_path)

if __name__ == '__main__':
    app.run(debug=True)