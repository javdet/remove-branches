# -*- coding: utf-8 -*-

from .configs import config
from .lib.mail import Mail
from .lib.bitbucket import Bitbucket

class BranchExecute(object):

    def FormatingData(self, branch_list):
        """
        Форматирование данных ввиде строки html таблицы
        :return: html-строка
        """

        for branch in branch_list:
            if branch_marked['action'] == "notify":
                url = "%s/projects/%s/repos/%s/browse?at=%s" % (
                    config.Bitbucket['ui'], 
                    branch['project_key'],
                    branch['repo'],
                    branch['branch_id']
                )
                content = """
                    <tr>
                    <td>%s</td>
                    <td>%s</td>
                    <td><a href="%s">%s</a></td>
                    <td>%s</td>
                    </tr>
                    """ % (
                        branch['project'],
                        branch['repo'], 
                        url, 
                        branch['name'],  
                        branch['author']
                    )
                try:
                    branch_data_list[branch.division] += content
                except KeyError:
                    branch_data_list[branch.division] = content

        return branch_data_list

    def PreparingMessages(self, branch_data_list, message_type):
        """
        Метод формирует тело сообщения
        :return: тело сообщения
        """
        pass


    def DeleteBranch(self, branch_marked_list):
        """
        Метод производит удаление веток с резолюцией delete
        :return: void
        """

        bitbucket = Bitbucket(
            config.BITBUCKET['rest'],
            config.BITBUCKET['user'],
            config.BITBUCKET['password'],
        )
        for branch_marked in branch_marked_list:
            if branch_marked['action'] == "delete":
                bitbucket.DeleteBranch(
                    branch_marked['project_key'], 
                    branch_marked['repo'], 
                    branch_marked['name']
                )


    def SendEmail(self, branch_marked_list):
        """
        Метод производит подготовку сообщений 
        и инициирует рассылку
        :return: void
        """
        for condition in config.NOTIFY_CONDITIONS:
            send_data_list = FormatingData(branch_marked_list)
            send_message_list = PreparingMessages(send_data_list)
            for send_message in send_message_list:
                pass

        """                
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
        """