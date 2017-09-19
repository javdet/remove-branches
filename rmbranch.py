#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import config
import re
from datetime import datetime
from bitbucket import Bitbucket
from jira import Jira
from mail import Mail

branch_template = re.compile("^(.*)/DIRI(\w+)-(\d+)$")

# Логирование
def logger(message):
    date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    f = open(config.LOG_FILE, 'a')
    f.write(date+" "+message.encode('utf-8')+"\n")
    f.close

# Проверка корректности имени
def check_branch_name(project, repo, branch):
    if len(branch_template.findall(branch)) == 1:
        task_id = "DIRI%s-%s" % (branch_template.findall(branch)[0][1], branch_template.findall(branch)[0][2])
        return task_id
    else:
        message = "%s %s %s Branch name is not valid" % (project, repo, branch)
        logger(message)
        return 0

# Проверка статуса задачи
def check_task_status(task):
    jira = Jira(config.BASE_URL_JIRA, config.USER_JIRA, config.PASS_JIRA)
    issue = jira.GetIssue(task)
    if issue.get('errorMessages'):
        message = "%s Error: %s" % (task, str(issue['errorMessages']))
        logger(message)
        return -1
    else:
        if issue['fields']['status']['id'] == "6":
            return 1
        else:
            return 0

# Форматирование данных
def preparing(project, repo, branch):
    content = """
<tr>
<td>%s</td>
<td>%s</td>
<td>%s</td>
</tr>
""" % (project, repo, branch)
    return content

# Проверка смержена ли ветка
def check_branch_merge(bb, project, repo, branch):
    if branch['metadata'].get('com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata'):
        if branch['metadata']['com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata'].get('pullRequest'):
            if branch['metadata']['com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata']['pullRequest']['state'] == "MERGED":
#                print(branch['displayId'], 
#                    branch['id'], 
#                    branch['latestCommit'], 
#                    branch['metadata']['com.atlassian.bitbucket.server.bitbucket-branch:ahead-behind-metadata-provider']['ahead'],
#                    branch['metadata']['com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata']['pullRequest']['state'],
#                    branch['metadata']['com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata']['pullRequest']['toRef']['displayId'],
#                    branch['metadata']['com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata']['pullRequest']['toRef']['id']
#                )
                compare = bb.CompareCommits(project['key'], 
                            repo['name'], 
                            branch['id'], 
                            branch['metadata']['com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata']['pullRequest']['toRef']['id']
                )
                if compare.get('errors'):
                    message = "%s %s %s Error: %s" % (project['name'], repo['name'], branch['displayId'], compare['errors'][0]['message'])
                    logger(message)
                    return -1
#                print(compare)
                return(compare['size'])
        elif branch['metadata']['com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata']['merged']:
            pr = bb.GetPullRequests(project['key'], repo['name'], branch['id'], 'MERGED')
#            print(branch['id'], pr)
#            print(branch['displayId'], 
#                branch['id'], 
#                branch['latestCommit'], 
#                branch['metadata']['com.atlassian.bitbucket.server.bitbucket-branch:ahead-behind-metadata-provider']['ahead'],
#                pr['values'][0]['toRef']['id']
#            )
            compare = bb.CompareCommits(project['key'], 
                        repo['name'], 
                        branch['id'], 
                        pr['values'][0]['toRef']['id']
            )
            if compare.get('errors'):
                message = "%s %s %s Error: %s" % (project['name'], repo['name'], branch['displayId'], compare['errors'][0]['message'])
                logger(message)
                return -1
#            print(compare)
            return(compare['size'])
    else:
        return -2


def main():
    logger("Start")
    bb = Bitbucket(config.BASE_URL_BITBUCKET, config.USER_BITBUCKET, config.PASS_BITBUCKET)
    projects = bb.GetProjects()

    msg_invalidname = ""
    msg_delete = ""
    msg_check = ""

    for project in projects['values']:
        if project['name'].encode('utf8') in config.exclude_projects:
            continue

        print(project['key'], project['name'])
        repos = bb.GetRepositories(project['key'])

        for repo in repos['values']:
            if repo['name'].encode('utf8') in config.exclude_repo:
                continue
        
            print(repo['name'])
            branches = bb.GetBranches(project['key'], repo['name'])

            for branch in branches['values']:
                if branch['displayId'] in config.exclude_branches:
                    continue
                task = check_branch_name(project['name'], repo['name'], branch['displayId'])
                if task:
                    branch_size = check_branch_merge(bb, project, repo, branch)
                    if branch_size == 0:
                        task_status = check_task_status(task)
                        if task_status:
                            if config.NOTIFY:
                                bb.DeleteBranch(project['key'], repo['name'], branch['displayId'])
                            msg_delete = msg_delete + preparing(project['name'], repo['name'], branch['displayId']).encode('utf-8')
                    elif branch_size == -1:
                        print("Not dest branch", project['name'], repo['name'], branch['displayId'])
                    elif branch_size > 0 or branch_size == -2:
                        try:
                            tdiff = datetime.now() - datetime.fromtimestamp(int(str(branch['metadata']['com.atlassian.bitbucket.server.bitbucket-branch:latest-commit-metadata']['authorTimestamp'])[0:10]))
                        except KeyError, e:
                            message = "%s %s %s Error: %s" % (project['name'], repo['name'], branch['displayId'], str(e))
                            logger(message)
                            continue
                        if tdiff.days > 30:
                            msg_check = msg_check + preparing(project['name'], repo['name'], branch['displayId']).encode('utf-8')
#                        print("Difference is %d days %d hours" % (tdiff.days, tdiff.seconds/3600))
                else:
                   msg_invalidname = msg_invalidname + preparing(project['name'], repo['name'], branch['displayId']).encode('utf-8')

    # Информирование о невалидных именах
    smtp = Mail(config.MAIL['smtp'], config.MAIL['fromaddr'])
    smtp.Send("invalid_name", config.MAIL['test'], msg_invalidname)
    smtp.close()

    # Информирование о ветках к удалению
    smtp = Mail(config.MAIL['smtp'], config.MAIL['fromaddr'])
    smtp.Send("delete", config.MAIL['test'], msg_delete)
    smtp.close()
    
    # Информирование о старых ветках
    smtp = Mail(config.MAIL['smtp'], config.MAIL['fromaddr'])
    smtp.Send("check", config.MAIL['test'], msg_check)
    smtp.close()
    logger("Stop")

if __name__ == "__main__": 
    main()