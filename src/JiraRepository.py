# -*- coding: utf-8 -*-

from .configs import config
from .lib.jira import Jira
from .lib.logger import Logger

class JiraRepository(object):

    def __init__(self):
        self.jira = Jira(
            config.JIRA['rest'], 
            config.JIRA['user'], 
            config.JIRA['password']
        )

    def GetTaskStatus(self, task):
        """
        Проверка статуса задачи
        :return: 1 - если задача закрыта, 0 - нет
        """
        
        if task != 0:
            issue = self.jira.GetIssue(task)
            if issue.get('errorMessages'):
                message = "%s Error: %s" % (task, str(issue['errorMessages']))
                logger = Logger(config.LOG_FILE)
                logger.Write(message)
                logger.Close()
                return 0

            if issue['fields']['status']['id'] == "6":
                return 1
        return 0
