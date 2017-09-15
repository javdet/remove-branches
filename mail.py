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
        elif msg_type == "invalid_name":
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
        self.smtp.set_debuglevel(1)
        try:
            self.smtp.sendmail(self.msg['From'], self.msg['To'], self.msg.as_string())
        except SMTPRecipientsRefused:
            return -1
        except MTPSenderRefused:
            return -2
        except SMTPDataError:
            return -3

    def close():
        self.smtp.quit()