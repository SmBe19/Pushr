from pushr_settings import PUSHR_SETTINGS
from pushr_mail_util import send_mail

class TemplateMailFormatter:

    def __init__(self, subject_due, body_due, subject_new, body_new):
        self.subject_due = subject_due
        self.body_due = body_due
        self.subject_new = subject_new
        self.body_new = body_new

    def enrich_task(self, task):
        return task

    def format_mail(self, task):
        task = self.enrich_task(task)
        task.update(PUSHR_SETTINGS["template_enrich"])
        if task["sent_mails"] > 0:
            return (self.subject_due.format(**task), self.body_due.format(**task))
        else:
            return (self.subject_new.format(**task), self.body_new.format(**task))

class FileTemplateMailFormatter(TemplateMailFormatter):

    def __init__(self, subject_due, body_file_due, subject_new, body_file_new):
        self.subject_due = subject_due
        self.subject_new = subject_new
        with open(body_file_due, "r") as f:
            self.body_due = f.read()
        with open(body_file_new, "r") as f:
            self.body_new = f.read()

class Mail:

    def __init__(self, mail_formatter):
        self.mail_formatter = mail_formatter

    def send_mails(self, tasks):
        for task in tasks:
            formatted = self.mail_formatter.format_mail(task)
            if formatted is None:
                continue
            if not PUSHR_SETTINGS["debug_mode"]:
                send_mail(task["victim_name"], task["victim_mail"], PUSHR_SETTINGS["mail_blind_copy"], formatted[0], formatted[1])
            print("Sent mail to '{victim_name} <{victim_mail}>' for task '{name}' ({slug})".format(**task))
