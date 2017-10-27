# -*- coding: utf-8 -*-

import json
import requests

class JiraRepository(object):

    def __init__(self, base_url, login, password):
        self.auth = (login, password)
        self.base_url = base_url

# Получение данных о задаче
    def GetIssue(self, issue):
        url = "%s/issue/%s" % (self.base_url, issue)
        resp = requests.get(url, auth=self.auth, verify=False)
        self.data = json.loads(resp.text)
        return self.data