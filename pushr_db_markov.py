from pushr_settings import PUSHR_SETTINGS
import sqlite3
import os

expression_insert_state = "INSERT INTO markov_chain (state, next_state, occurrence) VALUES (?, ?, 0)"
expression_insert_state_total = "INSERT INTO markov_chain_total (state, occurrence) VALUES (?, 0)"
expression_query_state = "SELECT id FROM markov_chain WHERE state = ? AND next_state = ?"
expression_query_state_total = "SELECT id FROM markov_chain_total WHERE state = ?"
expression_add_occurence = "UPDATE markov_chain SET occurrence=occurrence+1 WHERE state = ? AND next_state = ?"
expression_add_occurence_total = "UPDATE markov_chain_total SET occurrence=occurrence+1 WHERE state = ?"
expression_query_markov_chain = "SELECT next_state, occurrence FROM markov_chain WHERE state = ?"
expression_query_markov_chain_total = "SELECT occurrence FROM markov_chain_total WHERE state = ?"

class Markov_DB:

    def __init__(self, markov_type):
        db_exists = os.path.isfile(PUSHR_SETTINGS["db_name_markov"].format(markov_type=markov_type))

        self.db = sqlite3.connect(PUSHR_SETTINGS["db_name_markov"].format(markov_type=markov_type))

        if not db_exists:
            self.create_db()

    def create_db(self):
        self.db.execute("DROP TABLE IF EXISTS markov_chain")
        self.db.execute("DROP TABLE IF EXISTS markov_chain_total")
        self.db.execute("CREATE TABLE markov_chain (id INTEGER PRIMARY KEY, state TEXT, next_state TEXT, occurrence INTEGER)")
        self.db.execute("CREATE TABLE markov_chain_total (id INTEGER PRIMARY KEY, state TEXT, occurrence INTEGER)")

        self.db.commit()

    def add_occurence(self, state, next_state, do_commit=True):
        if not self.db.execute(expression_query_state, (state, next_state)).fetchone():
            self.db.execute(expression_insert_state, (state, next_state))
        if not self.db.execute(expression_query_state_total, (state,)).fetchone():
            self.db.execute(expression_insert_state_total, (state,))
        self.db.execute(expression_add_occurence, (state, next_state))
        self.db.execute(expression_add_occurence_total, (state,))
        if do_commit:
            self.db.commit()

    def get_possibilities(self, state):
        c = self.db.cursor()
        c.execute(expression_query_markov_chain_total, (state,))

        row = c.fetchone()
        if not row:
            return {}
        occurrence = int(row[0])

        sol = {}
        c.execute(expression_query_markov_chain, (state,))
        for row in c:
            sol[row[0]] = int(row[1]) / occurrence

        return sol

    def commit(self):
        self.db.commit()

    def close(self):
        self.db.close()
