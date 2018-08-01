import os
from flask import Flask, render_template, request
from joiner_scripts.joiner import AqGpsJoiner

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return render_template("upload.html")
#Runs once file is uploaded
@app.route("/upload", methods=['POST'])
def upload():
    csvFile = ''
    logFile = ''
    #Folder where files are put
    target = os.path.join(APP_ROOT,'files/')
    print(target)
    #If the directory does not exist, make it
    if not os.path.isdir(target):
        os.mkdir(target)
    #For each file in the list,     
    for file in request.files.getlist("file"):
        print(file)
        #print(filetype)
        #Checks whether file is a csv or log
        filename = file.filename
        filetype = filename.split('.')[1]
        if filetype == 'csv':
            print('filetype is csv')
            csvFile = file
        elif filetype == 'log':
            logFile = file
    if csvFile != '' and logFile != '':
        print(csvFile)
        print(logFile)
        finalFile = 'JoinedFile.csv'
        f = open(finalFile,"w+")
        f.close()
        #finalFileaddress = open(finalFile,"w")
        joiner = AqGpsJoiner(csvFile, logFile, finalFile, tdiff_tolerance_secs=1, filter_size='10')
        #f.close()
        joiner.createFile()
        filename = finalFile
        #Adding the filename to the files folder
        destination = "/".join([target, filename])
        print(destination)
        #f.close()
        #Saves file
        #with open(f,'r') as fi:
        f = FileStorage(f)
        f.save(destination)   
    #Load Complete page
    return render_template("complete.html", filetype=filetype, file2=csvFile)

if __name__ == "__main__":
    app.run(port=4555, debug=True)
        
