import os
from flask import Flask, render_template, request
from werkzeug.datastructures import FileStorage
from joiner_scripts.joiner import AqGpsJoiner
import datetime

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return render_template("upload.html")
#Runs once file is uploaded
@app.route("/upload", methods=['POST'])
def upload():
    now = datetime.datetime.now()
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
        #Creates a file 
        finalFile = 'JoinedAirQualityAndGPSData'+str(now)+'.csv'
        f = open(finalFile,"w+")
        f.close()
        #finalFileaddress = open(finalFile,"w")
        joiner = AqGpsJoiner(csvFile, logFile, finalFile, tdiff_tolerance_secs=1, filter_size='10')
        #f.close()
        joiner.createFile()
        

        #Creates a markdown file and saves it
        markDownFile =  str(now)+'.markdown'

        filename = markDownFile
        #Adding the filename to the files folder
        destination = "/".join([target, filename])
        print(destination)
        f.close()

        mD = open(markDownFile,"w+")
        mD.write('--- \ntitle: WOEIP Air Quality 02-2010 \nowner: <a href="https://www.woeip.org/">WOEIP</a>\nlayout: data\nmonth:'+now.month+'\nyear: '+now.year+'\ncategories: WOEIP\nresourceType: shift_by_month\nfileName: '+finalFile+'\n---')
        mD.close()


        mDtemp = FileStorage(markDownFile)
        mDtemp.save(destination)

        #Saves file
        filename = finalFile
        #Adding the filename to the files folder
        destination = "/".join([target, filename])
        print(destination)
        f.close()

        with open(finalFile,'r') as fj:
            fi = FileStorage(fj)
            fi.save(destination)
        #GET /repos/:owner/:repo/git/commits/:commit_sha   
    #Load Complete page
    return render_template("complete.html")

if __name__ == "__main__":
    app.run(port=4555, debug=True)
        
