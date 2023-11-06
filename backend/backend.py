from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query',methods=['POST'])
def query():
    print('Hello world!')
    return jsonify({'response':'Hello world!'})

if __name__ == '__main__':
    app.run(debug=True)