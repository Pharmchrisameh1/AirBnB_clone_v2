#!/usr/bin/python3
"""This module defines the function do_clean
"""
from fabric.api import *


env.hosts = ['34.207.212.22', '54.237.31.63']
env.user = 'ubuntu'


def do_clean(number=0):
    """This function deletes out-of-date archives
    """
    output = local("ls -lt ./versions/", capture=True)
    output = output.split('\n')
    output.pop(0)
    number = int(number)
    if number == 0:
        number = 1
    i = number
    while i <= (len(output) - 1):
        filename = output[i].split(' ')[-1]
        local("rm -rf ./versions/{}".format(filename))
        i += 1

    output = sudo("ls -lt /data/web_static/releases")
    output = output.split('\n')
    output.pop(0)
    i = number
    delstr = ""
    while i <= (len(output) - 1):
        fil = output[i].split(' ')[-1].replace('\r', '')
        filename = " /data/web_static/releases/" + fil + " "
        delstr += filename
        i += 1
    sudo("rm -rf {}".format(delstr))
