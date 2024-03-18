import os
import sqlite3

from os.path import join
BUILD_PATH = join(".", "db", "build.sql")

DB_PATH = "your_database_name.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

def with_commit(func):
    def inner(*args, **kwargs):
        v = func(*args, **kwargs)
        commit()
        return v
    return inner

@with_commit
def build():
    scriptexec(BUILD_PATH)

def close():
    cur.close()
    conn.close()

def commit():
    conn.commit()

def field(command, *values):
    cur.execute(command, tuple(values))
    fetch = cur.fetchone()
    if fetch is not None:
        return fetch[0]

def record(command, *values):
    cur.execute(command, tuple(values))
    return cur.fetchone()

def records(command, *values):
    cur.execute(command, tuple(values))
    return cur.fetchall()

def column(command, *values):
    cur.execute(command, tuple(values))
    return [item[0] for item in cur.fetchall()]

def execute(command, *values):
    cur.execute(command, tuple(values))

def executeF1(command, *values):
    cur.execute(command, tuple(values))
    return cur.fetchone()

def executeFAll(command, *values):
    cur.execute(command, tuple(values))
    return cur.fetchall()

def scriptexec(path):
    with open(path, "r", encoding="utf-8") as script:
        script_content = script.read()
        # Split the script into separate statements on each semicolon
        statements = script_content.split(';')
        for statement in statements:
            if statement.strip():  # Make sure it's not an empty statement
                cur.execute(statement)
    print("SQLite Ran", path)
