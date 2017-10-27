#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
from datetime import datetime
from configs import config
from lib.bitbucket import BitbucketRepository
from lib.jira import JiraRepository
from lib.mail import Mail
from lib.logger import Logger

branch_template = re.compile("^(.*)/DIRI(\w+)-(\d+)$")
division_template = re.compile("^(.*)/DIRI(\d+)-(\d+)$")

# Проверка корректности имени
def check_branch_name(branch):
    if len(branch_template.findall(branch)) == 1:
        task_id = "DIRI%s-%s" % (branch_template.findall(branch)[0][1], branch_template.findall(branch)[0][2])
        return task_id
    else:
        return 0

# Получение имени автора ветки
def get_author(branch):
  try:
    author = branch['metadata']['com.github.wadahiro.bitbucket.branchauthor:branchAuthor']['author']['displayName']
    return author
  except KeyError:
    return "Unknown"

# Получение имени отдела
def get_division(branch):
    if len(division_template.findall(branch)) == 1:
        return "DIRI%s" % division_template.findall(branch)[0][1]
    else:
        return "DIRI525"

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

# Форматирование данных
def preparing(project, repo, branch, author, projectkey, branchid):
    url = "%s/projects/%s/repos/%s/browse?at=%s" % (config.BASE_URL_BITBUCKET_UI, projectkey, repo, branchid)
    content = """
<tr>
<td>%s</td>
<td>%s</td>
<td><a href="%s">%s</a></td>
<td>%s</td>
</tr>
""" % (project, repo, url, branch,  author)
    return content

# Рассылка сообщений
def send_mail(msg_type, msg):
    for key, value in msg.items():
        smtp = Mail(config.MAIL['smtp'], config.MAIL['fromaddr'])
        if key == "DIRI525":
            smtp.Send(msg_type, config.MAIL[key], value, key.encode('utf-8'))
        elif key in config.MAIL:
            smtp.Send(msg_type, "%s, %s" % (config.MAIL[key], config.MAIL['DIRI525']), value, key.encode('utf-8'))
        else:
            message = "No RCPT mail KEY %s" % key
            logger.Write(message)
        smtp.close()


# Проверка смержена ли ветка
def check_branch_merge(bb, project, repo, branch):
    if branch['metadata'].get('com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata'):
        if branch['metadata']['com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata'].get('pullRequest'):
            if branch['metadata']['com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata']['pullRequest']['state'] == "MERGED":
                compare = bb.CompareCommits(project['key'], 
                            repo['name'], 
                            branch['id'], 
                            branch['metadata']['com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata']['pullRequest']['toRef']['id']
                )
                if compare.get('errors'):
                    message = "%s %s %s Error: %s" % (project['name'], repo['name'], branch['displayId'], compare['errors'][0]['message'])
                    logger.Write(message)
                    return -1
                return(compare['size'])
        elif branch['metadata']['com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata']['merged']:
            pr = bb.GetPullRequests(project['key'], repo['name'], branch['id'], 'MERGED')
            compare = bb.CompareCommits(project['key'], 
                        repo['name'], 
                        branch['id'], 
                        pr['values'][0]['toRef']['id']
            )
            if compare.get('errors'):
                message = "%s %s %s Error: %s" % (project['name'], repo['name'], branch['displayId'], compare['errors'][0]['message'])
                logger.Write(message)
                return -1
            return(compare['size'])
    else:
        return -2


def main():
    logger = Logger(config.LOG_FILE)
    logger.Write("Start")
    bb = Bitbucket(config.BASE_URL_BITBUCKET, config.USER_BITBUCKET, config.PASS_BITBUCKET)
    projects = bb.GetProjects()

    branch_list_invalidname = {}
    branch_list_delete = {}
    branch_list_check = {}
    
    for project in projects['values']:
        if project['name'].encode('utf8') in config.exclude_projects:
            continue

        repos = bb.GetRepositories(project['key'])
        for repo in repos['values']:
            if repo['name'].encode('utf8') in config.exclude_repo:
                continue
        
            branches = bb.GetBranches(project['key'], repo['name'])
            for branch in branches['values']:
                if branch['displayId'] in config.exclude_branches:
                    continue
                task = check_branch_name(branch['displayId'])
                division = get_division(branch['displayId'])
                author = get_author(branch)
                if task:
                    branch_size = check_branch_merge(bb, project, repo, branch)

# Нет изменений относительно ветки назначения
                    if branch_size == 0:
                        task_status = check_task_status(task)
                        if task_status:
                            if config.TODELETE:
                                bb.DeleteBranch(project['key'], repo['name'], branch['displayId'])
                                message = "%s %s %s Branch delete" % (project['name'], repo['name'], branch['displayId'])
                                logger.Write(message)
                            try:
                                branch_list_delete[division] += preparing(project['name'], 
                                                                          repo['name'], 
                                                                          branch['displayId'], 
                                                                          author,
                                                                          project['key'], 
                                                                          branch['id']
                                                                ).encode('utf-8')
                            except KeyError:
                                branch_list_delete[division] = preparing(project['name'], 
                                                                         repo['name'], 
                                                                         branch['displayId'], 
                                                                         author,
                                                                         project['key'], 
                                                                         branch['id']
                                                               ).encode('utf-8')
# Не удалось сравнить изменения
                    elif branch_size == -1:
                        try:
                            branch_list_check[division] += preparing(project['name'], 
                                                                     repo['name'], 
                                                                     branch['displayId'], 
                                                                     author,
                                                                     project['key'], 
                                                                     branch['id']
                                                                    ).encode('utf-8')
                        except KeyError:
                            branch_list_check[division] = preparing(project['name'], 
                                                                    repo['name'], 
                                                                    branch['displayId'], 
                                                                    author,
                                                                    project['key'], 
                                                                    branch['id']
                                                                   ).encode('utf-8')
# Изменения есть или не было мержа
                    elif branch_size > 0 or branch_size == -2:
                        try:
                            tdiff = datetime.now() - datetime.fromtimestamp(int(str(branch['metadata']['com.atlassian.bitbucket.server.bitbucket-branch:latest-commit-metadata']['authorTimestamp'])[0:10]))
                        except KeyError, e:
                            message = "%s %s %s Key Error: %s" % (project['name'], repo['name'], branch['displayId'], str(e))
                            logger.Write(message)
                            continue
                        if tdiff.days > 30:
                            task_status = check_task_status(task)
                            if task_status:
                                try:
                                    branch_list_check[division] += preparing(project['name'], 
                                                                             repo['name'], 
                                                                             branch['displayId'], 
                                                                             author,
                                                                             project['key'], 
                                                                             branch['id']
                                                                            ).encode('utf-8')
                                except KeyError:
                                    branch_list_check[division] = preparing(project['name'], 
                                                                            repo['name'], 
                                                                            branch['displayId'], 
                                                                            author,
                                                                            project['key'], 
                                                                            branch['id']
                                                                           ).encode('utf-8')
# Некорректное название ветки
                else:
                   try:
                       branch_list_invalidname[division] += preparing(project['name'], 
                                                                      repo['name'], 
                                                                      branch['displayId'], 
                                                                      author,
                                                                      project['key'], 
                                                                      branch['id']
                                                                     ).encode('utf-8')
                   except KeyError:
                       branch_list_invalidname[division] = preparing(project['name'], 
                                                                     repo['name'], 
                                                                     branch['displayId'], 
                                                                     author,
                                                                     project['key'], 
                                                                     branch['id']
                                                                    ).encode('utf-8')

    # Информирование о невалидных именах
    send_mail("invalid_name", branch_list_invalidname)

    if not config.TODELETE:
        # Информирование о ветках к удалению
        send_mail("delete", branch_list_delete)
    
    # Информирование о старых ветках
    send_mail("check", branch_list_check)
    logger.Write("Stop")

if __name__ == "__main__": 
    main()