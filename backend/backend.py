from flask import Flask, render_template, request, jsonify
from database import dbquery, extract_result_times

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query',methods=['POST'])
def query():
    input = request.form['queryInput']
    result = dbquery(input)
    
    planning_time , execution_time, base64_image = extract_result_times(input)

    # Debugging print statements 
    print(f'Planning time: {planning_time} \n Execution time: {execution_time}')



    # return result
    # return jsonify({'response': result})

    return render_template('query.html', base64_image=base64_image, result=result)

if __name__ == '__main__':
    app.run(debug=True)