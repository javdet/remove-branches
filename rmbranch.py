#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import config
import re
from datetime import datetime
from bitbucket import Bitbucket
from jira import Jira

branch_template = re.compile("^(.*)/DIRI(\w+)-(\d+)$")

def logger(message):
    date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    f = open(config.LOG_FILE, 'a')
    f.write(date+" "+message+"\n")
    f.close

# Проверка корректности имени
def check_branch_name(project, repo, branch):
    if len(branch_template.findall(branch)) == 1:
        task_id = "DIRI%s-%s" % (branch_template.findall(branch)[0][1], branch_template.findall(branch)[0][2])
        return task_id
    else:
        logger("%s %s %s Branch name is not valid" % (project, repo, branch))
        return 0

# Проверка статуса задачи
def check_task_status(task):
    jira = Jira(config.BASE_URL_JIRA, config.USER_JIRA, config.PASS_JIRA)
    issue = jira.GetIssue(task)
    if issue['fields']['status']['id'] == "6":
        print('Closed issue')


# Проверка смержена ли ветка
def check_branch_merge(bb, project, repo, branch):
    if len(branch_template.findall(branch['displayId'])) == 1:
        task_id = "DIRI%s-%s" % (branch_template.findall(branch['displayId'])[0][1], branch_template.findall(branch['displayId'])[0][2])
    else:
        logger("%s %s %s Branch name is not valid" % (project['name'], repo['name'], branch['displayId']))
        return -1
    if branch['metadata'].get('com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata'):
        if branch['metadata']['com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata'].get('pullRequest'):
            if branch['metadata']['com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata']['pullRequest']['state'] == "MERGED":
                print(branch['displayId'], 
                    branch['id'], 
                    branch['latestCommit'], 
                    branch['metadata']['com.atlassian.bitbucket.server.bitbucket-branch:ahead-behind-metadata-provider']['ahead'],
                    branch['metadata']['com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata']['pullRequest']['state'],
                    branch['metadata']['com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata']['pullRequest']['toRef']['displayId'],
                    branch['metadata']['com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata']['pullRequest']['toRef']['id']
                )
                compare = bb.CompareCommits(project['key'], 
                            repo['name'], 
                            branch['id'], 
                            branch['metadata']['com.atlassian.bitbucket.server.bitbucket-ref-metadata:outgoing-pull-request-metadata']['pullRequest']['toRef']['id']
                )
                if compare.get('errors'):
                    logger("%s %s %s Error: %s" % (project['name'], repo['name'], branch['displayId'], compare['errors'][0]['message']))
                    return -2
                print(compare)
                return(compare['size'])
        else:
            pr = bb.GetPullRequests(project['key'], repo['name'], branch['id'], 'MERGED')
            print(branch['displayId'], 
                branch['id'], 
                branch['latestCommit'], 
                branch['metadata']['com.atlassian.bitbucket.server.bitbucket-branch:ahead-behind-metadata-provider']['ahead'],
                pr['values'][0]['toRef']['id']
            )
            compare = bb.CompareCommits(project['key'], 
                        repo['name'], 
                        branch['id'], 
                        pr['values'][0]['toRef']['id']
            )
            if compare.get('errors'):
                logger("%s %s %s Error: %s" % (project['name'], repo['name'], branch['displayId'], compare['errors'][0]['message']))
                return -2
            print(compare)
            return(compare['size'])


def main():
    bb = Bitbucket(config.BASE_URL_BITBUCKET, config.USER_BITBUCKET, config.PASS_BITBUCKET)
    projects = bb.GetProjects()

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
                    if branch_size == "0":
                        task_status == check_task_status(task)

if __name__ == "__main__": 
    main()