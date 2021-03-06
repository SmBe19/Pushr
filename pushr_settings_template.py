# rename to pushr_settings.py

PUSHR_SETTINGS = {}

PUSHR_SETTINGS["debug_mode"] = False

PUSHR_SETTINGS["slug_length"] = 8

PUSHR_SETTINGS["sender_name"] = "Pushr"
PUSHR_SETTINGS["sender_mail"] = "me@example.com"
PUSHR_SETTINGS["mail_blind_copy"] = ["archive@example.com"]
PUSHR_SETTINGS["message_id_domain"] = "example.com"
PUSHR_SETTINGS["template_enrich"] = {
    "control_address": "control@example.com",
    "feedback_address": "feedback@example.com"
}

PUSHR_SETTINGS["quote_text_markov_type"] = "quote_text"
PUSHR_SETTINGS["quote_author_markov_type"] = "quote_author"
PUSHR_SETTINGS["markov_type"] = {
    "quote_text": {
        "separator": " ",
        "prefix": 1,
        "length": 20,
        "endchars": ['.', '!', '?']
    },
    "quote_author": {
        "separator": "",
        "prefix": 1,
        "length": 10,
        "endchars": [' ']
    }
}

PUSHR_SETTINGS["template_file_due"] = "mail_template_due.txt"
PUSHR_SETTINGS["template_file_new"] = "mail_template_new.txt"
PUSHR_SETTINGS["mail_subject_due"] = "Task: {name}"
PUSHR_SETTINGS["mail_subject_new"] = "new Task: {name}"

PUSHR_SETTINGS["db_name_markov"] = "pushr_markov_{markov_type}.db"
PUSHR_SETTINGS["db_name_tasks"] = "pushr_tasks.db"

PUSHR_SETTINGS["smtp_server"] = "smtp.gmail.com"
PUSHR_SETTINGS["smtp_port"] = 587
PUSHR_SETTINGS["smtp_user"] = "me@example.com"
PUSHR_SETTINGS["smtp_password"] = "123"
