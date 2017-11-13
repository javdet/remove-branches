# -*- coding: utf-8 -*-

import re
from datetime import datetime
from .lib.bitbucket import Bitbucket
from .lib.logger import Logger
from .JiraRepository import JiraRepository
from .configs import config

class BranchService(object):

    def __init__(self):
        self.branch_template = re.compile(config.BRANCH_NAME_TEMPLATE)
        self.division_template = re.compile(config.DIVISION_NAME_TEMPLATE)
        self.logger = Logger(config.LOG_FILE)

    """
    Метод запускает проверки для ветки
    Возвращает структуру:
    {
        "project": 
        "project_key":
        "repo": 
        "name":
        "branch_id": 
        "division": 
        "author": 
        "difference": 
        "isBranchValid": 
        "isBranchMerged": 
        "noBranchDiff": 
        "isTaskClosed": 
        "noBranchDiffToDevelop": 
        "isBranchOlder": 
    }
    """
    def GetMarkForBranch(self, project, repo, branch):
        self.bitbucket = Bitbucket(
            config.BITBUCKET['rest'],
            config.BITBUCKET['user'],
            config.BITBUCKET['password']
        )

        task = self.GetTaskByBranchName(branch['displayId'])
        jira = JiraRepository()
        task_status = jira.GetTaskStatus(task)

        division = self.GetDivision(branch['displayId'])
        author = self.GetAuthor(branch)
        age = self.GetDiffTime(project['name'], repo['name'], branch)
        toref = self.CheckBranchMerge(
            project['key'], 
            repo['name'],
            branch
        )
        diff_develop = self.CompareBranch(
            project, 
            repo,
            branch,
            'develop'
        )
        difference = 1
        if toref:
            difference = self.CompareBranch(
                project, 
                repo,
                branch,
                toref
            )

        result = {
            "project": project['name'],
            "project_key": project['key'],
            "repo": repo['name'],
            "name": branch['displayId'],
            "branch_id": branch['id'],
            "division": division,
            "author": author,
            "difference": difference,
            "isBranchValid": task,
            "isBranchMerged": toref,
            "BranchDiff": difference,
            "isTaskClosed": task_status,
            "BranchDiffToDevelop": diff_develop,
            "isBranchOlder": age
        }
        print(result)
        return result

    """
    Проверка имени ветки на соответствие правилам
    Возвращает ключ задачи или 0
    """
    def GetTaskByBranchName(self, branch):
        if len(self.branch_template.findall(branch)) == 1:
            task_id = "DIRI%s-%s" % (
                self.branch_template.findall(branch)[0][1], 
                self.branch_template.findall(branch)[0][2]
            )
            return task_id
        else:
            return 0

    """
    Получение имени автора ветки
    Возвращает Unknown - если автора нет
    """
    def GetAuthor(self, branch):
        try:
            author = branch['metadata']['com.github.wadahiro.bitbucket.branchauthor:branchAuthor']['author']['displayName']
            return author
        except KeyError:
            return "Unknown"

    """
    Получение идентификатора отдела
    Возвращает код отдела или DIRI525 - по умолчанию
    """
    def GetDivision(self, branch):
        if len(self.division_template.findall(branch)) == 1:
            return "DIRI%s" % self.division_template.findall(branch)[0][1]
        else:
            return "DIRI525"

    """
    Проверка смержена ли ветка
    Возвращает имя ветки назначение или 0
    """
    def CheckBranchMerge(self, project, repo, branch):
        if branch['metadata'].get('com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata'):
            if branch['metadata']['com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata'].get('pullRequest'):
                if branch['metadata']['com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata']['pullRequest']['state'] == "MERGED":
                    return branch['metadata']['com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata']['pullRequest']['toRef']['id']
                else:
                    return 0
            # Для случаев, когда мержилось несколько раз
            elif branch['metadata']['com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata']['merged']:
                pr = self.bitbucket.GetPullRequests(
                    project, 
                    repo, 
                    branch['id'], 
                    'MERGED'
                )
                return pr['values'][0]['toRef']['id']
            else:
                return 0
        else:
            return 0

    """
    Сравнение веток
    Возвращает 0 - нет изменений, 1 - есть
    """
    def CompareBranch(self, project, repo, branch, toref):
        compare = self.bitbucket.CompareCommits(
            project['key'],
            repo['name'],
            branch['id'],
            toref
        )
        if compare.get('errors'):
            message = "%s %s %s Error: %s" % (
                project['name'], 
                repo['name'], 
                branch['displayId'], 
                compare['errors'][0]['message']
            )
            self.logger.Write(message)
            return 1
        if compare['size'] == 0:
            return(compare['size'])
        else:
            return 1

    """
    Проверка старше ли ветка 30 дней
    Возвращает 1 - да, 0 - нет
    """
    def GetDiffTime(self, project, repo, branch):
        try:
            tdiff = datetime.now() - datetime.fromtimestamp(
                int(str(branch['metadata']['com.atlassian.bitbucket.server.bitbucket-branch:latest-commit-metadata']['authorTimestamp'])[0:10])
            )
        except KeyError as e:
            message = "%s %s %s Key Error: %s" % (project, repo, branch, str(e))
            self.logger.Write(message)
            return 0
        if tdiff.days > 30:
            return 1
        else:
            return 0

    """
    Сравнение с условиями и выставления флагов
    """
    def GetBranchByCondition(self, branch_item):
        branch_item['action'] = "no"
        branch_result = self.GetBranchByConditionDeletion(branch_item)
        branch_result = self.GetBranchByConditionNotification(branch_item)
        print(branch_result)
        return branch_result

    def GetBranchByConditionDeletion(self, branch_item):
        for condition in config.DELETE_CONDITIONS:
            success_condition_count = 0
            for condition_item in condition:
                if branch_item[condition_item]:
                    success_condition_count += 1

            if len(condition) == success_condition_count:
                message = "%s %s %s Branch delete" % (
                    branch_item['project'], 
                    branch_item['repo'], 
                    branch_item['name']
                )
                self.logger.Write(message)
                branch_item['action'] = "delete"
                break
        return branch_item
    
    def GetBranchByConditionNotification(self, branch_item):
        for condition in config.NOTIFY_CONDITIONS:
            success_condition_count = 0
            for condition_item in config.NOTIFY_CONDITIONS[condition]:
                if branch_item[condition_item]:
                    success_condition_count += 1

            if len(config.NOTIFY_CONDITIONS[condition]) == success_condition_count:
                message = "%s %s %s Branch sendmail" % (
                    branch_item['project'], 
                    branch_item['repo'], 
                    branch_item['name']
                )
                self.logger.Write(message)
                branch_item['action'] = "notify"
                break
        return branch_item
