from pushr_settings import PUSHR_SETTINGS
import sqlite3
import os
import datetime

expression_get_new_tasks = "SELECT slug, victim_name, victim_mail, name, due_date, sent_mails FROM tasks WHERE sent_mails = 0 AND done = 0"
expression_get_due_tasks = "SELECT slug, victim_name, victim_mail, name, due_date, sent_mails FROM tasks WHERE date(due_date) <= date('now') AND done = 0"
expression_get_need_tasks = "SELECT slug, victim_name, victim_mail, name, due_date, sent_mails FROM tasks WHERE (date(due_date) <= date('now') OR sent_mails = 0) AND done = 0"
expression_get_undone_tasks = "SELECT slug, victim_name, victim_mail, name, due_date, sent_mails FROM tasks WHERE done = 0"
expression_get_done_tasks = "SELECT slug, victim_name, victim_mail, name, due_date, sent_mails FROM tasks WHERE done != 0"
expression_get_task = "SELECT slug, victim_name, victim_mail, name, due_date FROM tasks WHERE slug = ?"

expression_insert_task = "INSERT INTO tasks (slug, victim_name, victim_mail, name, due_date, sent_mails, done) VALUES (?, ?, ?, ?, ?, 0, 0)"
expression_add_sent_mail = "UPDATE tasks SET sent_mails = sent_mails + 1 WHERE slug = ?"
expression_set_done = "UPDATE tasks SET done = 1 WHERE slug = ?"
expression_set_undone = "UPDATE tasks SET done = 0 WHERE slug = ?"
expression_set_due_date = "UPDATE tasks SET due_date = ? WHERE slug = ?"

expression_add_admin = "INSERT INTO admins (mail) VALUES (?)"
expression_remove_admin = "DELETE FROM admins WHERE mail = ?"
expression_get_admin = "SELECT mail FROM admins WHERE mail = ?"
expression_get_admins = "SELECT mail FROM admins"

date_format = "%Y-%m-%d"

class Task_DB:

    def __init__(self):
        db_exists = os.path.isfile(PUSHR_SETTINGS["db_name_tasks"])

        self.db = sqlite3.connect(PUSHR_SETTINGS["db_name_tasks"])

        if not db_exists:
            self.create_db()

    def create_db(self):
        self.db.execute("DROP TABLE IF EXISTS admins")
        self.db.execute("DROP TABLE IF EXISTS tasks")
        self.db.execute("CREATE TABLE admins (id INTEGER PRIMARY KEY, mail TEXT)")
        self.db.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY, slug TEXT, victim_name TEXT, victim_mail TEXT, name TEXT, due_date TEXT, sent_mails INTEGER, done INTEGER)")

        self.db.commit()

    def add_task(self, slug, victim_name, victim_mail, name, due_date):
        if not self.check_date(due_date):
            return False
        if self.get_task(slug) is not None:
            return False
        self.db.execute(expression_insert_task, (slug, victim_name, victim_mail, name, due_date))
        self.db.commit()
        return True

    def add_sent_mail(self, slug):
        if self.get_task(slug) is None:
            return False
        self.db.execute(expression_add_sent_mail, (slug,))
        self.db.commit()
        return True

    def set_done(self, slug):
        if self.get_task(slug) is None:
            return False
        self.db.execute(expression_set_done, (slug,))
        self.db.commit()
        return True

    def set_undone(self, slug):
        if self.get_task(slug) is None:
            return False
        self.db.execute(expression_set_undone, (slug,))
        self.db.commit()
        return True

    def set_due_date(self, slug, due_date):
        if not self.check_date(due_date):
            return False
        if self.get_task(slug) is None:
            return False
        self.db.execute(expression_set_due_date, (due_date, slug))
        self.db.commit()
        return True

    def get_tasks(self, expression):
        c = self.db.cursor()
        c.execute(expression)

        tasks = []
        for row in c:
            tasks.append(self.create_task(*row))

        return tasks

    def get_new_tasks(self):
        return self.get_tasks(expression_get_new_tasks)

    def get_due_tasks(self):
        return self.get_tasks(expression_get_due_tasks)

    def get_need_tasks(self):
        return self.get_tasks(expression_get_need_tasks)

    def get_undone_tasks(self):
        return self.get_tasks(expression_get_undone_tasks)

    def get_done_tasks(self):
        return self.get_tasks(expression_get_done_tasks)

    def get_task(self, slug):
        c = self.db.cursor()
        c.execute(expression_get_task, (slug,))

        return c.fetchone()

    def add_admin(self, mail):
        if self.is_admin(mail):
            return False
        self.db.execute(expression_add_admin, (mail,))
        self.db.commit()
        return True

    def remove_admin(self, mail):
        if not self.is_admin(mail):
            return False
        self.db.execute(expression_remove_admin, (mail,))
        self.db.commit()
        return True

    def is_admin(self, mail):
        c = self.db.cursor()
        c.execute(expression_get_admin, (mail,))
        return c.fetchone() is not None

    def get_admins(self):
        c = self.db.cursor()
        c.execute(expression_get_admins)

        admins = [row[0] for row in c]
        return admins

    def commit(self):
        self.db.commit()

    def close(self):
        self.db.close()

    def create_task (self, slug, victim_name, victim_mail, name, due_date, sent_mails):
        return {"slug": slug, "victim_name": victim_name, "victim_mail": victim_mail, "name": name, "due_date": due_date, "sent_mails": sent_mails}

    def check_date(self, date):
        try:
            datetime.datetime.strptime(date, date_format)
        except ValueError:
            return False
        return True
