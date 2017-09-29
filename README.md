Скрипт автоматического удаления веток в Bitbucket
-------------------------------------------------

Требования к окружению:
- python 2 или 3
- python-requests >=2.4.2
- logrotate

Для возможности удаления веток у пользователя deployer должны быть права на запись в репозитории
Скрипт может работать в режиме только оповещение и удаление + оповещение
Конфигурирование происходит через файл config.py

Установка зависимостей
```
pip install -r requirements.txt
```

Запуск
```
python rmbranch.py
```


Для ротации лога необходимо скопировать файл rmbranch.rotate в /etc/logrotate.d/
Путь к логу в config.py должен совпадать с тем, что указан в rmbranch.rotate