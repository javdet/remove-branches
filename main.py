#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.BranchHandler import BranchHandler
from src.lib.logger import Logger

"""
Метод запускает процедуру проверки веток на соответствие
условиям удаления/оповещения и выполнении действий
Возвращает void
"""
def main():

    logger = Logger(config.LOG_FILE)
    logger.Write("Start")

    bh = BranchHandler()
    bh.Handle()

    logger.Write("Stop")

if __name__ == "__main__": 
    main()