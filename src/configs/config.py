# -*- coding: utf-8 -*-

# Реквизиты подключения к API Bitbucket
BITBUCKET = {
    "ui": "https:/bitbucket.org/",
    "rest": "https://bitbucket.org/rest",
    "user": "user",
    "password": "password"
}

# Реквизиты подключения к API Jira
JIRA = {
    "rest": "https://jira.org/rest/api/2",
    "user": "user",
    "password": "password"
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
    "fromaddr": "noreply@company.org",
    "smtp": "mail.company.org",
    "developers": "developers@company.org"
}

# Указать тот же путь в файле ротации
LOG_FILE = "/var/log/rmbranch.log"

# Проекты в которых проверть не нужно
EXCLUDE_PROJECTS = [
    'EXAMPLE1',
    'EXAMPLE2'
]

# Репозитории в которых проверть не нужно
EXCLUDE_REPOS = []

# Ветки в которых проверть не нужно
EXCLUDE_BRANCHES = [
    'master',
    'develop'
]