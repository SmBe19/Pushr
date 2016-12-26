from pushr_settings import PUSHR_SETTINGS
from pushr_db_tasks import Task_DB
import re
import shlex

RE_FROM_ADDRESS = re.compile(r"From: (?:.*? <(\S+@\S+.\S+)>|(\S+@\S+.\S+))")
RE_ACTION = re.compile(r".*?!(done|undone|add|addadmin|removeadmin) (.*)")

def handle_mail():
    db = Task_DB()
    from_address = None
    is_admin = False
    try:
        while True:
            line = input().strip()
            if from_address is None:
                match = RE_FROM_ADDRESS.match(line)
                if match:
                    from_address = match.group(1) if match.group(1) is not None else match.group(2)
                    is_admin = db.is_admin(from_address)
            match = RE_ACTION.match(line.lower(), re.IGNORECASE)
            if match:
                action = match.group(1).lower()
                args = shlex.split(match.group(2))
                if action == "done":
                    if len(args) >= 1:
                        db.set_done(args[0])
                elif action == "undone":
                    if len(args) >= 1:
                        db.set_undone(args[0])
                elif action == "add":
                    if is_admin and len(args) >= 5:
                        db.add_task(args[0], args[1], args[2], args[3], args[4])
                elif action == "addadmin":
                    if is_admin and len(args) >= 1:
                        db.add_admin(args[0])
                elif action == "removeadmin":
                    if is_admin and len(args) >= 1:
                        db.remove_admin(args[0])
    except EOFError:
        pass
