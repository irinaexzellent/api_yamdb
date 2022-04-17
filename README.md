# О проекте:

Проект для публикации отзывов на произведения

# Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:irinaexzellent/api_yamdb.git
```

```
cd api_yamdb
```
Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```
```
source venv/Scripts/activate

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python3 manage.py migrate
```

Запустить проект:
```
python3 manage.py runserver
```
.
