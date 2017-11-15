#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.BranchHandler import BranchHandler
from src.lib.logger import Logger
from src.configs import config

def main():
    """
    Метод запускает процедуру проверки веток на соответствие
    условиям удаления/оповещения и выполнении действий
    Возвращает void
    """

    logger = Logger(config.LOG_FILE)
    logger.Write("Start")

    bh = BranchHandler()
    bh.Handle()

    logger.Write("Stop")
    logger.Close()

if __name__ == "__main__": 
    main()