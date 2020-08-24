import pymysql
import json
from DBError import DBError
import datetime
from ProjectFile import ProjectFile
import traceback
from Entity import Entity
from collections import OrderedDict
from pymysql.cursors import DictCursorMixin, Cursor


class DBHandler:



    def __init__(self,DATABASEIP , DB_USER , DB_PASSWORD , DATABASE):
        self.DATABASEIP = DATABASEIP
        self.DB_USER = DB_USER
        self.DB_PASSWORD = DB_PASSWORD
        self.DATABASE = DATABASE
    def  __del__(self):
        print("Destructor")

    def getProjectList(self,user):
        db = pymysql.connect(self.DATABASEIP, self.DB_USER, self.DB_PASSWORD,self.DATABASE)
        cur = db.cursor()

        error = None
        projectList = []
        try:
            sql = 'SELECT  ProjectName  FROM project_users WHERE UserName = %s'

            args = (user)

            cur.execute(sql, args)
            projectList = []
            for row in cur.fetchall():
                projectList.append(row[0])

            print(user)
            print(projectList)
        except Exception as e:
            error = str(e)
            raise DBError('Did not get any Projects'+error)
            print("In DB Handler",error)
        finally:
            db.close()
        return projectList

    def getProjectJSON(self,user):
        print("In DB Handler")
        db = pymysql.connect(self.DATABASEIP, self.DB_USER, self.DB_PASSWORD,self.DATABASE)
        cur = db.cursor()

        error = None
        projectList = []
        try:
            print("One")
            sql = 'SELECT  projects.ProjectName ,projects.ProjectDesc,projects.ProjectOwner,projects.ProjectCreateDate  FROM project_users , projects WHERE projects.ProjectName=project_users.ProjectName and UserName = %s'

            args = (user)
            print("two")
            print(sql)
            cur.execute(sql, args)
            print(sql)
            print("three")
            for row in cur.fetchall():
                print("four")
                project = []
                project.append(row[0])
                project.append(row[1])
                project.append(row[2])
                project.append(str(row[3]))
                projectList.append(project)

            print(user)
            print(projectList)
        except Exception as e:
            error = str(e)
            raise DBError('Did not get any Projects'+error)
            print("In DB Handler",error)
        finally:
            db.close()
        print(projectList)
        return json.dumps(projectList)



    def getProjectFiles(self,user ,project):
        print("In DB Handler")
        db = pymysql.connect(self.DATABASEIP, self.DB_USER, self.DB_PASSWORD,self.DATABASE)
        cur = db.cursor(pymysql.cursors.DictCursor)

        error = None
        projectFilesList = []
        try:
            print("One")
            sql = 'SELECT  FileName ,Processed,UploadDate  FROM project_files  WHERE ProjectName = %s and ProjectUserID = %s and Lang <> %s ORDER BY %s %s '

            args = (project , user ,"eng","FileID","DESC")
            print("two")
            print(sql)
            cur.execute(sql, args)
            print(sql)
            print("three")
            for row in cur.fetchall():
                print("four")
                file = []
                file.append(row["FileName"])
                file.append(row["Processed"])
                file.append(str(row["UploadDate"]))
                projectFilesList.append(file)

            print(user)
            print(projectFilesList)
        except Exception as e:
            error = str(e)
            raise DBError('Did not get any Files'+error)
            print("In DB Handler",error)
        finally:
            db.close()
        print(projectFilesList)
        return projectFilesList

    def getProjectUsers(self,project):
        print("In DB Handler")
        db = pymysql.connect(self.DATABASEIP, self.DB_USER, self.DB_PASSWORD,self.DATABASE)
        cur = db.cursor()

        error = None
        usersList = []
        try:
            print("One")
            sql = 'SELECT  UserName  FROM project_users WHERE ProjectName = %s '

            args = (project)
            print("two")
            print(sql)
            cur.execute(sql, args)
            print(sql)
            print("three")
            for row in cur.fetchall():
                print("four")
                user = []
                user.append(row[0])

                usersList.append(user)


            print(usersList)
        except Exception as e:
            error = str(e)
            raise DBError('Did not get any Users'+error)
            print("In DB Handler",error)
        finally:
            db.close()
        print(usersList)
        return usersList

    def createProject(self,pname,pDesc,user):
        print("In DB Handler")
        inserted = True
        datetime_now = datetime.datetime.now();
        formatted_date = datetime_now.strftime('%Y-%m-%d')

        db = pymysql.connect(self.DATABASEIP, self.DB_USER, self.DB_PASSWORD,self.DATABASE)
        cur = db.cursor()

        error = None
        usersList = []
        try:
            print("One")
            sql = 'INSERT INTO projects (ProjectName,ProjectDesc,ProjectOwner,ProjectCreateDate) VALUES (%s, %s ,%s,%s)'

            args = (pname, pDesc,user ,formatted_date)

            sql2 = 'INSERT INTO project_users (ProjectName,UserName,UsersAddOn) VALUES (%s, %s ,%s)'
            args_2 = (pname,user,formatted_date)


            print("two")
            print(sql)
            cur.execute(sql, args)
            cur.execute(sql2, args_2)
            db.commit()


            # Commit your changes in the database

        except Exception as e:
            error = str(e)
            raise DBError('Can not create Project'+error)
            print("In DB Handler",error)
        finally:

            db.close()
        print(usersList)



    def insertRelation(self, relationList):
        print ("inserting relations in db")
        db = None
        try:

            db = pymysql.connect(self.DATABASEIP, self.DB_USER, self.DB_PASSWORD,
                                 self.DATABASE)
            cur = db.cursor()

            sql = 'INSERT INTO relations (ProjectName ,FileName,DocumentURL ,Subject , Object,Relation ,Source,sourceRelation  ) VALUES (%s, %s,%s,%s,%s,%s,%s,%s)'

            for relation in relationList:
                if(isinstance(relation,Entity)):
                    print("It is Entity")
                else:
                    print("It is Relation")



                args = (relation.pname, relation.filename, relation.url, relation.getSubject_(), relation.getObject_(),
                        relation.getRelation_(),relation.getSource(),relation.getSourceSbject())

                # Execute the SQL command
                print(args)
                cur.execute(sql, args)

        except Exception as error:
            traceback.print_exc()

            raise DBError('Can not insert File  Data into DB ' + str(error))
            print("In DB Handler storing file Data", error)
            traceback.print_exc()

        finally:
            if (db != None):
                db.commit()
                db.close()

    def insertFiles(self,projectFile):
        print ("insert file data into DB")
        db = None
        cur = None
        try:
            db = pymysql.connect(self.DATABASEIP, self.DB_USER, self.DB_PASSWORD,self.DATABASE)
            cur = db.cursor()
            args = (projectFile.FileName, projectFile.ProjectName, projectFile.ProjectUserID, projectFile.UploadDate,projectFile.UploadPath, projectFile.Processed , projectFile.lang)
            print
            sql = 'INSERT INTO project_files (FileName,ProjectName,ProjectUserID,UploadDate,UploadPath,Processed,Lang) VALUES (%s,%s, %s ,%s,%s,%s,%s)'
            cur.execute(sql, args)
        except Exception as error:
            raise DBError('Can not insert File  Data into DB ' + str(error))
            print("In DB Handler storing file Data", error)
        finally:
            if(db !=None):
                db.commit()
                db.close()

    def getFilesToProcess(self):
        db = None
        cur = None
        filesList =[]
        try:
            db = pymysql.connect(self.DATABASEIP, self.DB_USER, self.DB_PASSWORD,self.DATABASE)
            cur = db.cursor()
            processed = "N"
            args = (processed)
            sql = 'Select FileName,ProjectName,ProjectUserID,Processed,UploadDate,UploadPath,Lang , FileID from project_files where Processed = %s'
            cur.execute(sql, args)

            for row in cur.fetchall():
               ProjectFile_ = ProjectFile(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
               ProjectFile_.setFileID(row[7])
               filesList.append(ProjectFile_)
               del ProjectFile_

        except Exception as error:
            raise DBError('Can not insert File  Data into DB ' + str(error))
            print("In DB Handler storing file Data", error)
        finally:
            if(db !=None):
                db.close()
        return filesList

    def updateFileStatus(self,fileName,processed):
        print("insert file data into DB")
        db = None
        cur = None
        try:
            db = pymysql.connect(self.DATABASEIP, self.DB_USER, self.DB_PASSWORD, self.DATABASE)
            cur = db.cursor()
            args = (processed,fileName)
            sql = 'update project_files set Processed=%s where FileName=%s'
            cur.execute(sql, args)
        except Exception as error:
            raise DBError('Can not update File  status into DB ' + str(error))
            print("In DB Handler storing file Data", error)
        finally:
            if (db != None):
                db.commit()
                db.close()
















