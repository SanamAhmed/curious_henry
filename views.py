# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.views import APIView
from rest_framework.response import Response
#for function based views
from rest_framework.decorators import api_view
#for apiroot reverse
from rest_framework.reverse import reverse
import datetime
import nltk
import pyodbc
import pandas as pd
from api import model_fr
from api import vectTrain_fr
from api import model_arabizi
from api import vectTrain_arabizi
from api import model_arabic
from api import vectTrain_arabic
from api import startup
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import QueryDict
from nltk.corpus import stopwords
from nltk.stem.snowball import FrenchStemmer
from textblob import TextBlob
import re
import gensim



import json

from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

DataFiles = '/root/sentiment/DataFiles/'



def api_root(request):
    """
    The root of all APIs, serves as a basic presentation of the APIs aviliable,
    however needs manual additions of the functions.
    reverse() serves as a url call to each function views.
    """
    return Response({
        'hello_world': reverse('hello_world', request=request),
        'sentiment': reverse('sentiment', request=request),
        'topicmodelingsearch': reverse('topicmodelingsearch', request=request),
        'entityapi': reverse('entityapi', request=request),
        'topicmodeling': reverse('topicmodeling', request=request)
    })

@api_view()
def hello_world(request):
    """
    An example api, this part of text will be visible when entering /hello_world.

    """

    return Response({"message": "Hello, world!"})

@api_view()
def sentiment(request):
    try:
        comment = request.GET.get('comment')
        lan = request.GET.get('lan')
        comment.replace("%20"," ")
        comment_class = "Neutral"
        df_t = pd.DataFrame(columns=["Comment"])
        df_t.loc[1] = comment
        if lan=="fr":
            predictions = model_fr.predict(vectTrain_fr.transform(df_t['Comment']))
            comment_class = predictions[0];

        elif lan=="ar":
            predictions = model_arabizi.predict(vectTrain_arabizi.transform(df_t['Comment']))
            comment_class = predictions[0];

        elif lan=="arz":
            predictions = model_arabic.predict(vectTrain_arabic.transform(df_t['Comment']))
            comment_class = predictions[0];

        else:
            analysis = TextBlob(comment)
            comment_class=""+str(analysis.sentiment.polarity)



        return Response({'function': 'sentiment','Comment:Class':   comment_class})
    except Exception as e:
        return Response({'function': 'sentiment','result': 'there was an error ' + str(e)})

@api_view()
def sentimentTrainingUpdate(request):
    try:
        comment = request.GET.get('comment')
        lan = request.GET.get('lan')
        class_ = request.GET.get('class')
        comment.replace("%20"," ")
        comment_updated = "No"
        if lan=="fr":
            df_fr= pd.read_csv(DataFiles +'FinalDataSetStopWordRemoval.csv')
            for (i, row) in df_fr.iterrows():
                val = row['Comment']
                if val==comment:
                    row['Class'] = class_
                    df_fr.loc[i, 'Class'] = class_
                    comment_updated = "Yes"
                    df_fr.to_csv(DataFiles +'FinalDataSetStopWordRemoval.csv',index=False)
                    startup()
                    break





        elif lan=="arabizi":
            x1 = pd.ExcelFile("/home/Hooriya/ArabiziSenti.xlsx")
            df_arabi = x1.parse("Sheet1")
            for (i, row) in df_arabi.iterrows():
                val = row['Comment']
                if val==comment:
                    df_arabi.loc[i, 'Class'] = class_
                    writer = pd.ExcelWriter("/home/Hooriya/ArabiziSenti.xlsx")
                    df_arabi.to_excel(writer,sheet_name = 'Sheet1',index=False)
                    writer.save()
                    writer.close()
                    startup()
                    comment_updated = "Yes"

                    break





        elif lan=="arabic":
            x2 = pd.ExcelFile("/home/Hooriya/ArabicSenti.xlsx")
            df_arabic = x2.parse("Sheet1")
            df_arabic.loc[df_arabic['Comment'] == comment, 'Class'] = class_
            for (i, row) in df_arabic.iterrows():
                val = row['Comment']
                if val==comment:
                    df_arabic.loc[i, 'Class'] = class_
                    writer = pd.ExcelWriter("/home/Hooriya/ArabicSenti.xlsx")
                    df_arabic.to_excel(writer,sheet_name = 'Sheet1',index=False)
                    writer.save()
                    writer.close()
                    startup()
                    comment_updated = "Yes"
                    break




        return Response({'function': 'sentimentTrainingUpdate','Comment:Updated':   comment_updated})
    except Exception as e:
        return Response({'function': 'sentimentTrainingUpdate','result': 'there was an error ' + str(e)})


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))

def login(request):
    username = request.GET.get("username")
    password = request.GET.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)

def topicmodeling(request):
    comment = request.GET.get('comment')
    language = request.GET.get('lan')
    stop_words=[]
    if language=="French":
        stop_words = stopwords.words('french')
    elif language=="Arabic":
        x2 = pd.ExcelFile("/root/sentiment/DataFiles/ArabicStopWords.xlsx")
        dfs = x2.parse("Sheet1")
        stop_words_= dfs['stopwords'].tolist()
        for s in stop_words_:
            s = s.strip(' \t\n\r')
            stop_words.append(s)

    elif language=="Arabizi":
        x2 = pd.ExcelFile("/root/sentiment/DataFiles/ArabiziStopWords.xlsx")
        dfs = x2.parse("Sheet1")
        stop_words_= dfs['stopwords'].tolist()
        for s in stop_words_:
            s = s.strip(' \t\n\r')
            stop_words.append(s)
    try:
        cleantext = re.sub(r'[*()+0123456789."]', ' ', comment)
        topics = showTopics(cleantext,stop_words)
        my_topic = ''.join(map(str, topics))
        topic = re.sub(r'[*()+0123456789."]', ' ', my_topic)
        return Response({'function': 'topicmodeling', 'Comment Topic :': topic})
    except Exception as e:
        return Response({'function': 'topicmodeling', 'result': 'there was an error ' + str(e)})






def clean(doc,stop_words):
    print("loooooooooooooooooooook")
    #stop_free = " ".join([i for i in doc.lower().split() if i not in stop_words ])
    stop_free = []

    for i in doc.lower().split():
        if i not  in stop_words:
            stop_free.append(" "+i)

    str1 = "".join(stop_free)
    print(str1)
    return str1


def showTopics(doc1,stop_words):
    print(doc1)
    if(len(doc1)>1):
        doc_complete = [doc1]

        doc_clean = [clean(doc,stop_words).split() for doc in doc_complete]
        dictionary = corpora.Dictionary(doc_clean)
        doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
        Lda = gensim.models.ldamodel.LdaModel
        l = len(doc_term_matrix)
        if(l>0):
            ldamodel = Lda(doc_term_matrix, num_topics=3, id2word = dictionary, passes=50)
            print(ldamodel.print_topics(num_topics=3, num_words=3))
            return ldamodel.print_topics(num_topics=3, num_words=3)
        else:
            return " "
    else:
        return "  "



@api_view()
def topicmodelingsearch(request):
    comment_f = request.GET.get('comment_f')
    comment_class = request.GET.get('comment_class')
    startdate = request.GET.get('startdate')
    enddate = request.GET.get('enddate')
    cityf = request.GET.get('cityf')
    gender = request.GET.get('gender')
    advance = request.GET.get('advance')
    rlimit= request.GET.get('rlimit')
    lan = request.GET.get('lan')
    if lan=="fr":
        x1 = pd.ExcelFile("/root/sentiment/DataFiles/TopicModelingFrench03.xlsx")
        df_S = x1.parse("Sheet1")

    elif lan=="arabizi":
        x1 = pd.ExcelFile("/root/sentiment/DataFiles/TopicModelingArabizi.xlsx")
        df_S = x1.parse("Sheet1")

    elif lan=="arabic":
        x1 = pd.ExcelFile("/root/sentiment/DataFiles/TopicModelingArabic01.xlsx")
        df_S = x1.parse("Sheet1")
    else:
        x1 = pd.ExcelFile("/root/sentiment/DataFiles/TopicModelingFrench03.xlsx")
        df_S = x1.parse("Sheet1")

    ignore = "0"
    if(rlimit==""):
        rlimit=10
        ignore = "1"
    print("Advance")
    print(advance)
    print("cityf")
    print(cityf)
    #df_S = pd.read_csv("TopicModelingArabizi.csv",encoding ="ISO-8859-1")
    #raw = "%r"%text

    #print(len(words))
    if(startdate !=""):
        sd = datetime.datetime.strptime(startdate, '%d/%m/%Y')
    if(enddate !=""):
        ed = datetime.datetime.strptime(enddate, '%d/%m/%Y')
    commentList = []
    topicList = []
    sentimentList = []
    commentDateList = []
    commentCityList = []
    commentGenderList = []
    commentFifthList = []
    counter = 0
    max = int(rlimit)

    for row in df_S.itertuples():
        addRecord = "T"
        if(ignore=="0" and counter>max):
            break
        comment_ = df_S.loc[row.Index, 'Comment']
        topic_ = df_S.loc[row.Index, 'Topic']
        sentiment_ = df_S.loc[row.Index, 'Sentiment']
        dstring = df_S.loc[row.Index, 'Date']
        city_ = df_S.loc[row.Index, 'City']
        gender_ = df_S.loc[row.Index, 'Gender']
        fifth_ = df_S.loc[row.Index, 'Fifth']
        try:
            ds = datetime.datetime.strptime(str(dstring), '%d/%m/%Y')
        except ValueError:
            ds = datetime.datetime.strptime(str(dstring), '%Y-%m-%d %H:%M:%S')



        if(comment_f !=""):
            words = nltk.word_tokenize(comment_f)
            rlist = []
            for w in words:
                rlist.append(testPresence(w,topic_,comment_))

            if (allFalse(rlist)==True):
                addRecord = "F"


        if(enddate !="" and enddate !="" and (ds < sd or ds > ed)):
            addRecord = "F"


        if(cityf !="" and cityf.lower() != str(city_).lower()):
            addRecord = "F"

        if(gender !="" and gender.lower() != str(gender_).lower()):
            addRecord = "F"
        if(comment_class !="" and comment_class.lower() != str(sentiment_).lower()):
            addRecord = "F"

        if(advance !="" and advance != str(fifth_)):
            addRecord = "F"



        if(addRecord == "T"):
            counter=counter+1
            commentList.append(comment_)
            sentimentList.append(sentiment_)
            topicList.append(topic_)
            commentDateList.append(dstring)
            commentCityList.append(city_)
            commentGenderList.append(gender_)
            commentFifthList.append(fifth_)
    search = [('Comment',commentList ),
         ('Topic', topicList),
         ('Sentiment', sentimentList),
         ('Date', commentDateList),
         ('City', commentCityList),
         ('Gender', commentGenderList),

         ('Advance', commentFifthList),

         ]
    df = pd.DataFrame.from_items(search)
    #result2 = HttpResponse(json.dumps(df0_js), content_type = 'application/json')

    return Response(df.to_json(orient='records'))




@api_view()
def entityapi(request):
    try:
        label_ = request.GET.get('label')
        entity_ = request.GET.get('entity')
        cnxn = pyodbc.connect('Driver={SQL Server};'
                          'Server=95.216.64.125;'
                          'Database=ArabiziDB;'
                          'Trusted_Connection=no;'
                          'uid=bilal;pwd=bilal')

        cur = cnxn.cursor()
        label_=request.form["label"]
        entity_ = request.form["entity"]

        if (label_=="Person_Entities"):
            sql = 'INSERT INTO Person_Entities  (Entity_Text) VALUES (?);'
        elif (label_=="Location__Entities "):
            sql = 'INSERT INTO Location__Entities  (Entity_Text) VALUES (?);'
        elif (label_=="Brand__Entities "):
            sql = 'INSERT INTO Brand__Entities   (Entity_Text) VALUES (?);'

        elif (label_=="ProductOrService_Entities"):
            sql = 'INSERT INTO ProductOrService_Entities   (Entity_Text) VALUES (?);'

        elif (label_ == "Company_Entities "):
            sql = 'INSERT INTO Company_Entities  (Entity_Text) VALUES (?);'
        elif (label_ == "ProductReference_Entities "):
            sql = 'INSERT INTO ProductReference_Entities    (Entity_Text) VALUES (?);'

        else:
            sql=""

        args = (entity_.strip("'"))
        # Execute the SQL command
        if(sql!=""):
            cur.execute(sql, args)
        # Commit your changes in the database
            cnxn.commit()
            cnxn.close()




        return Response({'function': 'addEntity','Entity':   'Enity Added'})
    except Exception as e:
        return Response({'function': 'addEntity','result': 'there was an error ' + str(e)})


