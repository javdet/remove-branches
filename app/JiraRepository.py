# -*- coding: utf-8 -*-

class JiraRepository(object):

    # Проверка статуса задачи
    def check_task_status(task):
        jira = Jira(config.BASE_URL_JIRA, config.USER_JIRA, config.PASS_JIRA)
        issue = jira.GetIssue(task)
        if issue.get('errorMessages'):
            message = "%s Error: %s" % (task, str(issue['errorMessages']))
            logger.Write(message)
            return -1
        else:
            if issue['fields']['status']['id'] == "6":
                return 1
            else:
                return 0
