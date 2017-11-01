# -*- coding: utf-8 -*-

from ..configs import config
from ..lib.jira import Jira
from ..lib.logger import Logger

class JiraRepository(object):

    def __init__(self):
        self.jira = Jira(
            config.JIRA['rest'], 
            config.JIRA['user'], 
            config.JIRA['password']
        )

    # Проверка статуса задачи
    def GetTaskStatus(self, task):
        issue = self.jira.GetIssue(task)
        if issue.get('errorMessages'):
            message = "%s Error: %s" % (task, str(issue['errorMessages']))
            logger = Logger(config.LOG_FILE)
            logger.Write(message)
            logger.close()
            return -1
        else:
            if issue['fields']['status']['id'] == "6":
                return 1
            else:
                return 0
