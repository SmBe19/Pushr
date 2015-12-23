from pushr_settings import PUSHR_SETTINGS
from pushr_db_markov import Markov_DB
from pushr_mail import TemplateMailFormatter, FileTemplateMailFormatter
from collections import deque
import random

TEXT_START = "TEXT_START:::TEXT_START"
TEXT_END = "TEXT_END:::TEXT_END"

class MarkovTemplateMailFormatter(TemplateMailFormatter):

    def enrich_task(self, task):
        markov_text = Markov(PUSHR_SETTINGS["quote_text_markov_type"])
        markov_author = Markov(PUSHR_SETTINGS["quote_author_markov_type"])
        task["quote_text"] = markov_text.generate_text()
        task["quote_author"] = markov_author.generate_text()
        return task

class MarkovFileTemplateMailFormatter(FileTemplateMailFormatter):

    def enrich_task(self, task):
        markov_text = Markov(PUSHR_SETTINGS["quote_text_markov_type"])
        markov_author = Markov(PUSHR_SETTINGS["quote_author_markov_type"])
        task["quote_text"] = markov_text.generate_text()
        task["quote_author"] = markov_author.generate_text()
        return task

class Markov:

    def __init__(self, markov_type):
        self.db = Markov_DB(markov_type)
        self.separator = PUSHR_SETTINGS["markov_type"][markov_type]["separator"]
        self.prefix = PUSHR_SETTINGS["markov_type"][markov_type]["prefix"]
        self.length = PUSHR_SETTINGS["markov_type"][markov_type]["length"]
        self.endchars = PUSHR_SETTINGS["markov_type"][markov_type]["endchars"]

    def generate_text(self):
        text = ""
        state = deque([""] * (self.prefix - 1))
        state.append(TEXT_START)

        while state[-1] != TEXT_END and (len(text) <= self.length or text[-1] not in self.endchars):
            if state[-1] != TEXT_START:
                text += state[-1] + self.separator
            possibilities = self.db.get_possibilities("".join(state))

            if len(possibilities) == 0:
                break

            rnd = random.random()
            found = False
            for key in possibilities:
                rnd -= possibilities[key]
                if rnd <= 0:
                    state[0] = key
                    found = True
                    break

            if not found:
                return "404"

            state.rotate(-1)

        if len(self.separator) > 0:
            text = text[:-len(self.separator)]
        return text

    def analyze(self, text, do_commit=True):
        if not text:
            return

        if len(self.separator) == 0:
            parts = list(text)
        else:
            parts = text.split(self.separator)
        if len(parts) < self.prefix:
            return

        for i in range(self.prefix):
            self.db.add_occurence(TEXT_START + "".join(parts[:i]), parts[i], do_commit=False)
        for i in range(len(parts) - self.prefix):
            self.db.add_occurence("".join(parts[i:i+self.prefix]), parts[i+self.prefix], do_commit=False)
        self.db.add_occurence("".join(parts[-self.prefix:]), TEXT_END, do_commit=False)

        if do_commit:
            self.db.commit()

    def analyze_file(self, file_name):
        with open(file_name, "r") as f:
            for line in f:
                self.analyze(line, do_commit=False)
        self.db.commit()

    def analyze_stdio(self):
        try:
            while True:
                line = input().strip()
                self.analyze(line, do_commit=False)
        except EOFError:
            pass
        self.db.commit()
