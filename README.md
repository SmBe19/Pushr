# Pushr
Send automated push mails.

## Setup
Add the command `python pushr.py mail need` to cron or something similar using an appropriate timeframe. Additionally you should set up a control address if you don't want to handle the commands by yourself. Pass the mails sent to this control address to `python pushr.py handle` using stdin (this can be done for example with qmail).

## Usage Commandline
Call `python pushr.py --help` for help.

## Usage Mail
Write an email to the control address with one of the following commands:

- `!done slug`: mark the task with slug `slug` as done
- `!undone slug`: mark the task with slug `slug` as undone
- `!add slug victim_name victim_mail name due_date`: add a new task with the given values (`due_date` has to be formatted as follows: `YYYY-MM-DD`). This action needs admin privileges.
- `!addadmin mail`: Add the given mail as admin. This action needs admin privileges.
- `!removeadmin mail`: Remove the given mail from the admin list. This action needs admin privileges.
