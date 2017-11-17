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

    def GetDataForBranch(self, project, repo, branch):
        """
        Метод получает данные для ветки
        :return:
        {
            "project": 
            "project_key":
            "repo": 
            "name":
            "task":
            "branch_id": 
            "division": 
            "author": 
            "target_branch":
            "task_status":
            "diff_to_target":
            "diff_to_develop":
            "age": 
        }
        """

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
        target_branch = self.CheckBranchMerge(
            project['key'], 
            repo['name'],
            branch
        )
        diff_to_develop = self.CompareBranch(
            project, 
            repo,
            branch,
            'develop'
        )
        diff_to_target = self.CompareBranch(
                project, 
                repo,
                branch,
                target_branch
        )

        result = {
            "project": project['name'],
            "project_key": project['key'],
            "repo": repo['name'],
            "name": branch['displayId'],
            "branch_id": branch['id'],
            "task": task,
            "division": division,
            "author": author,
            "target_branch": target_branch,
            "task_status": task_status,
            "diff_to_target": diff_to_target,
            "diff_to_develop": diff_to_develop,
            "age": age
        }
        print(result)
        return result

    def GetFlagsForBranch(self, branch):
        """
        Метод запускает установку флагов для ветки
        :return:
        {
            "project": 
            "project_key":
            "repo": 
            "name":
            "branch_id": 
            "division": 
            "author": 
            "isBranchMerged": 
            "noBranchDiff": 
            "noBranchDiffToDevelop": 
            "isTaskClosed": 
            "noExistTargetBranch": 
            "noBranchValid":
            "isBranchOlder":
            "noTaskExist":
        }
        """

        isBranchMerged = 0
        noBranchDiff = 0
        noBranchDiffToDevelop = 0
        isTaskClosed = 0
        noExistTargetBranch = 0
        noBranchValid = 0
        isBranchOlder = 0
        noTaskExist = 0
                
        if branch['target_branch'] is not None:
            isBranchMerged = 1
        if branch['diff_to_target'] == 0:
            noBranchDiff = 1
        if branch['diff_to_develop'] == 0:
            noBranchDiffToDevelop = 1
        if branch['task_status'] == 6:
            isTaskClosed = 1
        if branch['task_status'] is not None:
            noTaskExist = 1
        if branch['diff_to_target'] is not None:
            noExistTargetBranch = 1
        if branch['task'] is not None:
            noBranchValid = 1
        if branch['age'] > 30:
            isBranchOlder = 1


        result = {
            "project": branch['project'],
            "project_key": branch['project_key'],
            "repo": branch['repo'],
            "name": branch['name'],
            "branch_id": branch['branch_id'],
            "division": branch['division'],
            "author": branch['author'],
            "isBranchMerged": isBranchMerged,
            "noBranchDiff": noBranchDiff,
            "noBranchDiffToDevelop": noBranchDiffToDevelop,
            "isTaskClosed": isTaskClosed,
            "noExistTargetBranch": noExistTargetBranch,
            "noBranchValid": noBranchValid,
            "isBranchOlder": isBranchOlder,
            "noTaskExist": noTaskExist
        }
        print(result)
        return result

    def GetTaskByBranchName(self, branch):
        """
        Проверка имени ветки на соответствие правилам
        :return: ключ задачи или None
        """

        if len(self.branch_template.findall(branch)) == 1:
            task_id = "DIRI%s-%s" % (
                self.branch_template.findall(branch)[0][1], 
                self.branch_template.findall(branch)[0][2]
            )
            return task_id
        else:
            return None

    def GetAuthor(self, branch):
        """
        Получение имени автора ветки
        :return: Unknown - если автора нет
        """

        try:
            author = branch['metadata']['com.github.wadahiro.bitbucket.branchauthor:branchAuthor']['author']['displayName']
            return author
        except KeyError:
            return "Unknown"

    def GetDivision(self, branch):
        """
        Получение идентификатора отдела
        :return: код отдела или DIRI525 - по умолчанию
        """

        if len(self.division_template.findall(branch)) == 1:
            return "DIRI%s" % self.division_template.findall(branch)[0][1]
        else:
            return "DIRI525"

    def CheckBranchMerge(self, project, repo, branch):
        """
        Проверка смержена ли ветка
        :return: имя ветки назначения или None
        """

        if branch['metadata'].get('com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata'):
            if branch['metadata']['com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata'].get('pullRequest'):
                if branch['metadata']['com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata']['pullRequest']['state'] == "MERGED":
                    return branch['metadata']['com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata']['pullRequest']['toRef']['id']
            # Для случаев, когда мержилось несколько раз
            elif branch['metadata']['com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata']['merged']:
                pr = self.bitbucket.GetPullRequests(
                    project, 
                    repo, 
                    branch['id'], 
                    'MERGED'
                )
                return pr['values'][0]['toRef']['id']
            
        return None

    def CompareBranch(self, project, repo, branch, toref):
        """
        Сравнение веток
        :return: 0 - нет изменений, >1 - есть, None - нет ветки
        """

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
            return None
        
        return(compare['size'])

    def GetDiffTime(self, project, repo, branch):
        """
        Проверка старше ли ветка 30 дней
        :return: число дней, None - не удалось определить
        """

        try:
            tdiff = datetime.now() - datetime.fromtimestamp(
                int(str(branch['metadata']['com.atlassian.bitbucket.server.bitbucket-branch:latest-commit-metadata']['authorTimestamp'])[0:10])
            )
        except KeyError as e:
            message = "%s %s %s Key Error: %s" % (project, repo, branch['displayId'], str(e))
            self.logger.Write(message)
            return None
        
        return tdiff.days

    def GetBranchForDeletion(self, map_by_branch):
        """
        Сравнение с условиями на удаление
        возвращает только список веток для удаления
        :return:
        [
            {
                "project": 
                "project_key":
                "repo": 
                "name":
                "branch_id": 
                "division": 
                "author": 
            },
            {...}
        ]
        """

        deletion_list = []
        for branch_item in map_by_branch:
            for condition in config.DELETE_CONDITIONS:
                delete_branch = self.CheckBranchConditionDeletion(
                    branch_item, 
                    condition
                )
                if delete_branch is not None:
                    deletion_list.append(
                        delete_branch
                    )
                    break

        return deletion_list

    def CheckBranchConditionDeletion(self, branch_item, condition):
        """
        Возвращает параметры ветки для удаления
        :return: none или
        {
            "project": 
            "project_key":
            "repo": 
            "name":
            "branch_id": 
            "division": 
            "author":
        }
        """

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
            result = {
                "project": branch_item['project'],
                "project_key": branch_item['project_key'],
                "repo": branch_item['repo'], 
                "name": branch_item['name'],
                "branch_id": branch_item['branch_id'],
                "division": branch_item['division'],
                "author": branch_item['author']
            }
            return result
        return None
        
    def GetBranchForNotify(self, map_by_branch):
        """
        Сравнение с условиями на оповещение
        возвращает только список веток для оповещения
        :return:
        [
            {
                "project": 
                "project_key":
                "repo": 
                "name":
                "branch_id": 
                "division": 
                "author":
                "message":
            },
            {...}
        ]
        """

        notify_list = []
        for branch_item in map_by_branch:
            for condition in config.NOTIFY_CONDITIONS:
                notify_branch = self.CheckBranchConditionNotify(
                    branch_item, 
                    condition
                )
                if notify_branch is not None:
                    notify_list.append(
                        notify_branch    
                    )
                    break

        return notify_list

    def CheckBranchConditionNotify(self, branch_item, condition):
        """
        Возвращает параметры ветки для оповещения
        :return: none или
        {
            "project": 
            "project_key":
            "repo": 
            "name":
            "branch_id": 
            "division": 
            "author":
            "message":
        }
        """

        success_condition_count = 0
        for condition_item in config.NOTIFY_CONDITIONS[condition]:
            if branch_item[condition_item]:
                success_condition_count += 1

        if len(config.NOTIFY_CONDITIONS[condition]) == success_condition_count:
            message = "%s %s %s Branch sendmail %s" % (
                branch_item['project'], 
                branch_item['repo'], 
                branch_item['name'],
                branch_item['message']
            )
            self.logger.Write(message)
            result = {
                "project": branch_item['project'],
                "project_key": branch_item['project_key'],
                "repo": branch_item['repo'], 
                "name": branch_item['name'],
                "branch_id": branch_item['branch_id'],
                "division": branch_item['division'],
                "author": branch_item['author'],
                "message": condition
            }
            return result
        return None
