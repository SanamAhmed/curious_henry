
from pycorenlp import *
import spacy
from collections import Counter


def splitCount(s, count):
    return [''.join(x) for x in zip(*[list(s[z::count]) for z in range(count)])]


nlp = spacy.load('en_core_web_sm')
from Entity import Entity

c= Counter('abracadabra')
source = c.most_common(3)
print(type(source[0]))
print(source[1][0])
src_path = "C:\\Users\\sanam\Desktop\\AttomusFiles\\"

nlp = StanfordCoreNLP("http://localhost:9000/")
GOOGLE_API_KEY = 'C:\\Users\\sanam\\Desktop\\AttomusFiles\\CuriousHenry-beta-5153a5857731.json'
line = "The Borrower and the Bank have herewith agreed that failing to resolve any disputes arising from the Agreement on the basis of good will the dispute shall be resolved by Harju County Court.This is "
print("sfjdhfjghsrthsejth")
print(splitCount(line,100))
output = nlp.annotate(line, properties={"annotators":"tokenize,ssplit,pos,depparse,natlog,openie",
                                 "outputFormat": "json",
                                 "openie.triple.strict": "true",
                                 "openie.max_entailments_per_clause": "1"})
if(output!=None):
    print(output)
    result = [output['sentences'][0]['openie'] for item in output]
    for i in result:
        for rel in i:
            relationSent=rel['subject'],rel['relation'],rel['object']
            print(relationSent)
else:
    print("Failed")




'''
mydic ={}
print(mydic.get("Aisk"))
mydic["Aisk"]="23"
print(mydic.get("Aisk"))

def extractentities(text):
    entities = []
    doc = nlp(text)

    for X in doc.ents:
        if X.text != ('\n') and X.label_ not in ('ORDINAL', 'CARDINAL', 'NORP', 'Non-­‐binding'):
            print(X.text,X.label_)
            entity_ = Entity(X.text,X.label_)
            entities.append(entity_)

    return entities
extractentities("Narva mnt 9A, Tallinn 10117 ")
'''
