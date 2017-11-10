# -*- coding: utf-8 -*-
from datetime import datetime

# Логирование
class Logger(object):

    def __init__(self, log_file):
        self.date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        self.f = open(log_file, 'a')

    def Write(self, message):
        self.f.write(self.date+" "+message+"\n")
        
    def Close(self):
        self.f.close()