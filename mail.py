#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

class Mail:

    def __init__(self, smtp_server, fromaddr):
        self.smtp = smtplib.SMTP(smtp_server)
        self.msg = MIMEMultipart()
        self.msg['From'] = fromaddr

# Отправка сообщения
    def Send(self, msg_type, toaddr, content):
        if msg_type == "delete":
            self.msg['Subject'] = "Список веток для удаления"
        elif msg_type == "check":
            self.msg['Subject'] = "Список веток для проверки"
        elif msg_type == "incorrect_name":
            self.msg['Subject'] = "Список веток с некорректным имененм"
        
        self.msg['To'] = toaddr
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
<table>
<tr>
<th>Проект</th>
<th>Репозиторий</th>
<th>Ветка</th>
</tr>
%s
</table>
</body>
</html>
""" % (self.msg['Subject'], content)
        part = MIMEText(body.decode('cp1251'), 'html', 'cp1251')
        self.msg.attach(part)
        self.smtp.sendmail(self.msg['From'], self.msg['To'], msg.as_string())

# Форматирование данных
    def Preparing(project, repo, branch):
        content = """
<tr>
<td>%s</td>
<td>%s</td>
<td>%s</td>
""" % (project, repo, branch)
        return content

    def close():
        self.smtp.quit()