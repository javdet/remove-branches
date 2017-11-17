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
        1. Формирование структуры со списком необходимы данных по веткам
        2. Формирование структуры с флагами проверок по веткам
        3. Сравнения результатов с условиями и установка резолюций
        4. Выполнение действий согласно резолюции
        """

        info_by_branch = self.GetBranchesInfo()
        flags_by_branch = self.GetBranchesFlags(info_by_branch)
        actions_by_branch = self.GetBranchesAction(flags_by_branch)
        # self.BranchExecute(actions_by_branch)

    def GetBranchesInfo(self):
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
                "task":
                "division": 
                "author": 
                "target_branch":
                "task_status":
                "diff_to_target":
                "diff_to_develop":
                "age":  
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
                    branch_data_list.append(
                        self.branch_service.GetDataForBranch(project, repo, branch)
                    )

        return branch_data_list

    def GetBranchesFlags(self, info_by_branch):
        """
        Метод получает структуру с флагами проверок по веткам
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
                "isBranchMerged": 
                "noBranchDiff": 
                "noBranchDiffToDevelop": 
                "isTaskClosed": 
                "noExistTargetBranch": 
                "noBranchValid":
                "isBranchOlder":
            },
            {...}
        ]
        """

        for branch in info_by_branch:
            branch_flags_list.append(
                self.branch_service.GetFlagsForBranch(branch)
            )
        return branch_flags_list

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
    
    

    

    