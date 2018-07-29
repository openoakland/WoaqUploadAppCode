from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
#@app.route('/hello/Ethan')
def hello():
    name2 = 'Ethan'
    return render_template('index.html', name=name2)
#@app.route('/')
#def hello_world():
#    return 'Hello, World!'
