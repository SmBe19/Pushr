#!/usr/bin/env python3

from pushr_settings import PUSHR_SETTINGS
from pushr_db_tasks import Task_DB
from pushr_mail_handler import handle_mail
from pushr_mail import Mail, FileTemplateMailFormatter

import argparse
import os

def admin(args):
    db = Task_DB()
    action = args.action.lower()
    if action == "add":
        res = db.add_admin(args.mail)
        if not res:
            print("Admin not added!")
    elif action == "remove":
        res = db.remove_admin(args.mail)
        if not res:
            print("Admin not removed!")
    else:
        print("unknown action '" + args.action + "'")

def addtask(args):
    db = Task_DB()
    res = db.add_task(args.slug, args.victim_name, args.victim_mail, args.name, args.due_date)
    if not res:
        print("Task not added!")

def chtask(args):
    db = Task_DB()
    action = args.action.lower()
    if action == "done":
        db.set_done(args.slug)
    elif action == "undone":
        db.set_undone(args.slug)
    else:
        print("unknown action '" + args.action + "'")

def itemlist(args):
    db = Task_DB()
    listname = args.itemlist.lower()
    items = []
    if listname == "admin":
        items = db.get_admins()
    else:
        tasks = []
        if listname == "new":
            tasks = db.get_new_tasks()
        elif listname == "due":
            tasks = db.get_due_tasks()
        elif listname == "need":
            tasks = db.get_need_tasks()
        elif listname == "undone":
            tasks = db.get_undone_tasks()
        elif listname == "done":
            tasks = db.get_done_tasks()
        items = ["{slug} ({victim_name} / {due_date}): {name}".format(**task) for task in tasks]
    for item in items:
        print(item)

def mail(args):
    db = Task_DB()
    mailsender = Mail(FileTemplateMailFormatter(PUSHR_SETTINGS["mail_subject_due"], PUSHR_SETTINGS["template_file_due"], PUSHR_SETTINGS["mail_subject_new"], PUSHR_SETTINGS["template_file_new"]))
    action = args.action.lower()
    tasks = []

    if action == "new":
        tasks = db.get_new_tasks()
    elif action == "due":
        tasks = db.get_due_tasks()
    elif action == "need":
        tasks = db.get_need_tasks()
    elif action == "undone":
        tasks = db.get_undone_tasks()

    mailsender.send_mails(tasks)
    for task in tasks:
        db.add_sent_mail(task["slug"])

def handle(args):
    handle_mail()

def nothing(args):
    print("missing arguments. Call --help")

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    parser = argparse.ArgumentParser(description="send push mails")
    subparsers = parser.add_subparsers(help="sub-command help")
    parser.set_defaults(func=nothing)

    admin_parser = subparsers.add_parser("admin", help="admin management")
    admin_parser.add_argument("action", help="action to perform (add)")
    admin_parser.add_argument("mail", help="mail to perform action on")
    admin_parser.set_defaults(func=admin)

    task_parser = subparsers.add_parser("addtask", help="add task")
    task_parser.add_argument("slug", help="slug of the task")
    task_parser.add_argument("victim_name", help="name of the victim")
    task_parser.add_argument("victim_mail", help="mail of the victim")
    task_parser.add_argument("name", help="name of the task")
    task_parser.add_argument("due_date", help="date the task is due")
    task_parser.set_defaults(func=addtask)

    chtask_parser = subparsers.add_parser("chtask", help="task management")
    chtask_parser.add_argument("action", help="action to perform (done / undone)")
    chtask_parser.add_argument("slug", help="slug of task to perform action on")
    chtask_parser.set_defaults(func=chtask)

    itemlist_parser = subparsers.add_parser("list", help="list items")
    itemlist_parser.add_argument("itemlist", help="which items to list (admin / new / need / due / undone / done)")
    itemlist_parser.set_defaults(func=itemlist)

    mail_parser = subparsers.add_parser("mail", help="send mails")
    mail_parser.add_argument("action", help="action to perform (new / due / need / undone)")
    mail_parser.set_defaults(func=mail)

    handle_parser = subparsers.add_parser("handle", help="handle an incomming mail")
    handle_parser.set_defaults(func=handle)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
