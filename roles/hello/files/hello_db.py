"""
hellostats sample API
author: Alex G.S.

Some simple sql functions to insert a name and
to get a final count of all names submitted

"""

import sqlite3
from os import path

def insert_name(name):
    """insert a name into the db with a timestamp"""
    app_path="/var/www/hello/hello.db"
    tmp_path="/tmp/hello.db"
    if path.exists(app_path):
        db = app_path
    elif path.exists(tmp_path):
        db = tmp_path
    else:
        db = "NOT_FOUND"
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("insert into names values ('{}')".format(name))
    except:
        return "ERROR: problem with local database!"
    else:
        conn.commit()
    finally:
        conn.close()

def list_names():
    """get a list of names and their counts"""
    app_path="/var/www/hello/hello.db"
    tmp_path="/tmp/hello.db"
    if path.exists(app_path):
        db = app_path
    elif path.exists(tmp_path):
        db = tmp_path
    else:
        db = "NOT_FOUND"
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("select name, count(name) from names group by name")
        result = c.fetchall()
        namelist = [(r[0],r[1]) for r in result]
    except:
        conn.close()
        return "ERROR: problem with local database!"
    else:
        conn.close()
        return namelist

