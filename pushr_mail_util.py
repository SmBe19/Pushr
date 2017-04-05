from pushr_settings import PUSHR_SETTINGS
import smtplib
from email.mime.text import MIMEText
import email.utils

import base64
import hashlib
import random
import time

USE_MIME = False

def send_mail(recipient_name, recipient_mail, blind_copy, subject, message):
    smtp = smtplib.SMTP(host=PUSHR_SETTINGS["smtp_server"], port=PUSHR_SETTINGS["smtp_port"])
    smtp.starttls()
    smtp.login(PUSHR_SETTINGS["smtp_user"], PUSHR_SETTINGS["smtp_password"])
    sender = PUSHR_SETTINGS["sender_mail"]
    sender_full = PUSHR_SETTINGS["sender_name"] + " <" + PUSHR_SETTINGS["sender_mail"] + ">"
    recipient_full = recipient_name + " <" + recipient_mail + ">"
    message_id = str(round(time.time()*10)) + "." + sha256(message) + "@" + PUSHR_SETTINGS["message_id_domain"]

    if USE_MIME:
        m = MIMEText(message.encode("utf-8"), _charset="utf-8")
        m["To"] = recipient_full
        m["From"] = sender_full
        m["Subject"] = subject
        m["Date"] = email.utils.formatdate()
        m["Message-ID"] = message_id
        msg = m.as_string()
    else:
        msg = "Date: {0}\nFrom: {1}\nMessage-ID: <{2}>\nTo: {3}\nSubject: {4}\n\n{5}".format(email.utils.formatdate(), sender_full, message_id, recipient_full, subject, message)

    smtp.sendmail(sender, recipient_mail, msg)

    for mail in blind_copy:
        smtp.sendmail(sender, mail, msg)

    smtp.quit()

def sha256(msg):
    h = hashlib.sha256()
    h.update(msg.encode("utf-8"))
    d = h.digest()
    return base64.b64encode(d).decode("utf-8")
