# -*- coding: utf-8 -*-

from .configs import config
from .lib.bitbucket import Bitbucket

class BitbucketRepository(object):

    def __init__(self):
        self.bitbucket = Bitbucket(
            config.BITBUCKET['rest'], 
            config.BITBUCKET['user'],  
            config.BITBUCKET['password'], 
        )

    def GetProjectList(self):
        projects = self.bitbucket.GetProjects()
        result_projects = []
        for project in projects['values']:
            if project['name'] not in config.EXCLUDE_PROJECTS:
                result_projects.append(project)
                
        return result_projects

    def GetRepositoryList(self, project_key):
        repos = self.bitbucket.GetRepositories(project_key)
        result_repositories = []
        for repo in repos['values']:
            if repo['name'] not in config.EXCLUDE_REPOS:
                result_repositories.append(repo)
                
        return result_repositories

    def GetBranchList(self, project_key, repo_name):
        branches = self.bitbucket.GetBranches(project_key, repo_name)
        result_branches = []
        for branch in branches['values']:
            if branch['displayId'] not in config.EXCLUDE_BRANCHES:
                result_branches.append(branch)
                
        return result_branches