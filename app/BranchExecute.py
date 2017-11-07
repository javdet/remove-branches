# -*- coding: utf-8 -*-

from ..configs import config
from ..lib.mail import Mail
from ..lib.bitbucket import Bitbucket

class BranchExecute(object):

    # Форматирование данных
    def FormatingData(project, repo, branch, author, projectkey, branchid):
        url = "%s/projects/%s/repos/%s/browse?at=%s" % (
            config.Bitbucket['ui'], 
            projectkey, 
            repo, 
            branchid
        )
        content = """
            <tr>
            <td>%s</td>
            <td>%s</td>
            <td><a href="%s">%s</a></td>
            <td>%s</td>
            </tr>
            """ % (project, repo, url, branch,  author)
        return content

    # Удаление ветки
    def DeleteBranch(self, branch_marked_list):
        bb = Bitbucket(
            config.BITBUCKET['rest'],
            config.BITBUCKET['user'],
            config.BITBUCKET['password'],
        )
        for branch_marked in branch_marked_list:
            for condition in config.DELETE_CONDITIONS:
                shared_items = set(condition.items()) & set(branch_marked.items())
                if len(shared_items) == len(condition):
                    bb.DeleteBranch(
                        branch_marked['project_key'], 
                        branch_marked['repo'], 
                        branch_marked['name']
                    )
                    message = "%s %s %s Branch delete" % (project['name'], repo['name'], branch['displayId'])
                    logger.Write(message)
                    break

    # Рассылка сообщений
    def SendEmail(self, branch_marked_list):
        branch_list_invalidname = {}
        branch_list_check = {}
        bb = Bitbucket(
            config.BITBUCKET['rest'],
            config.BITBUCKET['user'],
            config.BITBUCKET['password'],
        )
        for branch_marked in branch_marked_list:
            for key in config.SENDMAIL_CONDITIONS:
                shared_items = set(config.SENDMAIL_CONDITIONS[key].items()) & set(branch_marked.items())
                if len(shared_items) == len(config.SENDMAIL_CONDITIONS[key]):
                    branch_list_check[branch_marked.division] += FormatingData(
                        branch_marked['project'],
                        branch_marked['repo'],
                        branch_marked['name'],
                        branch_marked['author'],
                        branch_marked['project_key'],
                        branch_marked['branch_id']
                    ).encode('utf-8')

        for key, value in msg.items():
            smtp = Mail(config.MAIL['smtp'], config.MAIL['fromaddr'])
            if key == "DIRI525":
                smtp.Send(msg_type, config.MAIL[key], value, key.encode('utf-8'))
            elif key in config.MAIL:
                smtp.Send(msg_type, "%s, %s" % (config.MAIL[key], config.MAIL['DIRI525']), value, key.encode('utf-8'))
            else:
                message = "No RCPT mail KEY %s" % key
                logger.Write(message)
            smtp.close()