#!/usr/bin/env python
# -*- coding: utf-8 -*-

BASE_URL_BITBUCKET = "https://stash.itmh.ru/rest/api/1.0"
USER_BITBUCKET = "deployer"
PASS_BITBUCKET = "taQeq9VMFi"

BASE_URL_JIRA = "https://plan.itmh.local/rest/api/2"
USER_JIRA = "service_atlas_assist"
PASS_JIRA = "HDgbf67sgwk"

MAIL = {
  "fromaddr": "stash.itmh.ru",
  "smtp": "mail.sis.mirasystem.net",
  "dir525": "DIR.I5.2.5.users@itmh.ru",
  "dir521": "DIR.I5.2.1.users@itmh.ru",
  "dir522": "DIR.I5.2.2.users@itmh.ru",
  "dir523": "DIR.I5.2.3.users@itmh.ru",
  "test": "byvshev.sergey@itmh.ru"
}

LOG_FILE = "/home/byvshev/rmbranch/rmbranch.log"

exclude_projects = [
    'ARM',
    'Assistant',
    'DHCP Web Service',
    'DIR.I5.2.2',
    'DIR.I5.2.4 Тестирование',
    'DIR.I5.5',
    'Docker',
    'Firmware',
    'ISMS',
    'ITIA',
    'iTV',
    'NMS',
    'Toolchain',
    'Архив старья',
    'ОИР'
]

exclude_repo = []

exclude_branches = [
    'master',
    'develop'
]