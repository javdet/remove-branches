#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import config
from datetime import datetime
from bitbucket import Bitbucket


def logger(message):
    date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    f = open(config.LOG_FILE, 'a')
    f.write(date+" "+message+"\n")
    f.close

bb = Bitbucket(config.BASE_URL, config.USER, config.PASS)
projects = bb.GetProjects()
for project in projects['values']:
    if project['name'].encode('utf8') in config.exclude_projects:
        continue

    print(project['key'], project['name'])
    repos = bb.GetRepositories(project['name'])
    for repo in repos['values']:
        print(repo['name'])
        branches = bb.GetBranches(project['key'], repo['name'])
        test = bb.GetBranchesTest('PLAN', 'planeta.tc')
        print(test)
