#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.header import Header

class Mail:

    def __init__(self, smtp_server, fromaddr):
        self.smtp = smtplib.SMTP(smtp_server)
        self.msg = MIMEMultipart()
        self.msg['From'] = fromaddr

# Отправка сообщения
    def Send(self, msg_type, toaddr, content, division):
        if msg_type == "delete":
            self.msg['Subject'] = Header("Список веток для удаления %s" % division, 'utf-8')
            message = "Ветки, которые будут удалены автоматически"
        elif msg_type == "check":
            self.msg['Subject'] = Header("Список веток для проверки %s" % division, 'utf-8')
            message = "Просьба проверить нужны ли ветки и при необходимости удалить" 
        elif msg_type == "invalid_name":
            self.msg['Subject'] = Header("Список веток с некорректным имененем %s" % division, 'utf-8')
            message = "Следующие ветки имеют некорректное название" 
        
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
%s
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
""" % (self.msg['Subject'], message, content)
        part = MIMEText(body, 'html', 'utf-8')
        self.msg.attach(part)
        try:
            self.smtp.sendmail(self.msg['From'], self.msg['To'], self.msg.as_string())
        except SMTPRecipientsRefused:
            return -1
        except MTPSenderRefused:
            return -2
        except SMTPDataError:
            return -3

    def close(self):
        self.smtp.quit()