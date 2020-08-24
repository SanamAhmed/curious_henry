
from pycorenlp import *
import win32com.client
from docx import Document
import os
src_path = "C:\\Users\\sanam\Desktop\\AttomusFiles\\"
print("Hello")
import Translator
#outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
#msg = outlook.OpenSharedItem(r"C:\Users\sanam\Desktop\AttomusFiles\Test.msg")
#text1 = msg.Body
nlp = StanfordCoreNLP("http://localhost:9000/")
GOOGLE_API_KEY = 'C:\\Users\\sanam\\Desktop\\AttomusFiles\\CuriousHenry-beta-5153a5857731.json'

with open("C:\\Users\\sanam\\Desktop\\AttomusFiles\\Erastamise_leping_EV.txt", "r") as myfile:
    data = myfile.read()
    #data=Translator.translate_(data,GOOGLE_API_KEY)
paras = data.split("\n\n")
for p in paras:


    for line in p.split("\n"):
        line = Translator.translate_(line,GOOGLE_API_KEY)
        output = nlp.annotate(line, properties={"annotators":"tokenize,ssplit,pos,depparse,natlog,openie",
                                         "outputFormat": "json",
                                         "openie.triple.strict": "true",
                                         "openie.max_entailments_per_clause": "3"})
        if(output!=None):
            if(len(output["sentences"])>0):
                result = [output["sentences"][0]["openie"] for item in output]
                #print(len(result))
                for i in result:
                    for rel in i:
                        relationSent=rel['subject'],rel['relation'],rel['object']
                        print(relationSent)

for line in text1.split("\n"):
    output = nlp.annotate(line, properties={"annotators":"tokenize,ssplit,pos,depparse,natlog,openie",
                                     "outputFormat": "json",
                                     "openie.triple.strict": "true",
                                     "openie.max_entailments_per_clause": "1"})
    if(output!=None):
        if(len(output["sentences"])>0):
            result = [output["sentences"][0]["openie"] for item in output]
            #print(len(result))
            for i in result:
                for rel in i:
                    relationSent=rel['subject'],rel['relation'],rel['object']
                    print(relationSent)