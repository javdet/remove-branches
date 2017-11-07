# -*- coding: utf-8 -*-

import re
from datetime import datetime
from ..lib.Bitbucket import Bitbucket
from JiraRepository import JiraRepository
from ..configs import config

class BranchService(object):

    def __init__(self):
        self.branch_template = re.compile(config.BRANCH_NAME_TEMPLATE)
        self.division_template = re.compile(config.DIVISION_NAME_TEMPLATE)

    # Формирование объекта ветки, с необходимыми параметрами
    def GetMarkForBranch(self, project, repo, branch):
        task = self.GetTaskByBranchName(branch['displayId'])
        division = self.GetDivision(branch['displayId'])
        author = self.GetAuthor(branch)
        age = GetAge(branch)

        mapper1 = lambda x: 1 if x else 0
        mapper2 = lambda x: 1 if x == 0 else 0

        toref = self.CheckBranchMerge(
            project['key'], 
            repo['name'],
            branch
        )

        diffDevelop = self.CompareBranch(
            project['key'], 
            repo['name'],
            branch,
            'develop'
        )

        jr = JiraRepository()
        task_status = jr.GetTaskStatus(task)

        isTaskClosed = mapper1(task_status)
        isBranchValid = mapper1(task)
        noBranchDiffToDevelop = mapper2(diffDevelop)
        
        if toref:
            isBranchMerged = 1
            difference = self.CompareBranch(
                project['key'], 
                repo['name'],
                branch,
                toref
            )
        else:
            isBranchMerged = 0
            difference = -2

        noBranchDiff = mapper2(difference)
        isBranchOlder = mapper1(age)

        result = {
            "project": project['name'],
            "project_key": project['key'],
            "repo": repo['name'],
            "name": branch['displayId'],
            "branch_id": branch['id'],
            "division": division,
            "author": author,
            "difference": difference
            "isBranchValid": isBranchValid,
            "isBranchMerged": isBranchMerged,
            "noBranchDiff": noBranchDiff
            "isTaskClosed": isTaskClosed,
            "noBranchDiffToDevelop": noBranchDiffToDevelop,
            "isBranchOlder": isBranchOlder
        }
        return result

    # Проверка корректности имени
    def GetTaskByBranchName(self, branch):
        if len(self.branch_template.findall(branch)) == 1:
            task_id = "DIRI%s-%s" % (
                self.branch_template.findall(branch)[0][1], 
                self.branch_template.findall(branch)[0][2]
            )
            return task_id
        else:
            return 0

    # Получение имени автора ветки
    def GetAuthor(self, branch):
        try:
            author = branch['metadata']['com.github.wadahiro.bitbucket.branchauthor:branchAuthor']['author']['displayName']
            return author
        except KeyError:
            return "Unknown"

    # Получение имени отдела
    def GetDivision(self, branch):
        if len(self.division_template.findall(branch)) == 1:
            return "DIRI%s" % division_template.findall(branch)[0][1]
        else:
            return "DIRI525"

    # Проверка смержена ли ветка
    def CheckBranchMerge(self, project, repo, branch):
        if branch['metadata'].get('com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata'):
            if branch['metadata']['com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata'].get('pullRequest'):
                if branch['metadata']['com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata']['pullRequest']['state'] == "MERGED":
                    return branch['metadata']['com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata']['pullRequest']['toRef']['id']
                else:
                    return 0
            # Для случаев, когда мержилось несколько раз
            elif branch['metadata']['com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata']['merged']:
                pr = bb.GetPullRequests(project['key'], repo['name'], branch['id'], 'MERGED')
                return pr['values'][0]['toRef']['id']
            else:
                return 0
        else:
            return 0

    # Сравнение веток
    def CompareBranch(self, project, repo, branch, toref):
        compare = bb.CompareCommits(project['key'],
                            repo['name'],
                            branch['id'],
                            toref
                 )
        if compare.get('errors'):
            message = "%s %s %s Error: %s" % (project['name'], repo['name'], branch['displayId'], compare['errors'][0]['message'])
            logger.Write(message)
            return -1
        return(compare['size'])

    def GetAge(self, branch):
        try:
            tdiff = datetime.now() - datetime.fromtimestamp(
                int(str(branch['metadata']['com.atlassian.bitbucket.server.bitbucket-branch:latest-commit-metadata']['authorTimestamp'])[0:10])
            )
        except KeyError, e:
            message = "%s %s %s Key Error: %s" % (project['name'], repo['name'], branch['displayId'], str(e))
            logger.Write(message)
            return 0
        if tdiff.days > 30:
            return 1
        else:
            return 0