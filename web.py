import os
from flask import Flask, render_template, request
from joiner_scripts.joiner import AqGpsJoiner

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return render_template("upload.html")

@app.route("/upload", methods=['POST'])
def upload():
    csvFile = ''
    logFile = ''
    #Folder where files are put
    target = os.path.join(APP_ROOT,'files/')
    print(target)
    
    if not os.path.isdir(target):
        os.mkdir(target)
    #For each file in the list,     
    for file in request.files.getlist("file"):
        print(file)
        #print(filetype)
        filename = file.filename
        filetype = filename.split('.')[1]
        if filetype == 'csv':
            print('filetype is csv')
            csvFile = file
            #Adding the filename to the files folder
            destination = "/".join([target, filename])
            print(destination)
            csvFile = file.save(destination)
        elif filetype == 'log':
            logFile = file
            #Adding the filename to the files folder
            destination = "/".join([target, filename])
            print(destination)
            logFile = file.save(destination)
    

    if csvFile != '' and logFile != '':
        print(csvFile)
        print(logFile)
        finalFile = 'JoinedFile.csv'
        joiner = AqGpsJoiner(csvFile, logFile, finalFile, tdiff_tolerance_secs=1, filter_size='10')
        joiner.createFile()
        filename = finalFile.filename
        
    

        
    #Load Complete page
    return render_template("complete.html", filetype=filetype, file2=csvFile)

if __name__ == "__main__":
    app.run(port=4555, debug=True)
        
