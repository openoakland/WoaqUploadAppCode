import os
import magic
from flask import Flask, render_template, request
app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return render_template("upload.html")

@app.route("/upload", methods=['POST'])
def upload():
    #Where to put images
    target = os.path.join(APP_ROOT,'files/')
    print(target)
    
    if not os.path.isdir(target):
        os.mkdir(target)
    #For each file in the list,     
    for file in request.files.getlist("file"):
        print(file)
        #filetype = magic.from_file(file)
        #print(filetype)
        filename = file.filename
        #if filetype = '':
            
        #Adding the filename to the files folder
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)
        
    #Load Complete page
    return render_template("complete.html")

if __name__ == "__main__":
    app.run(port=4555, debug=True)
        
