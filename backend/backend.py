from flask import Flask, render_template, request, jsonify
from database import dbquery, extract_result_times
from tree import tree

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query',methods=['POST'])
def query():
    input_query = request.form['queryInput']
    result = dbquery(input_query,True)

    print(result)
    operations = tree(result)

    planning_time , execution_time, base64_image = extract_result_times(input_query)

    # Debugging print statements 
    print(f'Planning time: {planning_time} \n Execution time: {execution_time}')

    return render_template('query.html', base64_image=base64_image, result=operations)

if __name__ == '__main__':
    app.run(debug=True)