#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app.BranchHandler import BranchHandler
from lib.logger import Logger

"""
Метод запускает процедуру проверки веток на соответствие
условиям удаления/оповещения и выполнении действий
"""
def main():

    logger = Logger(config.LOG_FILE)
    logger.Write("Start")

    bh = BranchHandler()
    bh.handle()

    # Получаем список проектов в Bibucket
    bb = BitbucketRepository()
    projects = bb.GetProjectList()

    bs = BranchService()

    marked_branch_list = []
    
    # Получаем список репозиториев для каждого проекта
    for project in projects:
        repos = bb.GetRepositoryList(project['key'])

        # Получаем список веток для каждого репозитория
        for repo in repos:
            branches = bb.GetBranchList(project['key'], repo['name'])

            # Для каждой ветки создаем структуру с результатами проверки
            for branch in branches:
                marked_branch_list.append(bs.GetMarkForBranch(project, repo, branch))
    
    be = BranchExecute()
    be.Deletebranch(marked_branch_list)
    be.SendEmail(marked_branch_list)

    logger.Write("Stop")

if __name__ == "__main__": 
    main()