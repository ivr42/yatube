# Yatube

Yatube — концепт социальной сети для публикации дневников.

## Стек технологий, использованных в проекте
- Python 3.7
- Django 2.2
- PostgreSQL 13


## Как установить проект:
1. Клонировать репозиторий и перейти в него в командной строке:
```shell
git clone https://github.com/ivr42/api_final_yatube
```
```shell
cd api_final_yatube
```

2. Cоздать и активировать виртуальное окружение:
```shell
python3 -m venv venv
```
```shell
source venv/bin/activate
```

3. Установить зависимости из файла requirements.txt:
```shell
python3 -m pip install --upgrade pip
```
```shell
pip install -r requirements.txt
```

4. Выполнить миграции:
```shell
python3 manage.py migrate
```
## Как запустить проект:
```shell
python3 manage.py runserver
```

