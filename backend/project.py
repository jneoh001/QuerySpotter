from flask import Flask, render_template, request, send_from_directory, session
from explore import dbquery, extract_result_times, visualise_blocks_3d, query_analysis, visualise_blocks 
from tree import interactive_tree
import json
import dash
# import dash_core_components as dcc
# import dash_html_components as html
from dash import dcc 
from dash import html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate



app = Flask(__name__)
app.secret_key = 'DatabaseGroup30' # need to set secretkey to allow me to use sessions. security 

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query',methods=['POST'])
def query():
    input_query = request.form['queryInput']
    input_query = input_query.replace('\r', '').replace('\n', ' ') # Clear up escape sequences.
    session['query'] = input_query # Need to store the user's input query as session to reuse in other routes.
    # For Plots 
    result = dbquery(input_query,True)
    result = json.dumps(result[0][0][0]) # Access down to the JSON level. 
    
    #For Tree
    interactive_tree(result)
    base64_analysis = query_analysis(result)
    # For blocks
    #visualise_blocks_3d(input_query)

    visualise_blocks(input_query)
    # For Planning vs Execution Time Graph
    planning_time , execution_time, base64_image = extract_result_times(input_query)

    # For query analysis
    
    # Debugging print statements 
    # print(f'Planning time: {planning_time} \n Execution time: {execution_time}')
    # print(f'\n Backend.py query results: {result}')

    return render_template('query.html', base64_image=base64_image, base64_analysis=base64_analysis)

@app.route('/query/graph',methods=['GET'])
def show_graph():
    return send_from_directory('static','images/execution_plan_interactive.svg')


# @app.route('/query/blocktuples')
# def blocktuples():
#     input_query = session.get('query')
#     figure_html = visualise_blocks_3d(input_query)
#     return render_template('blocktuples.html', figure_html=figure_html)


if __name__ == '__main__':
    app.run(debug=True)


