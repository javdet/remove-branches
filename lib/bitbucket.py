# -*- coding: utf-8 -*-

import json
import requests


class BitbucketRepository(object):

    def __init__(self, base_url, login, password):
        self.auth = (login, password)
        self.base_url = base_url
        self.headers = {
                        'Content-Type': 'application/json'
    }

# Получить список проектов
    def GetProjects(self):
        url = "%s/api/1.0/projects" % self.base_url
        resp = requests.get(url, auth=self.auth, headers=self.headers)
        self.data = json.loads(resp.text)
        return self.data

# Получить список репозиториев в проекте	
    def GetRepositories(self, projectkey):
        url = "%s/api/1.0/projects/%s/repos" % (self.base_url, projectkey)
        resp = requests.get(url, auth=self.auth, headers=self.headers)
        self.data = json.loads(resp.text)
        return self.data

# Получить список веток
    def GetBranches(self, projectkey, reponame):
        url = "%s/api/1.0/projects/%s/repos/%s/branches" % (self.base_url, projectkey, reponame)
        parameters = dict(
            details='true',
            limit=400
        )
        resp = requests.get(url, auth=self.auth, params=parameters, headers=self.headers)
        self.data = json.loads(resp.text)
        return self.data

# Получить данные по одной ветке
    def GetBranch(self, projectkey, reponame, branchname):
        url = "%s/api/1.0/projects/%s/repos/%s/branches" % (self.base_url, projectkey, reponame)
        parameters = dict(
            details='true',
            filterText=branchname
        )
        resp = requests.get(url, auth=self.auth, params=parameters, headers=self.headers)
        self.data = json.loads(resp.text)
        return self.data

# Получить список PR
    def GetPullRequests(self, projectkey, reponame, branchid, state):
        url = "%s/api/1.0/projects/%s/repos/%s/pull-requests" % (self.base_url, projectkey, reponame)
        parameters = dict(
            direction='OUTGOING',
            at=branchid,
            state=state
        )
        resp = requests.get(url, auth=self.auth, params=parameters, headers=self.headers)
        self.data = json.loads(resp.text)
        return self.data

# Сравнение веток
    def CompareCommits(self, projectkey, reponame, frombranchid, tobranchid):
        url = "%s/api/1.0/projects/%s/repos/%s/compare/commits" % (self.base_url, projectkey, reponame)
        parameters = {
            'from': frombranchid,
            'to': tobranchid
        }
        resp = requests.get(url, auth=self.auth, params=parameters, headers=self.headers)
        self.data = json.loads(resp.text)
        return self.data

# Удаление ветки
    def DeleteBranch(self, projectkey, reponame, branchid):
        url = "%s/branch-utils/1.0/projects/%s/repos/%s/branches" % (self.base_url, projectkey, reponame)
        parameters = dict (
            name=branchid,
            dryRun="false"
        )
        resp = requests.delete(url, auth=self.auth, json=parameters, headers=self.headers)
        return resp