# -*- coding: utf-8 -*-

# Реквизиты подключения к API Bitbucket
BITBUCKET = {
    "ui": "https://stash.itmh.ru",
    "rest": "https://stash.itmh.ru/rest",
    "user": "deployer",
    "password": "taQeq9VMFi"
}

# Реквизиты подключения к API Jira
JIRA = {
    "rest": "https://plan.itmh.local/rest/api/2",
    "user": "service_atlas_assist",
    "password": "HDgbf67sgwk"
}

"""
Список условий для удаления. Условия в одном списке 
объеденины в логическое И, в разных - ИЛИ
Возможные условаия:
isBranchMerged - ветка находиться в статусе Merged
noBranchDiff - нет новых коммитов относительно ветки назначения
isTaskClosed - задача в КСУ с кодом ветки находиться в статусе Закрыта
noExistTargetBranch - не существует ветки назначения
noBranchDiffToDevelop - нет новых коммитов относительно ветки develop
noTaskExist - задачи в КСУ с кодом ветки не существует
noBranchValid - ветка не соответствует правилам именования
isBranchOlder - ветка существует более месяца
"""
DELETE_CONDITIONS = [
    [
        "isBranchMerged",
        "noBranchDiff",
        "isTaskClosed"
    ],
    [
        "isTaskClosed",
        "isBranchMerged",
        "noExistTargetBranch",
        "noBranchDiffToDevelop"
    ],
    [
        "noTaskExist",
        "isBranchMerged",
        "noExistTargetBranch",
        "noBranchDiffToDevelop"
    ],
    [
        "noBranchValid",
        "isBranchMerged",
        "noExistTargetBranch",
        "noBranchDiffToDevelop"
    ]
]

NOTIFY_CONDITIONS = {
    "check": [
        "isBranchMerged",
        "isTaskClosed",
        "isBranchOlder"
    ],
    "invalid_name": [
        "noBranchValid"
    ]
}

BRANCH_NAME_TEMPLATE = "^(.*)/DIRI(\w+)-(\d+)$"
DIVISION_NAME_TEMPLATE = "^(.*)/DIRI(\d+)-(\d+)$"

"""
Параметры отправки сообщений. fromaddr и smtp обязательные параметры.
fromaddr - Адрес отправителя
smtp - адрес SMTP сервера
Остальные параметры относятся к адресам получателей
"""
MAIL = {
    "fromaddr": "noreply@stash.itmh.ru",
    "smtp": "mail.sis.mirasystem.net",
    "default": "DIR.I5.2.5.users@itmh.ru",
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
EXCLUDE_PROJECTS = [
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
EXCLUDE_REPOS = []

# Ветки в которых проверть не нужно
EXCLUDE_BRANCHES = [
    'master',
    'develop'
]