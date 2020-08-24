from flask import Flask,flash, redirect, url_for, request, render_template, session, send_from_directory , jsonify
from werkzeug.utils import secure_filename
import pymysql
import os
import datetime
import mammoth
import traceback
from DBHandler import DBHandler
from DBError import DBError
from email import policy
from email.parser import BytesParser


from bs4 import BeautifulSoup,NavigableString


from EntityExtractor import EntityExtractor
from EntityRelation import EntityRelation
import OCR

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'docx','msg'])


app = Flask(__name__)
app.config.from_object('config')
app.secret_key = app.config["SECRET_KEY"]


@app.route('/')
@app.route('/hello')
def hello_world():
    return render_template('login.html', error=None)
@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html', error=None)
    # return 'Hello World!'
@app.route('/success/<n>')
def success(n):
    print("Test")
    return 'welcome %s' % n

@app.route('/createProjectForm')
def createProjectForm():
    print("In Project Creation Getting Projects")
    projectList = []
    error = None
    DBHandler_ = DBHandler(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"],
                           app.config["DATABASE"])
    projectList = []

    error = None
    projectlistJSON = []
    try:

        projectList_ = DBHandler_.getProjectList(session['user'])
        projectlistJSON = DBHandler_.getProjectJSON(session['user'])
        if (projectList != []):
            session['projectList'] = projectList_
    except DBError  as e:
        error = e
    finally:
        del DBHandler_


    return render_template('createProject.html',projectList=projectlistJSON, email=session['user'])

@app.route('/createproject',methods=['POST', 'GET'])
def createproject():
    print("In Project Creation")
    if request.method == 'POST':
        pname = request.form['pname']
        pDesc = request.form['pDesc']

    error = None
    projectList =[]
    projectlistJSON = []
    DBHandler_ = DBHandler(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"],
                           app.config["DATABASE"])
    error = None
    try:

         create = DBHandler_.createProject(pname,pDesc,session['user'])
         projectList = DBHandler_.getProjectList(session['user'])
         projectlistJSON = DBHandler_.getProjectJSON(session['user'])
         if(projectList !=[]):
             session['projectList'] = projectList

    except DBError  as e:
        error = e

    return render_template('createProject.html',projectList=projectlistJSON, email=session['user'])


@app.route('/addFileForm')
def addFileForm():
    return render_template('addfiles.html',projectList=session['projectList'], email=session['user'])




@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('success', n=str(user)))
    else:
        user = request.args.get('nm')
        return redirect(url_for('success', n=str(user)))


class ServerError(Exception): pass


@app.route('/signin', methods=['POST', 'GET'])
def signin():

    error = None
    try:
        db = pymysql.connect(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"],
                             app.config["DATABASE"])
        cur = db.cursor()

        if request.method == 'POST':
            email_form = request.form['email']
            print(email_form)
            sql = 'SELECT COUNT(1) FROM USERS WHERE email = %s ;'

            args = (email_form)

            cur.execute(sql, args)

            if not cur.fetchone()[0]:
                print("why")
                raise ServerError('Invalid Email')


            password_form = request.form['password']
            # cur.execute("SELECT password FROM USERS WHERE email = {};"
            # .format(email_form))
            sql2 = 'SELECT password FROM USERS WHERE email = %s ;'

            args2 = (email_form)
            cur.execute(sql2, args2)
            projectList = []
            error = None

            DBHandler_ = DBHandler(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"],
                                   app.config["DATABASE"])
            try:
                projectList = DBHandler_.getProjectList(email_form)

                session['projectList'] = projectList
                print(session['projectList'])
            except DBError  as e:
                error = str(e)
                print(str(e))


            for row in cur.fetchall():
                #print(type(password_form))
               # print(row[0].strip("'"))
                print(password_form)
                print(row[0])
                if password_form == row[0]:
                    session['user'] = request.form['email']
                    return render_template('addfiles.html',projectList=session['projectList'], error=error ,email=session['user'])
                else:
                    raise ServerError('Invalid password')
    except ServerError as e :
        error = str(e)
    except Exception as e:
        error = str(e)

    return render_template('login.html', error=error)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    error = None
    db = None
    try:


        db = pymysql.connect(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"],
                             app.config["DATABASE"])
        cur = db.cursor()

        email = request.form['email']
        password = request.form['password']
        fname = request.form['fname']
        lname = request.form['lname']
        sql = 'INSERT INTO USERS (email,password,fname,lname) VALUES (%s,%s,%s,%s)'

        args = (email.strip("'"), password.strip("'"), fname.strip("'"), lname.strip("'"))
        # Execute the SQL command
        cur.execute(sql, args)
        # Commit your changes in the database
        db.commit()

        # return redirect(url_for('success', n=str(email)))
        print("yooooooooooooooo")
        session['user']=email
        return render_template('addfiles.html',projectList=session['user'], email=email)

    except Exception as e:
        print(e)
        error = str(e)
        return render_template('login.html', error=error)

    finally:
        if(db !=None):
            db.close()



@app.route('/upload')
def upload_file():
    return render_template('addfiles.html',email=session['user'])



@app.route('/addfile')
def addfile():
    return render_template('addfiles.html',projectList=session['projectList'],email=session['user'])
@app.route('/searchEntity')
def searchEntity():

    return render_template('search.html',projectList=session['projectList'],email=session['user'])

@app.route('/ShowFileEntity_')
def ShowFileEntity_():
    return render_template('ShowFileEntity.html',email=session['user'])



@app.route('/addUserForm')
def addUserForm():
    return render_template('AddUser.html',projectList=session['projectList'],email=session['user'])




@app.route('/uploader', methods=['GET', 'POST'])
def upload_file_():
    try:
        print("Here in uploader")
        file = request.files['file']
        pname = request.form['pname']
        print(file)
        print(pname)

        if request.method == 'POST':
            file = request.files['file']
            pname = request.form['pname']
            lang = request.form['lang']

            if file.filename == '':
                print("file name is empty")
                return redirect(url_for('addfiles.html',
                                        message='No selected file'))
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.filename.replace(" ","_")
                print("file",file.filename)

                file.save(os.path.join(app.config['UPLOAD_PATH_PDF'], filename))
                datetime_now = datetime.datetime.now();
                formatted_date = datetime_now.strftime('%Y-%m-%d')
                db = pymysql.connect(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"],
                                     app.config["DATABASE"])
                cur = db.cursor()
                sql = 'INSERT INTO Project_Files (FileName,ProjectName,ProjectUserID,UploadDate,UploadPath,Nodes,Edges,FileEntities,URL) VALUES (%s,%s, %s ,%s,%s,%s,%s,%s,%s)'
                entityExtractor_ = None
                document_url = None
                if (".docx" in file.filename):
                    with open(app.config['UPLOAD_PATH_PDF'] + file.filename, "rb") as docx_file:
                        result = mammoth.convert_to_html(docx_file)
                        html = result.value  # The generated HTML

                    temp = file.filename.replace(".docx", "")
                    Html_file = open(app.config['UPLOAD_PATH_PDF'] + temp + ".html", "w")
                    Html_file.write(html)
                    Html_file.close()
                    document_url = "http://george.runmy.tech:5000/static/web/"+ temp + ".html"

                    entityExtractor_ = EntityExtractor(lang,app.config['UPLOAD_PATH_PDF'] + file.filename,pname.strip("'"),document_url,app.config['GOOGLE_API_KEY'],app.config['NLP_API_KEY'],app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"],
                         app.config["DATABASE"],file.filename)
                    entityExtractor_.getEntityDocxJson()

                elif(".txt" in file.filename):
                    temp = file.filename.replace(".txt", "")
                    data = ""
                    html = "<html></html>"
                    soup = BeautifulSoup(html)
                    htmltag = soup.find('html')
                    body = soup.new_tag("body")
                    with open(app.config['UPLOAD_PATH_PDF'] + file.filename, "r") as myfile:
                        data = myfile.read()
                    paras = data.split("\n\n")
                    for para in paras:
                        html = "<p></p>"
                        souppara = BeautifulSoup(html)
                        ptag = souppara.find('p')
                        ptag.insert(0, NavigableString(para))
                        body.append(ptag)
                    htmltag.append(body)
                    html_page = soup.prettify("utf-8")
                    with open(app.config['UPLOAD_PATH_PDF'] + temp + ".html", "wb+") as filewriter:
                        filewriter.write(html_page)
                    document_url = "http://george.runmy.tech:5000/static/web/" + temp + ".html"
                    entityExtractor_ = EntityExtractor(lang,app.config['UPLOAD_PATH_PDF'] + filename,pname.strip("'"), document_url,app.config['GOOGLE_API_KEY'],app.config['NLP_API_KEY'],app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"],
                         app.config["DATABASE"],file.filename)
                    entityExtractor_.getEntityTxtJson()
                elif(".msg" in file.filename):
                    #pythoncom.CoInitialize()
                    #outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
                    #temp = file.filename.replace(".msg", "")

                    #msg = outlook.OpenSharedItem(app.config['UPLOAD_PATH_PDF']+ file.filename)
                    #data = msg.Body
                    #os.system('cd /home/sanam/Test ; msgconvert chunmun.msg')
                    print('cd '+app.config['UPLOAD_PATH_PDF']+'; '+'msgconvert '+file.filename)
                    os.system('cd '+app.config['UPLOAD_PATH_PDF']+'; '+'msgconvert '+file.filename )
                    with open(app.config['UPLOAD_PATH_PDF']+file.filename+'.eml',
                              'rb') as fp:  # select a specific email file from the list
                        msg = BytesParser(policy=policy.default).parse(fp)
                    data = msg.get_body(preferencelist=('plain')).get_content()
                    #print(text)  # print the email content

                    print(data)
                    temp = file.filename.replace(".msg", "")
                    html = "<html></html>"
                    soup = BeautifulSoup(html)
                    htmltag = soup.find('html')
                    body = soup.new_tag("body")
                    paras = data.split("\n\n")
                    for para in paras:
                        html = "<p></p>"
                        souppara = BeautifulSoup(html,features="lxml")
                        ptag = souppara.find('p')
                        ptag.insert(0, NavigableString(para))
                        body.append(ptag)
                    htmltag.append(body)
                    html_page = soup.prettify("utf-8")
                    with open(app.config['UPLOAD_PATH_PDF'] + temp + ".html", "wb+") as filewriter:
                        filewriter.write(html_page)
                    with open(app.config['UPLOAD_PATH_PDF'] + temp + ".txt", "w+") as filewriter:
                        print("Converting .msg into Text")
                        filewriter.write(data)
                        print("Converted .msg into Text")

                    document_url = "http://george.runmy.tech:5000/static/web/" + temp + ".html"
                    entityExtractor_ = EntityExtractor(lang,app.config['UPLOAD_PATH_PDF'] + temp+".txt", pname.strip("'"),document_url,app.config['GOOGLE_API_KEY'],app.config['NLP_API_KEY'],app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"],
                         app.config["DATABASE"],file.filename)
                    print("Stucked")
                    entityExtractor_.getEntityTxtJson()


                else:
                    temp = file.filename.replace(".pdf", "")
                    document_url = "http://george.runmy.tech:5000/static/web/viewer.html?file=" + file.filename
                    entityExtractor_ = EntityExtractor(lang,app.config['UPLOAD_PATH_PDF'] + file.filename,pname.strip("'"),document_url,app.config['GOOGLE_API_KEY'],app.config['NLP_API_KEY'],app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"],
                         app.config["DATABASE"],file.filename)
                    searchable = entityExtractor_.isSearchablePDF();
                    if(searchable):
                        entityExtractor_.getEntityPDFJson()
                    else:
                        # OCR
                        print("Have to do OCR")

                        document_url = "http://george.runmy.tech:5000/static/web/viewer.html?file=" + file.filename
                        OCR.pdf_splitter(app.config['UPLOAD_PATH_PDF'] + filename, app.config['UPLOAD_PATH_PDF'] + temp+".txt", app.config['OCR_API_KEY'])
                        entityExtractor_ = EntityExtractor(lang,app.config['UPLOAD_PATH_PDF'] + temp + ".txt",pname.strip("'"), document_url,app.config['GOOGLE_API_KEY'],app.config['NLP_API_KEY'],app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"],
                         app.config["DATABASE"],file.filename)
                        entityExtractor_.getEntityTxtJson()

                print(entityExtractor_.getEntities())
                print("some stuff")
                args = (file.filename, pname.strip("'"), session['user'].strip("'"), formatted_date.strip("'"),
                        app.config['UPLOAD_PATH_PDF'],entityExtractor_.getNodesList(),entityExtractor_.getEdgeList(),entityExtractor_.getEntities(),document_url)

                if(entityExtractor_ !=None):
                    del entityExtractor_

                    # Execute the SQL command
                cur.execute(sql, args)
                # Commit your changes in the database
                db.commit()

                # return redirect(url_for('success', n=str(email)))
                # session['user']=email
                db.close()
                return render_template('addfiles.html', email=session['user'],projectList=session['projectList'],message="File is successfully uploaded and processed")
            else:
                return render_template('addfiles.html',email=session['user'],projectList=session['projectList'],
                                        message='File Extension not allowed')

    except Exception as e:
        print("Error is here soooooooooo" + str(e))
        print(''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)))
        return render_template('addfiles.html', projectList=session['projectList'],email=session['user'],message='Exception in file processing')



@app.route('/showFiles', methods=['POST', 'GET'])
def showFiles():
    print("In show Files")
    DBHandler_ = DBHandler(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"],
                           app.config["DATABASE"])
    pname = request.args.get("pname")
    print("Project:",pname)
    projectFileList = DBHandler_.getProjectFiles(session['user'],pname)
    return jsonify(projectFileList)


@app.route('/showUsers', methods=['POST', 'GET'])
def showUsers():
    print("In show Files")
    DBHandler_ = DBHandler(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"],
                           app.config["DATABASE"])
    pname = request.args.get("pname")
    print("Project:",pname)
    projectUsersList = DBHandler_.getProjectUsers(pname)
    return jsonify(projectUsersList)

@app.route('/addUser', methods=['POST', 'GET'])
def addUser():
    print("in Add User")
    datetime_now = datetime.datetime.now();
    formatted_date = datetime_now.strftime('%Y-%m-%d %H:%M:%S')

    db = pymysql.connect(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"],
                         app.config["DATABASE"])
    cur = db.cursor()

    if request.method == 'POST':
        pname = request.form['pname']
        uname = request.form['uname']

    sql = 'INSERT INTO Project_USERS (ProjectName,UserName,UsersAddOn) VALUES (%s, %s ,%s)'

    args = (pname.strip("'"), uname.strip("'"),formatted_date.strip("'"))

    try:

        # Execute the SQL command
        cur.execute(sql, args)
        # Commit your changes in the database
        db.commit()


    except Exception as e:
        print(e)
        return render_template('adduser.html',projectList=session['projectList'], email=session['user'] ,error=e)
    finally:
        db.close()
    # return redirect(url_for('success', n=str(email)))
    #session['user']=email
    return render_template('adduser.html', projectList=session['projectList'],email=session['user'])



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'],
                               filename)


@app.route('/searchRelation', methods=['POST', 'GET'])
def searchRelation():
    Nodes = []
    Edges = []

    print("reached here")
    if request.method == 'POST':
        pname = request.form['pname']
        query = request.form['query']
        fname = request.form['fname']
    print(pname)
    print(query)
    print("fname",fname)
    entityRelationExtractor_ = EntityRelation(pname, query, app.config["DATABASEIP"], app.config["DB_USER"],
                                              app.config["DB_PASSWORD"],
                                              app.config["DATABASE"],fname)
    message = None
    try:
        if(fname != "" and query ==""  ):
            entityRelationExtractor_.allEntities()
        elif(fname =="" and query !=""):
            entityRelationExtractor_.entityRelation()
        elif(fname !="" and query !=""):
            entityRelationExtractor_.entityRelationOneFile()
        else:
            message = "Key word and File Name both are empty"
    except DBError as e:
        print (e)
        return render_template('search.html', projectList=session['projectList'], email=session['user'], nw=Nodes,
                               ne=Edges , message=message)
    except Exception as e:
        return render_template('search.html', projectList=session['projectList'], email=session['user'], nw=Nodes,
                               ne=Edges, message=message)


    Nodes = entityRelationExtractor_.getNodesList()
    Edges =  entityRelationExtractor_.getEdgeList()
    print(len(Nodes))
    print(len(Edges))
    if(entityRelationExtractor_ != None):
        del entityRelationExtractor_
    return render_template('search.html',projectList=session['projectList'],email=session['user'], nw=Nodes, ne=Edges)



@app.route('/uploader_', methods=['GET', 'POST'])
def upload_file_s():
    try:
        print("Here in uploader Two")
        file = request.files['file']
        pname = request.form['pname']
        print(file)
        print(pname)

        if request.method == 'POST':
            file = request.files['file']
            pname = request.form['pname']
            lang = request.form['lang']

            if file.filename == '':
                print("file name is empty")
                return redirect(url_for('addfiles.html',
                                        message='No selected file'))
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.filename.replace(" ","_")
                print("file",file.filename)

                file.save(os.path.join(app.config['UPLOAD_PATH_PDF'], file.filename))
                datetime_now = datetime.datetime.now();
                formatted_date = datetime_now.strftime('%Y-%m-%d')
                db = pymysql.connect(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"],
                                     app.config["DATABASE"])
                cur = db.cursor()
                args = (file.filename, pname.strip("'"), session['user'].strip("'"), formatted_date.strip("'"),
                        app.config['UPLOAD_PATH'],'N')

                sql = 'INSERT INTO Project_Files (FileName,ProjectName,ProjectUserID,Processed ,UploadDate,UploadPath) VALUES (%s,%s, %s ,%s,%s,%s)'
                cur.execute(sql, args)
                    # Commit your changes in the database
                return render_template('addfiles.html', email=session['user'],projectList=session['projectList'],message="File is successfully uploaded will be processed by File processor")

    except Exception as e:
        print("Error is here soooooooooo" + str(e))
        print(''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)))
        return render_template('addfiles.html', projectList=session['projectList'],email=session['user'],message='Exception in file processing')

    finally:
        db.commit()

        db.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0')





