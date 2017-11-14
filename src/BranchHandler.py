# -*- coding: utf-8 -*-

from .BitbucketRepository import BitbucketRepository
from .BranchService import BranchService
from .BranchExecute import BranchExecute

class BranchHandler(object):

    def __init__(self):
        self.branch_service = BranchService()
        self.branch_execute = BranchExecute()

    def Handle(self):
        """
        Управляющий метод
        Выполняет 3 операции:
        1. Получение структуру результатов проверок веток
        2. Сравнения результатов с условиями и установка резолюций
        3. Выполнение действий согласно резолюции
        """
        map_by_branch = self.GetBranchesStatus()
        map_by_branch = self.GetBranchesAction(map_by_branch)
        # self.BranchExecute(self.map_by_branch)

    def GetBranchesStatus(self):
        """
        Метод создает структуру результатов проверок веток по всем 
        проектам и репозиториям
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
                "difference": 
                "BranchValid": 
                "BranchMerged": 
                "noBranchDiff": 
                "isTaskClosed": 
                "noBranchDiffToDevelop": 
                "isBranchOlder": 
            },
            {...}
        ] 
        """
        bitbucket_repository = BitbucketRepository()
        projects = bitbucket_repository.GetProjectList()
        marked_branch_list = []

        for project in projects:
            repos = bitbucket_repository.GetRepositoryList(
                project['key']
            )
            for repo in repos:
                branches = bitbucket_repository.GetBranchList(
                    project['key'], repo['name']
                )
                for branch in branches:
                    marked_branch_list.append(
                        self.branch_service.GetMarkForBranch(project, repo, branch)
                    )

        return marked_branch_list
                
    def GetBranchesAction(self, map_by_branch):
        """
        Метод создает структуру с указанием действий для каждой ветки
        на основании сравнения с условиями
        :return:
        """
        map_branch_by_condition = []

        for branch_item in map_by_branch:
            map_branch_by_condition.append(
                self.branch_service.GetBranchByCondition(branch_item)
            )
            
    def BranchesExecute(self, marked_branch_list):
        """
        Метод производит действия согласно резолюциям
        """
        pass
        # self.branch_execute.DeleteBranch(marked_branch_list)
        # self.branch_execute.SendEmail(marked_branch_list)
    
    

    

    