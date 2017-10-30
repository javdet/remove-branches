# -*- coding: utf-8 -*-

from ..configs import config
from ..lib.bitbucket import Bitbucket

class BitbucketRepository(object):

    def __init__(self):
        bb = Bitbucket(
                       config.BASE_URL_BITBUCKET, 
                       config.USER_BITBUCKET, 
                       config.PASS_BITBUCKET
                      )

    def GetProjectList(self):
        projects = bb.GetProjects()
        result_projects = []
        for project in projects['values']:
            if project['name'].encode('utf8') in config.exclude_projects:
                continue
            else:
                result_projects.append(project)
        return result_projects

    def GetRepositoryList(self, project_key):
        repos = bb.GetRepositories(project_key)
        result_repositories = []
        for repo in repos['values']:
            if repo['name'].encode('utf8') in config.exclude_repo:
                continue
            else:
                result_repositories.append(repo)
        return result_repositories

    def GetBranchList(self, project_key, repo_name):
        branches = bb.GetBranches(project['key'], repo['name'])
        result_branches = []
        for branch in branches['values']:
            if branch['displayId'] in config.exclude_branches:
                continue
            else:
                result_branches.append(branch)
        return result_branches