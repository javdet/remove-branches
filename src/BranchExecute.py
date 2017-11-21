# -*- coding: utf-8 -*-

from .configs import config
from .lib.mail import Mail
from .lib.bitbucket import Bitbucket
from .lib.logger import Logger

class BranchExecute(object):

    def FormatingData(self, condition, branch_list):
        """
        Форматирование данных ввиде строки html таблицы
        :return: dict
        { отдел: html список веток }
        """

        branch_data_list = {}
        for branch in branch_list:
            if branch['message'] == condition:
                url = "%s/projects/%s/repos/%s/browse?at=%s" % (
                    config.BITBUCKET['ui'], 
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
                division = branch['division']
                try:
                    branch_data_list[division] += content
                except KeyError:
                    branch_data_list[division] = content

        return branch_data_list

    def PreparingMessages(self, condition, data_list):
        """
        Метод формирует тело сообщения
        :return: dict
        {отдел, [заголовок, сообщение]}
        """

        message_data_list = {}
        for division in data_list:
            if condition == "delete":
                subject = "Список веток для удаления %s" % division
                message = "Ветки, которые будут удалены автоматически"
            elif condition == "check":
                subject = "Список веток для проверки %s" % division
                message = "Просьба проверить нужны ли ветки и при необходимости удалить" 
            elif condition == "invalid_name":
                subject = "Список веток с некорректным имененем %s" % division
                message = "Следующие ветки имеют некорректное название" 
            
            body = """
<!DOCTYPE html>
<html>
<head>
<title>%s</title>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
<meta http-equiv="content-type" content="application/xhtml+xml; charset=UTF-8">
<style type="text/css">
body{
font-size: 12px;
}
th {
background-color: #D3D3D3;
}
</style>
</head>
<body>
%s
<table>
<tr>
<th>Проект</th>
<th>Репозиторий</th>
<th>Ветка</th>
<th>Автор</th>
</tr>
%s
</table>
</body>
</html>
""" % (subject, message, data_list[division])

            try:
                message_data_list[division] += [
                    subject,
                    body
                ]
            except KeyError:
                message_data_list[division] = [
                    subject,
                    body
                ]

        return message_data_list


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
            logger = Logger(config.LOG_FILE)
            message = "%s %s %s Deleted" % (
                branch_marked['project_key'], 
                branch_marked['repo'], 
                branch_marked['name']
            )
            logger.Write(message)
        
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

        smtp = Mail(config.MAIL['smtp'])
        for condition in config.NOTIFY_CONDITIONS:
            send_data_list = self.FormatingData(condition, branch_marked_list)
            send_message_list = self.PreparingMessages(condition, send_data_list)
            for division in send_message_list:
                smtp.Send(
                    config.MAIL['fromaddr'],
                    config.MAIL[division], 
                    send_message_list[division][0], 
                    send_message_list[division][1]
                )
                
        smtp.close()

        
                