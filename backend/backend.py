from flask import Flask, render_template, request, jsonify, session
from database import dbquery, extract_result_times, visualise_blocks_3d
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
    session['query'] = input_query # Need to store the user's input query as session to reuse in other routes.
    # For Plots 
    result = dbquery(input_query,True)
    result = json.dumps(result[0][0][0]) # Access down to the JSON level. 
    
    #For Tree
    image_path = interactive_tree(result)

    # For blocks
    visualise_blocks_3d(input_query)

    # For Planning vs Execution Time Graph
    planning_time , execution_time, base64_image = extract_result_times(input_query)

    # Debugging print statements 
    # print(f'Planning time: {planning_time} \n Execution time: {execution_time}')
    # print(f'\n Backend.py query results: {result}')

    return render_template('query.html', base64_image=base64_image, result=result,image_path=image_path)


@app.route('/query/blocktuples')
def blocktuples():
    input_query = session.get('query')
    figure_html = visualise_blocks_3d(input_query)
    return render_template('blocktuples.html', figure_html=figure_html)










if __name__ == '__main__':
    app.run(debug=True)



# #Dash stuff

# # Create the Dash app with the existing Flask app instance
# dash_app = dash.Dash(__name__, server=app, url_base_pathname='/dash/')

# dash_app.layout = html.Div([
#     dcc.Dropdown(
#         id='block-dropdown',
#         multi=True
#     ),
#     dcc.Graph(id='block-plot')
# ])


# Tried using dash

# @app.callback(
#     Output('block-plot', 'figure'),
#     [Input('block-dropdown', 'value')]
# )
# def update_plot(selected_block_numbers):
#     if not selected_block_numbers:
#         raise PreventUpdate

#     # Assuming you have a df_blocks DataFrame for block data
#     df_blocks = visualise_blocks(input_query)

#     df_blocks_filtered = df_blocks[df_blocks['block_number'].isin(selected_block_numbers)]

#     blocks_accessed = df_blocks_filtered['block_number'].unique()
#     tuples_accessed = df_blocks_filtered['tuple_index'].unique()
    
#     print('Blocks accessed:', blocks_accessed)
#     print('Tuples accessed:', tuples_accessed)
    
#     fig = px.scatter(
#         df_blocks_filtered,
#         x='block_number',
#         y='tuple_index',
#         facet_col="block_number",
#         title='Blocks and Tuples Visualization'
#     )
#     return fig


