import smtplib

gmail_user = 'sanam.ahmad@pucit.edu.pk'
gmail_password = 'mavra123'

sent_from = gmail_user
to = ['sanam.ahmad@pucit.edu.pk', 'sanam.ahmad@pucit.edu.pk']
subject = 'OMG Super Important Message'
body = 'Hey, whats up?\n\n- You'

email_text = """\  
From: %s  
To: %s  
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()

    print ('Email sent!')
except Exception as e:
    print(str(e))
    print ('Something went wrong...')
