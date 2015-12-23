from pushr_settings import PUSHR_SETTINGS
import smtplib

def send_mail(recipient_name, recipient_mail, subject, message):
    smtp = smtplib.SMTP(host=PUSHR_SETTINGS["smtp_server"], port=PUSHR_SETTINGS["smtp_port"])
    smtp.starttls()
    smtp.login(PUSHR_SETTINGS["smtp_user"], PUSHR_SETTINGS["smtp_password"])
    sender = PUSHR_SETTINGS["sender_mail"]
    sender_full = PUSHR_SETTINGS["sender_name"] + " <" + PUSHR_SETTINGS["sender_mail"] + ">"
    recipient_full = recipient_name + " <" + recipient_mail + ">"
    msg = "From: {0}\nTo: {1}\nSubject: {2}\n\n{3}".format(sender_full, recipient_full, subject, message)
    smtp.sendmail(sender, recipient_mail, msg)
    smtp.quit()
