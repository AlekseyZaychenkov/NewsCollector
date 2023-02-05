Приложение имеет графический web-интерфейс и позволяет искать ранее загруженные новости с сайтов музеев, загруженных из списка в .csv файле.
Для проверки функциональности уже содержит тестовую базу данных.

Протестировано на ОС Ubuntu 22.04.1 LTS 
Для начала работы нужно запустить команды
    • sudo apt-get install python3.10-dev python3.10-venv
    • python3.10 -m venv venv
    • source venv/bin/activate
    • python3.10 -m pip install --upgrade pip
    • pip3 install -r requirements.txt
    • python3.10 manage.py makemigrations
    • python manage.py migrate --run-syncdb
    • python manage.py runserver
ИЛИ скрипт (необходим установленый docker)
./docker_run.sh

После запуска приложение будет доступно на порту 127.0.0.1:8000

Работа с приложением:
Загрузка новых или замена списка может быть произведена с помощью кнопки 'Download list of museum'
Загрузка новостей из сайтов производится с помощью кнопки 'Download News' или через url /download_news
Поиск первых 10 новостей по ключевым словам в заголовке или тексте новости осуществляется с помощью поля 'Find in news' и кнопки 'Find' или через url q=<текст запроса>, возвращающего новости в формате JSON
