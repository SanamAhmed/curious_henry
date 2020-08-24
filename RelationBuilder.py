import pymysql
import json
import string
from RelationTriple import RelationTriple
class RelationBuilder:
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
        #sql = 'SELECT  FileName,FileEntities FROM project_files WHERE ProjectName = %s and FileEntities like %'+'%s'+'%'
        sql_template_1 = string.Template("""
                SELECT  Subject,Object,Relation,DocumentURL,Source,sourceRelation FROM relations WHERE ProjectName = '$pname' and (Subject LIKE '%$query%' or Object LIKE '%$query%' or Relation LIKE '%$query%' or Source LIKE '%$query%' or sourceRelation LIKE '%$query%')  LIMIT 100
                """)
        sql_1 = sql_template_1.substitute(pname=self.projectName, query=self.searchTerm)
        # sql_template =
        print(sql_1)
        cur.execute(sql_1)
        relationList =[]
        counter =1
        sourceNodes = {}
        Nodes ={}
        for row in cur.fetchall():
            relation = RelationTriple(row[0],row[1],row[2],row[3],"","")
            relation.source = row[4]
            relation.sourceSubject = row[5]
            relationList.append(relation)
            del relation
        print("Number of relations:"+str(len(row)))
        try:
            for rel in relationList:
                from_ = str(counter)
                if(Nodes.get(rel.getSubject_()) == None):
                    counter = counter+1
                    from_ = str(counter)
                    mydicobg_s = {"id": str(counter), "label": rel.getSubject_(),"title": rel.getSubject_(),
                          "url": rel.getURL()}
                    self.nodesList.append(mydicobg_s)
                    Nodes[rel.getSubject_()]=str(counter)
                elif(Nodes.get(rel.getSubject_()) != None):
                    print("Skiiped Redrawing")
                    from_ = Nodes.get(rel.getSubject_())
                if(rel.getObject_()!=""):
                    if (Nodes.get(rel.getObject_()) == None):

                        counter = counter + 1
                        mydicobg_o = {"id": str(counter), "label": rel.getObject_(),"title": rel.getObject_(),
                                  "url": rel.getURL()}
                        to_ = str(counter)
                        self.nodesList.append(mydicobg_o)

                    else:
                        print("Entity Object is skipped")
                        to_ = Nodes.get(rel.getObject_())

                    myedge = {"from": from_, "to": to_, "label": rel.getRelation_() ,"title": rel.getRelation_(),"widthConstraint": { "minimum": 150 }}
                    self.edgesList.append(myedge)
                if (sourceNodes.get(rel.source)==None and rel.source!=""):
                    counter = counter + 1
                    mydicobg_source = {"id": str(counter), "label": rel.source, "title": rel.source,
                                       "url": rel.getURL()}
                    sourceNodes[rel.source] = str(counter)
                    self.nodesList.append(mydicobg_source)
                if(rel.source!=""):
                    toSource = sourceNodes.get(rel.source)
                    if(toSource!=None):
                        myedge_ = {"from": from_, "to": toSource, "label": rel.sourceSubject, "title": rel.source,
                                  "widthConstraint": {"minimum": 150}}
                        self.edgesList.append(myedge_)
                #counter = counter + 1
        except Exception as e:
            print("Error is here"+str(e))
        print("I am here in RelationBuider")
        print(len(self.nodesList))
        print(len(self.edgesList))

    def allRelation(self):
        print("Here in all jfsjhfshfg")
        print("showing all relation of File")
        db = pymysql.connect(self.DATABASEIP, self.DB_USER,self.DB_PASSWORD,
                             self.DATABASE)
        cur = db.cursor()
        #sql = 'SELECT  FileName,FileEntities FROM project_files WHERE ProjectName = %s and FileEntities like %'+'%s'+'%'
        sql_template_1 = string.Template("""
                SELECT  Subject,Object,Relation,DocumentURL,Source,sourceRelation FROM relations WHERE ProjectName = '$pname' and  FileName = '$fname'
                """)
        sql_1 = sql_template_1.substitute(pname=self.projectName, fname=self.fname)
        # sql_template =
        print(sql_1)
        cur.execute(sql_1)
        relationList =[]
        counter =1
        sourceNodes = {}
        Nodes ={}
        for row in cur.fetchall():
            relation = RelationTriple(row[0],row[1],row[2],row[3],"","")
            relation.source = row[4]
            relation.sourceSubject = row[5]
            relationList.append(relation)
            del relation
        print("Number of relations:"+str(len(row)))
        try:
            for rel in relationList:
                from_ = str(counter)
                if(Nodes.get(rel.getSubject_()) == None):
                    counter = counter+1
                    from_ = str(counter)
                    mydicobg_s = {"id": str(counter), "label": rel.getSubject_(),"title": rel.getSubject_(),
                          "url": rel.getURL()}
                    self.nodesList.append(mydicobg_s)
                    Nodes[rel.getSubject_()]=str(counter)
                elif(Nodes.get(rel.getSubject_()) != None):
                    from_ = Nodes.get(rel.getSubject_())
                if(rel.getObject_()!=""):
                    if (Nodes.get(rel.getObject_()) == None):
                        counter = counter + 1
                        mydicobg_o = {"id": str(counter), "label": rel.getObject_(),"title": rel.getObject_(),
                                  "url": rel.getURL()}
                        to_ = str(counter)
                        self.nodesList.append(mydicobg_o)

                    else:
                        print("Entity Object is skipped")
                        to_ = Nodes.get(rel.getObject_())

                    myedge = {"from": from_, "to": to_, "label": rel.getRelation_() ,"title": rel.getRelation_(),"widthConstraint": { "minimum": 150 }}
                    self.edgesList.append(myedge)

                if (sourceNodes.get(rel.source)==None and rel.source!=""):
                    counter = counter + 1
                    mydicobg_source = {"id": str(counter), "label": rel.source, "title": rel.source,
                                       "url": rel.getURL()}
                    sourceNodes[rel.source] = str(counter)
                    self.nodesList.append(mydicobg_source)
                if(rel.source!=""):
                    toSource = sourceNodes.get(rel.source)
                    if(toSource!=None):
                        myedge_ = {"from": from_, "to": toSource, "label": rel.sourceSubject, "title": rel.source,
                                  "widthConstraint": {"minimum": 150}}
                        self.edgesList.append(myedge_)
                #counter = counter + 1
        except Exception as e:
            print("Error is here"+str(e))
        print("I am here in RelationBuider")
        print(len(self.nodesList))
        print(len(self.edgesList))


    def getNodesList(self):
        print("This is the point")
        print(self.nodesList)
        return json.dumps(self.nodesList)

    def getEdgeList(self):
        print("gfgdfgdfgsd")
        print(self.edgesList)
        return json.dumps(self.edgesList)



def replace_str_index(text,index=0,replacement=''):
    return '%s%s%s'%(text[:index],replacement,text[index+1:])