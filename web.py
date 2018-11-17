import os
from flask import Flask, render_template, request
from werkzeug.datastructures import FileStorage
from github import Github
from joiner_scripts.joiner import AqGpsJoiner
import datetime
import base64

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    g = Github("fa0dfb5e6103c9bf91cbbcc22e3c1aa5708cbdb4")
    repo = g.get_user().get_repo('woaq')
    contents = repo.get_contents("_Posts")
    #print(contents)
    #csvFileTemp = repo.get_contents('/_Posts/'+filename)
    #print('CSVFile below:')
    # while len(contents) > 1:
    #     file_content = contents.pop(0)
    #     if file_content.path == "_Posts":
    #         contents.extend(repo.get_contents(file_content.path))
    #     else:
    #         print(file_content)
    return render_template("home.html",databaseFiles=contents)
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
        elif filetype == 'txt':
            textFile = file

    if csvFile != '' and logFile != '':
        print(csvFile)
        print(logFile)
        #Creates a file 
        finalFile = 'JoinedAirQualityAndGPSData'+str(now)+'.csv'
        f = open(finalFile,"w+")
        f.close()
        #finalFileaddress = open(finalFile,"w")
        try:
            joiner = AqGpsJoiner(csvFile, logFile, finalFile, tdiff_tolerance_secs=1, filter_size='2.5')
            #f.close()
            joiner.createFile()
        except Exception as e:
            return render_template("WrongFileFormat.html")
        #Creates a markdown file and saves it
        markDownFile =  str(now)+'.markdown'

        filename = markDownFile
        #Adding the filename to the files folder
        destination = "/".join([target, filename])
        print(destination)
        f.close()

        """"mD = open(markDownFile,"w+")
        mD.write('--- \ntitle: WOEIP Air Quality 02-2010 \nowner: <a href="https://www.woeip.org/">WOEIP</a>\nlayout: data\nmonth:'+str(now.month)+'\nyear: '+str(now.year)+'\ncategories: WOEIP\nresourceType: shift_by_month\nfileName: '+finalFile+'\n---')
        mD.close()
        with open(markDownFile,'r') as fz:
            fk = FileStorage(fz)
            fk.save(destination)"""

        #mD = open(markDownFile,"w+")
        mD = '--- \ntitle: WOEIP Air Quality 02-2018 \nowner: <a href="https://www.woeip.org/">WOEIP</a>\nlayout: data\nmonth: '+str(now.month)+'\nyear: '+str(now.year)+'\ncategories: WOEIP\nresourceType: shift_by_month\nfileName: '+filename+'\n---'
        
        #Saves markdown file on github
        #Get authorization code
        try:
            #g = Github("c67078bb82f2d570125166f77089f78565caba1d")
            
            #g = Github("fe45e3a06969900ef870e3a49adcc051e4172482")
            #g = Github("a0740516bc41f331e1dfc84ef64cedadd8d35c0e")
            g = Github("fa0dfb5e6103c9bf91cbbcc22e3c1aa5708cbdb4")
            #For app
            #Current pygithub version: 1.40, flask 1.0.2
            #g = Github("v1.b6634b8e67d274dfe131b07b9dd3494cd2446d12")
            #Get repository
            repo = g.get_user().get_repo('woaq')#Need to change repository to main repository
            repo.create_file('_posts/'+markDownFile,"Added a new air quality markdown data file on "+str(now)+"date.",mD,branch='gh-pages')
            #Saves file
            filename = finalFile
            #Adding the filename to the files folder
            destination = "/".join([target, filename])
            print(destination)
            f.close()
            #Commits the optional text file 

            try:
                #g = Github("fe45e3a06969900ef870e3a49adcc051e4172482")
                #g = Github("a0740516bc41f331e1dfc84ef64cedadd8d35c0e")
                g = Github("fa0dfb5e6103c9bf91cbbcc22e3c1aa5708cbdb4")
                with open(textFile,'r') as fl:
                    data = fl.read()
                    if textFile != '':
                        repo.create_file('_Posts/'+filename+".txt","Added a new air quality text data file on "+str(now)+"date",data,branch='gh-pages')
            except Exception as e:
                print(e)

            with open(finalFile,'r') as fj:
                data = fj.read()
                #Final csv file commit:
                #This mat 
                repo.create_file('_Posts/'+filename,"Added a new air quality csv data file on "+str(now)+"date",data,branch='gh-pages')
                print(filename)
                #Gets CSV File from github
                #csvFile = repo.get_contents('/_Posts/'+filename)
                #print(csvFile)

                #fi = FileStorage(fj)
                #fi.save(destination)
                print(filename)
        except Exception as e:
            print(e)
            return render_template("authWrong.html")
        
        #GET /repos/:owner/:repo/git/commits/:commit_sha   
    #Load Complete page
        #repo.g
        with open(finalFile,'r') as fd:
                data = fd.read()
                #print(data)
                csvFile = str(data)
                return render_template("complete.html",csvFile=csvFile)
    else:
        return render_template("WrongFile.html")
@app.route("/databaseFiles",methods=['POST','GET'])
def loadDatabase():
    filename = request.args.get('param', '')
    print(filename)
    if (request.method == 'GET'):
        #filename = "JoinedAirQualityAndGPSData2018-11-14 01:55:04.860057.csv"
        g = Github("fa0dfb5e6103c9bf91cbbcc22e3c1aa5708cbdb4")
        repo = g.get_user().get_repo('woaq')

        contents = repo.get_contents(filename)
        print(contents)
        csvFileTemp = contents
        print('CSVFile below:')
        
        #print(csvFileTemp.content)
        #return render_template('complete.html',csvFile=csvFile)
        #with open(csvFileTemp.content,'r') as fd:
        #    data = fd.read()
        #    print(data)
        #    csvFile = str(data)
        csvFileTemp = base64.b64decode(csvFileTemp.content)
        return render_template('complete.html',csvFile=csvFileTemp)
    



if __name__ == "__main__":
    print("Using expired github token:"+str(g))
    app.run(port=4555, debug=True)
        
