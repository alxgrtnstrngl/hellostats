"""
hellostats sample API
author: Alex G.S.

Simple app that returns 'Hello' and some other useful
stats and information about the server it's running on

"""

import os, socket
import hello_tools as htools
import hello_db as hdb
from flask import Flask
from flask import request
app = Flask(__name__)

@app.route("/")
def hello_world():
    """this is a check to show that the apps works"""
    return htools.wrap_h("This Works!")

@app.route("/hello")
def hello_name():
    """return 'Hello NAME' for /?name=NAME"""
    name = request.args.get('name', '').capitalize()
    hdb.insert_name(name)
    return htools.wrap_h("Hello {}!".format(name))

@app.route("/counts")
def hello_counts():
    """get the counts of all names submitted"""
    names = hdb.list_names()
    name_h = ""
    for n in names:
        name_h += htools.wrap_p("{}: {} ".format(n[0],n[1]))
    return name_h

@app.route("/loadavg")
def os_info():
    """returns the load avg for the server as a stat"""
    stats = htools.get_stats()
    stats_msg = htools.wrap_h(str(stats[0]) + ": " +
            str(stats[1]) + ", " + str(stats[2]) + ", " + str(stats[3]))
    return stats_msg

@app.route("/nodestats")
def nodes_info():
    """returns the load avg for all nodes in the cluster"""
    node_stats = htools.node_stats()
    stats_msg = ""
    for stats in node_stats:
        stats_msg += htools.wrap_p(str(stats[0]) + ": " +
                str(stats[1]) + ", " + str(stats[2]) + ", " + str(stats[3]))
    stats_avg = htools.node_avg()
    stats_msg += htools.wrap_p(str(stats_avg[0]) + ": " +
                str(stats_avg[1]) + ", " + str(stats_avg[2]) + ", " + str(stats_avg[3]))
    return stats_msg

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
