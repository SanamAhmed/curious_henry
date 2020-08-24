import pymysql
import json
import string
from RelationTriple import RelationTriple
class EntityRelation:
    def __init__(self,projectName ,searchTerm,DATABASEIP,DB_USER,DB_PASSWORD,DATABASE , fname):
        self.projectName = projectName
        self.searchTerm = searchTerm
        self.DATABASEIP = DATABASEIP
        self.DB_USER = DB_USER
        self.DB_PASSWORD = DB_PASSWORD
        self.DATABASE = DATABASE
        self.nodesList = []
        self.edgesList = []
        self.fname = fname

    def __del__(self):
        print ("destructor")



    def entityRelation(self):
        db = pymysql.connect(self.DATABASEIP, self.DB_USER,self.DB_PASSWORD,
                             self.DATABASE)
        cur = db.cursor()
        sql_template = string.Template("""
                SELECT  FileName,FileEntities,URL FROM project_files WHERE ProjectName = '$pname' and FileEntities LIKE '%$query%'
                """)
        sql = sql_template.substitute(pname=self.projectName, query=self.searchTerm)
        # sql_template =
        print(sql)

        # args = (self.projectName)
        cur.execute(sql)
        fileNamesList = []
        URLList = []
        entities = []
        for row in cur.fetchall():
            print(row[0])
            print(row[1])
            fileNamesList.append(row[0])
            entities.append(row[1])
            URLList.append(row[2])

        counter = 1
        print(type(fileNamesList))
        print(type(entities))
        print(len(fileNamesList))
        print(len(entities))
        zippedList = zip(fileNamesList, entities, URLList)
        groupCounter = 0
        for filename_, entities_, myurl in zippedList:
            list_ = entities_.split(",")
            myset = set(list_)

            print(len(list_))
            nodeIdList = []
            for value in myset:
                label_ = value
                id_ = counter
                from_ = str(counter)
                to_ = str(counter + 1)
                label_edge = "related"
                myedge = {"from": from_, "to": to_, "label": label_edge ,"title":label_edge}
                mydicobg = {"id": str(id_), "label": label_, "group": str(groupCounter), "title": label_ ,"url":myurl}
                self.nodesList.append(mydicobg)
                self.edgesList.append(myedge)
                counter = counter + 1
                if (self.searchTerm in label_):
                    nodeIdList.append(id_)

            groupCounter = groupCounter + 1
            listiter = 0;
            print("jhsgfjhsfgashfg")
            print(nodeIdList)
            for id in nodeIdList:
                if (listiter + 1 <= (len(nodeIdList) - 1)):
                    print(listiter)
                    print(listiter + 1)
                    print(nodeIdList[listiter])
                    myedge = {"from": str(nodeIdList[listiter]), "to": str(nodeIdList[listiter + 1]),
                              "label": "RELATED"}
                else:
                    break
                listiter = listiter + 1

        #sql = 'SELECT  FileName,FileEntities FROM project_files WHERE ProjectName = %s and FileEntities like %'+'%s'+'%'
        sql_template_1 = string.Template("""
                SELECT  Subject,Object,Relation,DocumentURL FROM relations WHERE ProjectName = '$pname' and Subject LIKE '%$query%' or Object LIKE '%$query%' or Relation LIKE '%$query%' LIMIT 100
                """)
        sql_1 = sql_template_1.substitute(pname=self.projectName, query=self.searchTerm)
        # sql_template =
        print(sql_1)
        cur.execute(sql_1)
        relationList =[]
        for row in cur.fetchall():
            relation = RelationTriple(row[0],row[1],row[2],row[3],"","")
            relationList.append(relation)
            del relation
        for rel in relationList:
            from_ = str(counter)
            #mydicobg_s = '{"id":' + str(counter) + ', "label":"' + rel.getSubject_() + '","url":"' + rel.getURL() + '"}'
            #mydicobg_s = '{"id":' + str(counter) + ',"label":' + rel.getSubject_() + ',"url":' + rel.getURL() + '}'
            mydicobg_s = {"id": str(counter), "label": rel.getSubject_(),"title": rel.getSubject_(),
                          "url": rel.getURL()}
            #
            print(mydicobg_s)

            mydicobg_o = None
            if(rel.getObject_()!=""):
                counter = counter + 1
                mydicobg_o = {"id": str(counter), "label": rel.getObject_(),"title": rel.getObject_(),
                          "url": rel.getURL()}
               # mydicobg_o = {"id":' + str(counter) + ', "label":' + rel.getObject_() + ',"url":' +rel.getURL() + '}

            #label_edge = self.filename
            to_ = str(counter)
            myedge = {"from": from_, "to": to_, "label": rel.getRelation_() ,"title": rel.getRelation_(),"widthConstraint": { "minimum": 150 }}
            #myedge = '{"from":'+ from_+', "to": '+to_+', "label":'+ rel.getRelation_()+'}'
            myedge_ = {"from": to_, "to": counter + 1, "label": "", "widthConstraint": 100}

            self.nodesList.append(mydicobg_s)
            if(mydicobg_o!=None):
                self.nodesList.append(mydicobg_o)
            self.edgesList.append(myedge)
            self.edgesList.append(myedge_)

            counter = counter + 1

    def entityRelationOneFile(self):
        db = pymysql.connect(self.DATABASEIP, self.DB_USER, self.DB_PASSWORD,
                             self.DATABASE)
        cur = db.cursor()
        # sql = 'SELECT  FileName,FileEntities FROM project_files WHERE ProjectName = %s and FileEntities like %'+'%s'+'%'
        sql_template_1 = string.Template("""
                SELECT  Subject,Object,Relation,DocumentURL FROM relations WHERE ProjectName = '$pname' and FileName='$fname' and Subject LIKE '%$query%' or Object LIKE '%$query%' or Relation LIKE '%$query%' LIMIT 100
                """)
        sql_1 = sql_template_1.substitute(pname=self.projectName, query=self.searchTerm ,fname=self.fname)
        # sql_template =
        print(sql_1)
        cur.execute(sql_1)
        relationList = []
        for row in cur.fetchall():
            relation = RelationTriple(row[0], row[1], row[2], row[3],"","")
            relationList.append(relation)
            del relation
        counter = 1
        for rel in relationList:
            from_ = str(counter)
            # mydicobg_s = '{"id":' + str(counter) + ', "label":"' + rel.getSubject_() + '","url":"' + rel.getURL() + '"}'
            # mydicobg_s = '{"id":' + str(counter) + ',"label":' + rel.getSubject_() + ',"url":' + rel.getURL() + '}'
            mydicobg_s = {"id": str(counter), "label": rel.getSubject_(),"title": rel.getSubject_(),
                          "url": rel.getURL()}
            #
            print(mydicobg_s)

            mydicobg_o = None
            if (rel.getObject_() != ""):
                counter = counter + 1
                mydicobg_o = {"id": str(counter), "label": rel.getObject_(),"title": rel.getObject_(),
                              "url": rel.getURL()}
            # mydicobg_o = {"id":' + str(counter) + ', "label":' + rel.getObject_() + ',"url":' +rel.getURL() + '}

            # label_edge = self.filename
            to_ = str(counter)
            myedge = {"from": from_, "to": to_, "label": rel.getRelation_(),"title": rel.getRelation_(), "widthConstraint": 100}
            myedge_ = {"from": to_, "to": counter + 1, "label": "", "widthConstraint": 100}



            self.nodesList.append(mydicobg_s)
            if (mydicobg_o != None):
                self.nodesList.append(mydicobg_o)
            self.edgesList.append(myedge)
            self.edgesList.append(myedge_)

            counter = counter + 1

    def allEntities(self):
        db = pymysql.connect(self.DATABASEIP, self.DB_USER,self.DB_PASSWORD,
                             self.DATABASE)
        cur = db.cursor()
        sql_template = string.Template("""
                        SELECT  FileName,FileEntities,URL FROM project_files WHERE ProjectName = '$pname' and FileName = '$fname'
                        """)
        sql = sql_template.substitute(pname=self.projectName, fname=self.fname)
        # sql_template =
        print(sql)

        # args = (self.projectName)
        cur.execute(sql)
        fileNamesList = []
        URLList = []
        entities = []
        for row in cur.fetchall():
            print(row[0])
            print(row[1])
            fileNamesList.append(row[0])
            entities.append(row[1])
            URLList.append(row[2])

        counter = 1
        print(type(fileNamesList))
        print(type(entities))
        print(len(fileNamesList))
        print(len(entities))
        zippedList = zip(fileNamesList, entities, URLList)
        groupCounter = 0
        for filename_, entities_, myurl in zippedList:
            list_ = entities_.split(",")
            myset = set(list_)

            print(len(list_))
            nodeIdList = []
            for value in myset:
                label_ = value
                id_ = counter
                from_ = str(counter)
                to_ = str(counter + 1)
                label_edge = "related"
                myedge = {"from": from_, "to": to_, "label": label_edge, "title": label_edge}
                mydicobg = {"id": str(id_), "label": label_, "group": str(groupCounter), "title": label_, "url": myurl}
                self.nodesList.append(mydicobg)
                self.edgesList.append(myedge)
                counter = counter + 1
                if (self.searchTerm in label_):
                    nodeIdList.append(id_)

            groupCounter = groupCounter + 1
            listiter = 0;
            print("jhsgfjhsfgashfg")
            print(nodeIdList)
            for id in nodeIdList:
                if (listiter + 1 <= (len(nodeIdList) - 1)):
                    print(listiter)
                    print(listiter + 1)
                    print(nodeIdList[listiter])
                    myedge = {"from": str(nodeIdList[listiter]), "to": str(nodeIdList[listiter + 1]),
                              "label": "RELATED"}
                else:
                    break
                listiter = listiter + 1

        # sql = 'SELECT  FileName,FileEntities FROM project_files WHERE ProjectName = %s and FileEntities like %'+'%s'+'%'
        sql_template_1 = string.Template("""
                        SELECT  Subject,Object,Relation,DocumentURL FROM relations WHERE ProjectName = '$pname' and  FileName ='$fname' LIMIT 100
                        """)
        sql_1 = sql_template_1.substitute(pname=self.projectName, fname=self.fname)
        # sql_template =
        print(sql_1)
        cur.execute(sql_1)
        relationList = []
        for row in cur.fetchall():
            relation = RelationTriple(row[0], row[1], row[2], row[3],"","")
            relationList.append(relation)
            del relation
        for rel in relationList:
            from_ = str(counter)
            # mydicobg_s = '{"id":' + str(counter) + ', "label":"' + rel.getSubject_() + '","url":"' + rel.getURL() + '"}'
            # mydicobg_s = '{"id":' + str(counter) + ',"label":' + rel.getSubject_() + ',"url":' + rel.getURL() + '}'
            mydicobg_s = {"id": str(counter), "label": rel.getSubject_(), "title": rel.getSubject_(),
                          "url": rel.getURL()}
            #
            print(mydicobg_s)

            mydicobg_o = None
            if (rel.getObject_() != ""):
                counter = counter + 1
                mydicobg_o = {"id": str(counter), "label": rel.getObject_(), "title": rel.getObject_(),
                              "url": rel.getURL()}
            # mydicobg_o = {"id":' + str(counter) + ', "label":' + rel.getObject_() + ',"url":' +rel.getURL() + '}

            # label_edge = self.filename
            to_ = str(counter)
            myedge = {"from": from_, "to": to_, "label": rel.getRelation_(), "title": rel.getRelation_(),
                      "widthConstraint": {"minimum": 150}}
            # myedge = '{"from":'+ from_+', "to": '+to_+', "label":'+ rel.getRelation_()+'}'
            myedge_ = {"from": to_, "to": counter + 1, "label": "", "widthConstraint": 100}

            self.nodesList.append(mydicobg_s)
            if (mydicobg_o != None):
                self.nodesList.append(mydicobg_o)
            self.edgesList.append(myedge)
            self.edgesList.append(myedge_)

            counter = counter + 1




    def getNodesList(self):
        print("THIS is the point")
        print(self.nodesList)
        return json.dumps(self.nodesList)

    def getEdgeList(self):
        print("gfgdfgdfgsd")
        print(self.edgesList)
        return json.dumps(self.edgesList)



def replace_str_index(text,index=0,replacement=''):
    return '%s%s%s'%(text[:index],replacement,text[index+1:])