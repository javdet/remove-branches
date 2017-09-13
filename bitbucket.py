#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests


class Bitbucket:

    def __init__(self, base_url, login, password):
        self.auth = (login, password)
        self.base_url = base_url

# Получить список проектов		
    def GetProjects(self):
        url = "%s/projects" % self.base_url
        resp = requests.get(url, auth=self.auth)
        self.data = json.loads(resp.text)
        return self.data

# Получить список репозиториев в проекте	
    def GetRepositories(self, projectkey):
        url = "%s/projects/%s/repos" % (self.base_url, projectkey)
        parameters = dict(
            projectname=projectname
        )
        resp = requests.get(url, auth=self.auth, params=parameters)
        self.data = json.loads(resp.text)
        return self.data

# Получить список веток
    def GetBranches(self, projectkey, reponame):
        url = "%s/projects/%s/repos/%s/branches" % (self.base_url, projectkey, reponame)
        parameters = dict(
            details='true',
            limit=400
        )
        resp = requests.get(url, auth=self.auth, params=parameters)
        self.data = json.loads(resp.text)
        return self.data

# Получить список PR
    def GetPullRequests(self, projectkey, reponame, branchid, state):
        url = "%s/projects/%s/repos/%s/pull-requests" % (self.base_url, projectkey, reponame)
        parameters = dict(
            direction='OUTGOING',
            at=branchid,
            state=state
        )
        resp = requests.get(url, auth=self.auth, params=parameters)
        self.data = json.loads(resp.text)
        return self.data

# Сравнение веток
    def CompareCommits(self, projectkey, reponame, frombranchid, tobranchid):
        url = "%s/projects/%s/repos/%s/compare/commits" % (self.base_url, projectkey, reponame)
        parameters = {
            'from': frombranchid,
            'to': tobranchid
        }
        resp = requests.get(url, auth=self.auth, params=parameters)
        self.data = json.loads(resp.text)
        return self.data