from flask import Flask, render_template, request, jsonify
from database import dbquery

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query',methods=['POST'])
def query():
    input = request.form['queryInput']
    result = dbquery(input)

    return result
    # return jsonify({'response': result})

if __name__ == '__main__':
    app.run(debug=True)