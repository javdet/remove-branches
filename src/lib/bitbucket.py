# -*- coding: utf-8 -*-

import json
import requests


class Bitbucket(object):

    def __init__(self, base_url, login, password):
        self.auth = (login, password)
        self.base_url = base_url
        self.headers = {
                        'Content-Type': 'application/json'
    }

    def GetProjects(self):
        """
        Метод возвращает список проектов в bitbucket
        """

        url = "%s/api/1.0/projects" % self.base_url
        resp = requests.get(url, auth=self.auth, headers=self.headers)
        self.data = json.loads(resp.text)
        return self.data

    def GetRepositories(self, projectkey):
        """
        Метод возвращает список репозиториев в проекте
        """

        url = "%s/api/1.0/projects/%s/repos" % (self.base_url, projectkey)
        resp = requests.get(url, auth=self.auth, headers=self.headers)
        self.data = json.loads(resp.text)
        return self.data

    def GetBranches(self, projectkey, reponame):
        """
        Метод возвращает список веток в репозитории
        """

        url = "%s/api/1.0/projects/%s/repos/%s/branches" % (self.base_url, projectkey, reponame)
        parameters = dict(
            details='true',
            limit=100
        )
        resp = requests.get(url, auth=self.auth, params=parameters, headers=self.headers)
        self.data = json.loads(resp.text)
        return self.data

    def GetBranch(self, projectkey, reponame, branchname):
        """
        Метод возвращает данные по одной конкретной ветке
        """

        url = "%s/api/1.0/projects/%s/repos/%s/branches" % (self.base_url, projectkey, reponame)
        parameters = dict(
            details='true',
            filterText=branchname
        )
        resp = requests.get(url, auth=self.auth, params=parameters, headers=self.headers)
        self.data = json.loads(resp.text)
        return self.data


    def GetPullRequests(self, projectkey, reponame, branchid, state):
        """
        Метод возвращает данные по PR
        """

        url = "%s/api/1.0/projects/%s/repos/%s/pull-requests" % (self.base_url, projectkey, reponame)
        parameters = dict(
            direction='OUTGOING',
            at=branchid,
            state=state
        )
        resp = requests.get(url, auth=self.auth, params=parameters, headers=self.headers)
        self.data = json.loads(resp.text)
        return self.data

    def CompareCommits(self, projectkey, reponame, frombranchid, tobranchid):
        """
        Метод возвращает результат сравнения двух веток
        """

        url = "%s/api/1.0/projects/%s/repos/%s/compare/commits" % (self.base_url, projectkey, reponame)
        parameters = {
            'from': frombranchid,
            'to': tobranchid
        }
        resp = requests.get(url, auth=self.auth, params=parameters, headers=self.headers)
        self.data = json.loads(resp.text)
        return self.data

    def DeleteBranch(self, projectkey, reponame, branchid):
        """
        Метод производит удаление ветки
        """

        url = "%s/branch-utils/1.0/projects/%s/repos/%s/branches" % (self.base_url, projectkey, reponame)
        parameters = dict (
            name=branchid,
            dryRun="false"
        )
        resp = requests.delete(url, auth=self.auth, json=parameters, headers=self.headers)
        return resp