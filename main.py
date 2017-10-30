#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
from datetime import datetime
from configs import config
from app.BitbucketRepository import BitbucketRepository
from app.BranchExecute import BranchExecute
from app.BranchService import BranchService
from app.JiraRepository import JiraRepository
from lib.mail import Mail
from lib.logger import Logger

def main():

    logger = Logger(config.LOG_FILE)
    logger.Write("Start")

    bb = BitbucketRepository()
    projects = bb.GetProjectList()

    bs = BranchService()

    branch_list_invalidname = {}
    branch_list_delete = {}
    branch_list_check = {}
    
    for project in projects:
        repos = bb.GetRepositoryList(project['key'])

        for repo in repos:
            branches = bb.GetBranchList(project['key'], repo['name'])

            for branch in branches:
                task = bs.GetBranchName(branch['displayId'])
                division = bs.GetDivision(branch['displayId'])
                author = bs.GetAuthor(branch)
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