from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import string
import logtools

"""
Toolbox for sending emails through SMTP
"""

def send_error(error, email, lfil=None):
    sender = 'noreply@kirschner.med.harvard.edu'
    receivers = email

    message = MIMEMultipart(
        From="CoreRep Server <noreply@kirschner.med.harvard.edu>",
    )

    message['Subject'] = "COREREP SERVER ERROR!!!"

    body = MIMEText(error, 'html')
    message.attach(body)

    #make sure email can be send, and send
    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "Successfully sent email"
    except smtplib.SMTPException:
        if lfil is not None:
            logtools.add_fatal_error(lfil, "UNABLE TO SEND EMAIL!!!")
        print "Error: unable to send email"


def send_email(info, email, files, lfil=None, sub="CoreRep Results"):
    sender = 'noreply@kirschner.med.harvard.edu'
    receivers = email

    message = MIMEMultipart()
    message['To'] = email
    message['From'] = "CoreRep Server <noreply@kirschner.med.harvard.edu>"
    message['Subject'] = sub

    body = MIMEText(info, 'html')
    message.attach(body)

    for f in files or []:
        try:
            with open(f, "rb") as fil:
                attach_file = MIMEApplication(fil.read())
        except IOError:
            open(f, "w").close()
            with open(f, "rb") as fil:
                attach_file = MIMEApplication(fil.read())
        attach_file.add_header('Content-Disposition', 'attachment', filename=f)
        message.attach(attach_file)

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "Successfully sent email"
    except smtplib.SMTPException:
        if lfil is not None:
            logtools.add_fatal_error(lfil, "UNABLE TO SEND EMAIL!!!")
        print "Error: unable to send email"