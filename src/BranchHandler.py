# -*- coding: utf-8 -*-

from .BitbucketRepository import BitbucketRepository
from .BranchService import BranchService

class BranchHandler(object):

    # Управляющий метод
    def Handle(self):
        self.map_by_branch = self.GetBranchesStatus()
        # self.map_by_branch = self.GetBranchesAction(self.map_by_branch)
        # self.BranchesExecute(self.map_by_branch)

    """
    Метод создает структуру результатов проверок веток по всем 
    проектам и репозиториям
    Возвращает структуру:
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
            "isBranchValid": 
            "isBranchMerged": 
            "noBranchDiff": 
            "isTaskClosed": 
            "noBranchDiffToDevelop": 
            "isBranchOlder": 
        },
        {...}
    ] 
    """
    def GetBranchesStatus(self):
        br = BitbucketRepository()
        bs = BranchService()
        projects = br.GetProjectList()
        marked_branch_list = []

        for project in projects:
            repos = br.GetRepositoryList(project['key'])
            for repo in repos:
                branches = br.GetBranchList(project['key'], repo['name'])
                for branch in branches:
                    marked_branch_list.append(
                        bs.GetMarkForBranch(project, repo, branch)
                    )

        return marked_branch_list
                

    def GetBranchesAction(self):
        pass
    def BranchesExecute(self):
        pass
        # be.Deletebranch(marked_branch_list)
        # be.SendEmail(marked_branch_list)
    
    

    

    