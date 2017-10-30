# -*- coding: utf-8 -*-

class BranchExecute(object):

    # Форматирование данных
    def preparing(project, repo, branch, author, projectkey, branchid):
        url = "%s/projects/%s/repos/%s/browse?at=%s" % (
                                                        config.BASE_URL_BITBUCKET_UI, 
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

    # Рассылка сообщений
    def send_mail(msg_type, msg):
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