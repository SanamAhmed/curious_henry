

class RelationTriple(object):
    subject_ = ""
    object_ = ""
    relation_ = ""
    url = ""


    def __init__(self,subject_,object_,relation_,url,fname,pname):
        self.subject_ = subject_
        self.object_ = object_
        self.relation_ = relation_
        self.url = url
        self.filename = fname
        self.pname = pname
        self.source = ""
        self.sourceSubject =""


    def getSubject_(self):
        return self.subject_

    def getSource(self):
        return self.source

    def getSourceSbject(self):
        return self.sourceSubject


    def getSubject_(self):
        return self.subject_

    def getObject_(self):
        return self.object_
    def getRelation_(self):
        return self.relation_
    def getURL(self):
        return self.url




