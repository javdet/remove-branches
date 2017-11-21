#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

class Mail:

    def __init__(self, smtp_server):
        self.smtp = smtplib.SMTP(smtp_server)

    def Send(self, fromaddr, toaddr, subject, content):
        """
        Отправка сообщения указанному адресату
        :return: код ошибки отправки или void
        """

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['Subject'] = Header(subject, 'utf-8')
        msg['To'] = toaddr
        
        part = MIMEText(content, 'html', 'utf-8')
        msg.attach(part)
        try:
            self.smtp.sendmail(msg['From'], msg['To'], msg.as_string())
        except SMTPRecipientsRefused:
            return -1
        except MTPSenderRefused:
            return -2
        except SMTPDataError:
            return -3

    def close(self):
        self.smtp.quit()