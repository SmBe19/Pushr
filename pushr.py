#!/usr/bin/env python3

from pushr_settings import PUSHR_SETTINGS
from pushr_db_tasks import Task_DB
from pushr_mail_markov import Markov, MarkovFileTemplateMailFormatter
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
    res = db.add_task(args.victim_name, args.victim_mail, args.name, args.due_date)
    if not res:
        print("Task not added!")

def chtask(args):
    db = Task_DB()
    action = args.action.lower()
    if action == "done":
        if not db.set_done(args.slug):
            print("invalid slug")
    elif action == "undone":
        if not db.set_undone(args.slug):
            print("invalid slug")
    elif action == "due_date":
        if len(args.args) != 1:
            print("Expected exactly one argument: due_date")
        else:
            if not db.set_due_date(args.slug, args.args[0]):
                print("Invalid date or invalid slug")
    elif action == "victim_name":
        if len(args.args) != 1:
            print("Expected exactly one argument: victim_name")
        else:
            if not db.set_victim_name(args.slug, args.args[0]):
                print("Invalid date or invalid slug")
    elif action == "victim_mail":
        if len(args.args) != 1:
            print("Expected exactly one argument: victim_mail")
        else:
            if not db.set_victim_mail(args.slug, args.args[0]):
                print("Invalid date or invalid slug")
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
        else:
            print("unknown listname '" + args.itemlist + "'")
        items = ["{slug} ({victim_name} / {due_date}): {name}".format(**task) for task in tasks]
    for item in items:
        print(item)

def mail(args):
    db = Task_DB()
    mailsender = Mail(MarkovFileTemplateMailFormatter(PUSHR_SETTINGS["mail_subject_due"], PUSHR_SETTINGS["template_file_due"], PUSHR_SETTINGS["mail_subject_new"], PUSHR_SETTINGS["template_file_new"]))
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
    else:
        print("unknown action '" + args.action + "'")

    sent = mailsender.send_mails(tasks)
    for task in sent:
        db.add_sent_mail(task["slug"])

def handle(args):
    handle_mail()

def markov(args):
    markov = Markov(args.markov_type)
    action = args.action.lower()

    if action == "analyze":
        if args.file is None:
            markov.analyze_stdio()
        else:
            markov.analyze_file(args.file)
    elif action == "generate":
        print(markov.generate_text())
    else:
        print("unknown action '" + args.action + "'")

def nothing(args):
    print("missing arguments. Call --help")

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    parser = argparse.ArgumentParser(description="send push mails")
    subparsers = parser.add_subparsers(help="sub-command help")
    parser.set_defaults(func=nothing)

    admin_parser = subparsers.add_parser("admin", help="admin management")
    admin_parser.add_argument("action", help="action to perform (add / remove)")
    admin_parser.add_argument("mail", help="mail to perform action on")
    admin_parser.set_defaults(func=admin)

    task_parser = subparsers.add_parser("addtask", help="add task")
    task_parser.add_argument("victim_name", help="name of the victim")
    task_parser.add_argument("victim_mail", help="mail of the victim")
    task_parser.add_argument("name", help="name of the task")
    task_parser.add_argument("due_date", help="date the task is due")
    task_parser.set_defaults(func=addtask)

    chtask_parser = subparsers.add_parser("chtask", help="task management")
    chtask_parser.add_argument("action", help="action to perform (done / undone / due_date / victim_name / victim_mail)")
    chtask_parser.add_argument("slug", help="slug of task to perform action on")
    chtask_parser.add_argument("args", nargs="*", help="additional arguments")
    chtask_parser.set_defaults(func=chtask)

    itemlist_parser = subparsers.add_parser("list", help="list items")
    itemlist_parser.add_argument("itemlist", help="which items to list (admin / new / need / due / undone / done)")
    itemlist_parser.set_defaults(func=itemlist)

    mail_parser = subparsers.add_parser("mail", help="send mails")
    mail_parser.add_argument("action", help="action to perform (new / due / need / undone)")
    mail_parser.set_defaults(func=mail)

    handle_parser = subparsers.add_parser("handle", help="handle an incomming mail")
    handle_parser.set_defaults(func=handle)

    markov_parser = subparsers.add_parser("markov", help="control markov engine")
    markov_parser.add_argument("markov_type", help="name of the markov type (default: quote_text / quote_author)")
    markov_parser.add_argument("action", help="action to perform (analyze / generate)")
    markov_parser.add_argument("file", help="file to analyze", nargs="?", default=None)
    markov_parser.set_defaults(func=markov)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
