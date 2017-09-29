#!/usr/bin/env python
# -*- coding: utf-8 -*-

BASE_URL_BITBUCKET_UI = "https://stash.itmh.ru"
BASE_URL_BITBUCKET = "%s/rest" % BASE_URL_BITBUCKET_UI
USER_BITBUCKET = "deployer"
PASS_BITBUCKET = "taQeq9VMFi"

BASE_URL_JIRA = "https://plan.itmh.local/rest/api/2"
USER_JIRA = "service_atlas_assist"
PASS_JIRA = "HDgbf67sgwk"

# 1 - удалять, 0 - только оповещать
TODELETE = 1

MAIL = {
  "fromaddr": "noreply@stash.itmh.ru",
  "smtp": "mail.sis.mirasystem.net",
  "DIRI52": "DIR.I5.2.users@itmh.ru",
  "DIRI525": "DIR.I5.2.5.users@itmh.ru",
  "DIRI521": "DIR.I5.2.1.users@itmh.ru",
  "DIRI522": "DIR.I5.2.2.users@itmh.ru",
  "DIRI523": "DIR.I5.2.3.users@itmh.ru",
  "DIRI54": "DIR.I5.4.users@itmh.ru",
  "DIRI532": "DIR.I5.3.2.users@itmh.ru",
  "test": "byvshev.sergey@itmh.ru"
}


# Указать тот же путь в файле ротации
LOG_FILE = "/var/log/rmbranch.log"

# Проекты в которых проверть не нужно
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

# Репозитории в которых проверть не нужно
exclude_repo = []

# Ветки в которых проверть не нужно
exclude_branches = [
    'master',
    'develop'
]