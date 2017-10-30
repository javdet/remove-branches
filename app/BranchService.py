# -*- coding: utf-8 -*-

class BranchService(object):

    def __init__(self):
        self.branch_template = re.compile("^(.*)/DIRI(\w+)-(\d+)$")
        self.division_template = re.compile("^(.*)/DIRI(\d+)-(\d+)$")

    # Проверка корректности имени
    def GetBranchName(self, branch):
        if len(self.branch_template.findall(branch)) == 1:
           task_id = "DIRI%s-%s" % (
                                    self.branch_template.findall(branch)[0][1], 
                                    self.branch_template.findall(branch)[0][2]
                                   )
           return task_id
        else:
           return 0

    # Получение имени автора ветки
    def GetAuthor(self, branch):
        try:
            author = branch['metadata']['com.github.wadahiro.bitbucket.branchauthor:branchAuthor']['author']['displayName']
            return author
        except KeyError:
            return "Unknown"

    # Получение имени отдела
    def GetDivision(self, branch):
        if len(self.division_template.findall(branch)) == 1:
            return "DIRI%s" % division_template.findall(branch)[0][1]
        else:
            return "DIRI525"

    # Проверка смержена ли ветка
    def CheckBranchMerge(self, bb, project, repo, branch):
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