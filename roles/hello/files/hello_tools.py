"""
hellostats sample API
author: Alex G.S.

Utils for use by the hello app such as html formatting
getting loadavg of the server and ipaddress

"""

import os, socket, re
import requests
import json

# server tools and stats

def get_ip():
    """get the ip address for the server"""
    aws_url="http://169.254.169.254/latest/meta-data/public-ipv4"
    pub_ip = requests.get(aws_url).text
    return pub_ip

def get_stats():
    """return ip and loadavg as a tuple"""
    loada, loadb, loadc = os.getloadavg()
    stats = [get_ip(), loada, loadb, loadc]
    return stats

def json_stats():
    """return stats as JSON list with ip as key"""
    stats = get_stats()
    return json.dumps(stats)

def node_list():
    """get the list of nodes from the host list excluding localhost"""
    host_file = "/var/www/hello/hosts.list"
    if os.path.exists(host_file):
        try:
            with open(host_file, 'r') as hostfile:
                host_list = [h.strip() for h in hostfile.readlines() if h.strip() != get_ip()]
        except:
            return "ERROR: could not access host list!"
        else:
            return host_list
    else:
        return "ERROR: host list is missing!"

def node_stats():
    """get the loadavg stats from the entire cluster"""
    node_stats = list()
    node_stats.append(get_stats())
    if len(node_list()) > 0:
        for node in node_list():
            url = "http://{}/loadavg".format(node)
            try:
                resp = requests.get(url)
            except:
                return "ERROR: problem talking to node!"
            else:
                raw = re.sub(r'<h1>|</h1>|\s', '', resp.text)
                stats = re.split(r':|,', raw)
                node_stats.append(stats)
    else:
        return "ERROR: no nodes in the host list!"
    return node_stats

def node_avg():
    """get the avg of the node stats"""
    node_raw = ["average", 0, 0, 0]
    for node in node_stats():
        node_raw[1] += float(node[1])
        node_raw[2] += float(node[2])
        node_raw[3] += float(node[3])

    num = len(node_stats())
    node_avg = ["average",
            "{:.2f}".format(node_raw[1]/num),
            "{:.2f}".format(node_raw[2]/num),
            "{:.2f}".format(node_raw[3]/num)]
    return node_avg

# html formatters

def wrap_h(msg):
    """wraps text in a header tag for good desploy"""
    return "<h1>{}</h1>".format(msg)

def wrap_p(msg):
    """wraps text in a paragraph tag for good desploy"""
    return "<p>{}</p>".format(msg)
