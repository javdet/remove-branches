#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

class Mail:

    def __init__(self, smtp_server, fromaddr):
        self.smtp = smtplib.SMTP(smtp_server)
        self.msg = MIMEMultipart()
        self.msg['From'] = fromaddr

    def Send(self, toaddr, subject, content):
        """
        Отправка сообщения указанному адресату
        :return: код ошибки отправки или void
        """

        self.msg['Subject'] = Header(subject, 'utf-8')
        self.msg['To'] = toaddr
        
        part = MIMEText(content, 'html', 'utf-8')
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