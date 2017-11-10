# -*- coding: utf-8 -*-

from .BitbucketRepository import BitbucketRepository
from .BranchService import BranchService
from .lib.logger import Logger

class BranchHandler(object):

    # Управляющий метод
    def Handle(self):
        map_by_branch = self.GetBranchesStatus()
        # map_by_branch = self.GetBranchesAction(map_by_branch)
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
        bitbucket_repository = BitbucketRepository()
        branch_service = BranchService()
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
                        branch_service.GetMarkForBranch(project, repo, branch)
                    )

        return marked_branch_list
                

    def GetBranchesAction(self, map_by_branch):
        self.logger = Logger(config.LOG_FILE)
        for branch_item in map_by_branch:
            for condition in config.DELETE_CONDITIONS:
                shared_items = set(condition.items()) & set(branch_item.items())
                if len(shared_items) == len(condition):
                    bb.DeleteBranch(
                        branch_marked['project_key'], 
                        branch_marked['repo'], 
                        branch_marked['name']
                    )
                    message = "%s %s %s Branch delete" % (
                        project['name'], 
                        repo['name'], 
                        branch['displayId']
                    )
                    self.logger.Write(message)
                    break
    def BranchesExecute(self):
        pass
        # be.Deletebranch(marked_branch_list)
        # be.SendEmail(marked_branch_list)
    
    

    

    