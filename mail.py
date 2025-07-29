import os
from dotenv import load_dotenv
import ssl
import smtplib
import sys
from email.mime.text import MIMEText

load_dotenv()

USERNAME = os.getenv("EMAILID")
PASSWORD = os.getenv("EMAILPWD")

SMTPserver = 'smtp.mail.me.com'
sender = os.getenv("SENDER") if os.getenv("SENDER") is not None else USERNAME
destination = [] # list of email ids

# typical values for text_subtype are plain, html, xml
text_subtype = 'plain'


def send(classS, name):
    content=f"""\
Course available: {classS}: {name}
"""

    subject="COURSE AVAILABLE"
    try:
        msg = MIMEText(content, text_subtype)
        msg['Subject']=       subject
        msg['From']   = sender # some SMTP servers will do this automatically, not all
        context = ssl.create_default_context()
        conn = smtplib.SMTP(SMTPserver, port=587)
        # conn.set_debuglevel(False)
        conn.starttls(context=context)
        conn.login(USERNAME, PASSWORD)
        try:
            conn.sendmail(sender, destination, msg.as_string())
        finally:
            conn.quit()

    except Exception as e:
        print( "mail failed; %s %s" % ("CUSTOM_ERROR", e) ) # give an error message



# send("1685", "CSE 101")

# https://stackoverflow.com/a/64890