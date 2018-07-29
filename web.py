from flask import Flask, render_template
app = Flask(__name__)

@app.route('/hello/')
#@app.route('/hello/Ethan')
def hello():
    return render_template('render_template.html', name='Ethan')
#@app.route('/')
#def hello_world():
#    return 'Hello, World!'
