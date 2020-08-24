import email
import os

from email import policy
from email.parser import BytesParser,Parser
os.system('cd /home/sanam ; msgconvert Test.msg')
with open('/home/sanam/Test.msg.eml', 'rb') as fp:  # select a specific email file from the list
    msg = BytesParser(policy=policy.default).parse(fp)
text = msg.get_body(preferencelist=('plain')).get_content()
with open('/home/sanam/Test/chunmun.msg.eml', 'r+') as fhp:  # select a specific email file from the list
    headers = Parser().parse(fhp)
print(headers["to"])
print(headers["from"])
print(headers["subject"])

#print(text)  # print the email content

