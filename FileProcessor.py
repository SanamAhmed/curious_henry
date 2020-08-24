import mammoth
from EntityExtractor import EntityExtractor
from bs4 import BeautifulSoup,NavigableString
import OCR
import json
import os
from email import policy
from email.parser import BytesParser,Parser
from ProjectFile import ProjectFile
from EntityAndRelationBuilder import EntityAndRelationBuilder
from EmailRelationExtractor import EmailRelationExtractor
#import pythoncom
#import win32com
#import win32com.client
import  Translator
import time

class FileProcessor:

    def __init__(self):
        with open('configurations.json') as f:
            data = json.load(f)
        self.uploadurl = data["UPLOAD_URL"]
        self.uploadpath = data["UPLOAD_PATH_PDF"]
        self.googleapikey = data["GOOGLE_API_KEY"]
        self.nlpapikey = data["NLP_API_KEY"]
        self.ocrapikey = data["OCR_API_KEY"]
        self.dbip = data["DATABASEIP"]
        self.dbuser = data["DB_USER"]
        self.dbpassword = data["DB_PASSWORD"]
        self.dbname = data["DATABASE"]


    def __del__(self):
        print("File Processor Destructor")

    def process(self,projectFile_):
        entityExtractor_ = None
        document_url = None
        if (".docx" in projectFile_.FileName):
            with open(projectFile_.UploadPath + projectFile_.FileName, "rb") as docx_file:
                result = mammoth.convert_to_html(docx_file)
                html = result.value  # The generated HTML

            temp = projectFile_.FileName.replace(".docx", "")
            Html_file = open(projectFile_.UploadPath + temp + ".html", "w")
            Html_file.write(html)
            Html_file.write(html)
            Html_file.close()
            document_url = self.uploadurl + temp + ".html"
            title = self.extractTitle(projectFile_.UploadPath +temp + ".html",projectFile_.lang)
            print("Here in File Processor")
            print(self.uploadurl)
            print(document_url)
            entityExtractor_ = EntityAndRelationBuilder(projectFile_.lang, projectFile_.UploadPath+ projectFile_.FileName, projectFile_.ProjectName.strip("'"),
                                               document_url, projectFile_.FileName,title)
            entityExtractor_.getEntityDocxJson()

        elif (".txt" in projectFile_.FileName):
            temp = projectFile_.FileName.replace(".txt", "")
            data = ""
            html = "<html></html>"
            soup = BeautifulSoup(html)
            htmltag = soup.find('html')
            body = soup.new_tag("body")
            with open(projectFile_.UploadPath + projectFile_.FileName, "r") as myfile:
                data = myfile.read()
            print(data)
            paras = data.split("\n\n")
            for para in paras:
                html = "<p></p>"
                souppara = BeautifulSoup(html)
                ptag = souppara.find('p')
                ptag.insert(0, NavigableString(para))
                body.append(ptag)
            htmltag.append(body)
            html_page = soup.prettify("utf-8")
            with open(projectFile_.UploadPath + temp + ".html", "wb+") as filewriter:
                filewriter.write(html_page)
            document_url = self.uploadurl + temp + ".html"
            title = self.extractTitle(projectFile_.UploadPath + temp + ".html",projectFile_.lang)
            print("Language is:"+projectFile_.lang)
            entityExtractor_ = EntityAndRelationBuilder(projectFile_.lang, projectFile_.UploadPath+ projectFile_.FileName, projectFile_.ProjectName.strip("'"),
                                               document_url, projectFile_.FileName,title)
            entityExtractor_.getEntityTxtJson()
        elif (".msg" in projectFile_.FileName):
            '''            pythoncom.CoInitialize()
            outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
            temp = projectFile_.FileName.replace(".msg", "")

            msg = outlook.OpenSharedItem(projectFile_.UploadPath+ projectFile_.FileName)
            data = msg.Body
            '''
            print('cd ' + projectFile_.UploadPath + '; ' + 'msgconvert ' + projectFile_.FileName)
            os.system('cd ' + projectFile_.UploadPath + '; ' + 'msgconvert ' + projectFile_.FileName)
            with open(projectFile_.UploadPath + projectFile_.FileName + '.eml',
                      'rb') as fp:  # select a specific email file from the list
                msg = BytesParser(policy=policy.default).parse(fp)
            data = msg.get_body(preferencelist=('plain')).get_content()
            with open(projectFile_.UploadPath + projectFile_.FileName + '.eml',
                      'r+') as fhp:  # select a specific email file from the list
                headers = Parser().parse(fhp)
            print(headers["to"])
            print(headers["from"])
            print(headers["subject"])

            print(data)
            temp = projectFile_.FileName.replace(".msg.eml", "")
            html = "<html></html>"
            soup = BeautifulSoup(html)
            htmltag = soup.find('html')
            body = soup.new_tag("body")
            paras = data.split("\n\n")
            for para in paras:
                html = "<p></p>"
                souppara = BeautifulSoup(html, features="lxml")
                ptag = souppara.find('p')
                ptag.insert(0, NavigableString(para))
                body.append(ptag)
            htmltag.append(body)
            html_page = soup.prettify("utf-8")
            with open(projectFile_.UploadPath + temp + ".html", "wb+") as filewriter:
                filewriter.write(html_page)
            with open(projectFile_.UploadPath + temp + ".txt", "w+") as filewriter:
                print("Converting .msg into Text")
                filewriter.write(data)
                print("Converted .msg into Text")
            filename = projectFile_.UploadPath + temp + ".txt"
            document_url = self.uploadurl + temp + ".html"
            entityExtractor_ = EmailRelationExtractor(projectFile_.lang, filename, projectFile_.ProjectName.strip("'"),
                                               document_url, projectFile_.FileName,headers["to"],headers["from"],headers["subject"])
            print("Stucked")
            entityExtractor_.getEntityTxtJson()


        else:
            temp = projectFile_.FileName.replace(".pdf", "")
            title =""
            document_url = self.uploadurl+"viewer.html?file=" + projectFile_.FileName
            entityExtractor_ = EntityAndRelationBuilder(projectFile_.lang, projectFile_.UploadPath+ projectFile_.FileName, projectFile_.ProjectName.strip("'"),
                                               document_url, projectFile_.FileName,title)
            searchable = entityExtractor_.isSearchablePDF();
            if (searchable):
                entityExtractor_.getEntityPDFJson()
            else:
                # OCR
                print("Have to do OCR")

                document_url = self.uploadurl+"viewer.html?file=" + projectFile_.FileName
                OCR_FileName = projectFile_.UploadPath + temp + ".txt"
                OCR.pdf_splitter(projectFile_.UploadPath + projectFile_.FileName,
                                 OCR_FileName, self.ocrapikey)
                title = self.extractTitleText(OCR_FileName,projectFile_.lang)
                entityExtractor_ = EntityAndRelationBuilder(projectFile_.lang, OCR_FileName, projectFile_.ProjectName.strip("'"),
                                               document_url, projectFile_.FileName,title)
                entityExtractor_.getEntityTxtJson()

    def extractTitleText(self,filename , lang):
        f = open(filename, 'rb')
        title = ""
        data = f.read().decode('utf8', 'ignore')
        paragraphs = data.split("\n")
        title = data[0]
        if(lang not in "eng"):
            title = Translator.translate_(title, self.googleapikey)
            time.sleep(100)
        return title

    def extractTitle(self,filename , lang):
        title = ""

        with open(filename) as infile:
            soup = BeautifulSoup(infile, "html.parser")
        h1_tags = soup.find_all('h1')
        h2_tags = soup.find_all('h2')
        h3_tags = soup.find_all('h3')
        h4_tags = soup.find_all('h4')
        h5_tags = soup.find_all('h5')
        p_tags = soup.find_all('p')

        protocol = ""
        h1 = None
        h2 = None
        h3 = None
        h4 = None
        h5 = None
        p=None
        if(len(h1_tags)>0):
            h1=h1_tags[0].getText()
        if (len(h2_tags)>0):
            h2=h2_tags[0].getText()
        if (len(h3_tags)>0):
            h3=h3_tags[0].getText()
        if (len(h4_tags)>0):
            h4=h4_tags[0].getText()
        if (len(h5_tags)>0):
            h5=h5_tags[0].getText()

        if(len(p_tags)>0):
            p=p_tags[0].getText()

        if(h1 !=None):
            title = h1
        elif(h2 !=None):
            title = h2
        elif (h3 != None):
            title = h3
        elif (h4 != None):
            title = h4
        elif (h5 != None):
            title = h5
        elif (p != None):
            title = p

        print(title)
        if (lang not in "eng"):
            title = Translator.translate_(title, self.self.googleapikey)
            time.sleep(100)

        return title
