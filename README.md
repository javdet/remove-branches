Скрипт автоматического удаления веток в Bitbucket
-------------------------------------------------

Требования к окружению:
- python 3
- python-requests >=2.4.2
- logrotate

Для возможности удаления веток у пользователя deployer должны быть права на запись в репозитории
Конфигурирование происходит через файл configs/config.py

Установка зависимостей
```
pip install -r requirements.txt
```

Запуск
```
python main.py
```

Для ротации лога необходимо скопировать файл rmbranch.rotate в /etc/logrotate.d/
Путь к логу в configs/config.py должен совпадать с тем, что указан в rmbranch.rotate