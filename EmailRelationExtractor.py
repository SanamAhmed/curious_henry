from DBHandler import DBHandler
import re
import docx
import spacy
import Translator
from pycorenlp import *
import time
from RelationTriple import RelationTriple
nlp = spacy.load('en_core_web_sm')
import json
from Entity import Entity



class EmailRelationExtractor(object):

    def __init__(self, lang, filename, projectName,document_url ,fname,from_,to_,subject_):
        with open('configurations.json') as f:
            data = json.load(f)
        self.lang = lang
        self.filename = filename
        self.document_url = document_url
        self.projectName = projectName
        self.credentials = data["GOOGLE_API_KEY"]
        self.StanfordNLPPath = data["NLP_API_KEY"]
        self.relationExtractor = StanfordCoreNLP(self.StanfordNLPPath)
        self.DATABASEIP = data["DATABASEIP"]
        self.DB_USER = data["DB_USER"]
        self.DB_PASSWORD = data["DB_PASSWORD"]
        self.DATABASE = data["DATABASE"]
        self.fname = fname
        self.from_ = from_
        self.to_ = to_
        self.subject_ = subject_
        self.uniqueEntities = []
    def __del__(self):
        print("destructor")

    def getEntityTxtJson(self):
        print("New Extractor for Txt file")
        f = open(self.filename, 'rb')
        data = f.read().decode('utf8', 'ignore')
        paragraphs = data.split("\n\n")
        relationsList = []

        relation = RelationTriple(self.from_, self.to_, self.subject_, self.document_url, self.fname, self.projectName)
        relationsList.append(relation)
        print("Number of Paragraphs"+str(len(paragraphs)))
        for para in paragraphs:
            if (self.lang not in "eng"):
                translatedPara = Translator.translate_(para, self.credentials)
                para = translatedPara
            self.extractentities(para)
            relations = self.extractrelation(para)
            for r in relations:
                relation = RelationTriple(r.getSubject_(), r.getObject_(), r.getRelation_(), self.document_url,
                                          self.fname,
                                          self.projectName)
                relation.source = self.from_
                relation.sourceSubject = self.subject_
                relationsList.append(relation)
                del relation

        for entity in self.uniqueEntities:
            relation = RelationTriple(entity.Text, "", "", self.document_url, self.fname, self.projectName)
            relation.source = self.from_
            relation.sourceSubject = self.subject_
            relationsList.append(relation)
            del relation


        dbHandler_ =DBHandler(self.DATABASEIP,self.DB_USER,self.DB_PASSWORD,self.DATABASE)
        dbHandler_.insertRelation(relationsList)
        dbHandler_.updateFileStatus(self.fname,"Y")
        return True





    def extractentities(self,text):
        entities = []
        doc = nlp(text)

        for X in doc.ents:
            if X.text != ('\n') and X.label_ not in ('ORDINAL', 'CARDINAL', 'NORP', 'Non-­‐binding'):
                print(X.text,X.label_)
                newEntity = Entity(X.text,X.label_)
                newEntity.Text = re.sub('[^A-Za-z0-9]+', '', newEntity.Text)
                print("Herejhgjhghghfg")
                if self.uniqueEntities != []:

                    for entity in self.uniqueEntities:
                        entity_ = re.sub('[^A-Za-z0-9]+', '', entity.Text)
                        if (newEntity.Text.lower() == entity_.lower() or newEntity.Text.lower().__contains__(
                                entity_.lower()) or entity_.lower().__contains__(newEntity.Text.lower())):
                            print("Entity duplicated",newEntity.Text)
                else:
                    print("Entity is going to be added")
                    self.uniqueEntities.append(newEntity)


    def extractrelation(self,text):
        relationsList = []
        text.replace("\n","")
        for line in text.split("."):
            output = self.relationExtractor.annotate(line, properties={
                "annotators": "tokenize,ssplit,pos,depparse,natlog,openie",
                "outputFormat": "json",
                "openie.triple.strict": "true",
                "openie.max_entailments_per_clause": "1"})
            if (output != None):
                if (len(output["sentences"]) > 0):
                    result = [output["sentences"][0]["openie"] for item in output]
                    # print(len(result))
                    for i in result:
                        for rel in i:
                            relationSent = rel['subject'], rel['relation'], rel['object']
                            print(relationSent)
                            relation = RelationTriple(rel['subject'], rel['object'], rel['relation'],
                                                      self.document_url,self.fname,self.projectName)
                            relationsList.append(relation)
                            del relation

        return relationsList
    '''
    def updaterelations(self,entities):
        updatedrelations = []
        person = self.getPersonEntity(entities)
        organization = self.getOrgEntity(entities)
        if person != None:
            for entity in entities:
                if entity.Label in "LOC" or entity.Label in "GPE":
                    print("here")
                    print("here")
                    relation = RelationTriple(person.Text, entity.Text, "works at",
                                              self.document_url, self.fname, self.projectName)
                    updatedrelations.append(relation)
        elif organization != None:
            for entity in entities:
                if entity.Label in "LOC" or entity.Label in "GPE":
                    print("bjdfbgjd")
                    relation = RelationTriple(organization.Text, entity.Text, "is located ",
                                              self.document_url, self.fname, self.projectName)

                    updatedrelations.append(relation)


        return updatedrelations
    '''

    def getPersonEntity(self,entities):
        for entity in entities:
            if entity.Label =="PERSON":
                return entity
        return None

    def getOrgEntity(self,entities):
        for entity in entities:
            if entity.Label =="ORG":
                return entity
        return None




