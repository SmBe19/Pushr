from pushr_settings import PUSHR_SETTINGS
import smtplib
from email.mime.text import MIMEText
import email.utils

USE_MIME = False

def send_mail(recipient_name, recipient_mail, blind_copy, subject, message):
    smtp = smtplib.SMTP(host=PUSHR_SETTINGS["smtp_server"], port=PUSHR_SETTINGS["smtp_port"])
    smtp.starttls()
    smtp.login(PUSHR_SETTINGS["smtp_user"], PUSHR_SETTINGS["smtp_password"])
    sender = PUSHR_SETTINGS["sender_mail"]
    sender_full = PUSHR_SETTINGS["sender_name"] + " <" + PUSHR_SETTINGS["sender_mail"] + ">"
    recipient_full = recipient_name + " <" + recipient_mail + ">"

    if USE_MIME:
        m = MIMEText(message.encode("utf-8"), _charset="utf-8")
        m["To"] = recipient_full
        m["From"] = sender_full
        m["Subject"] = subject
        m["Date"] = email.utils.formatdate()
        msg = m.as_string()
    else:
        msg = "Date: {0}\nFrom: {1}\nTo: {2}\nSubject: {3}\n\n{4}".format(email.utils.formatdate(), sender_full, recipient_full, subject, message)

    smtp.sendmail(sender, recipient_mail, msg)

    for mail in blind_copy:
        smtp.sendmail(sender, mail, msg)

    smtp.quit()
