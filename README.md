
# MEMES (test assigment for Ray)

Проект MEMES представляет собой сайт, позволяющий пользователям просматривать, загружать и лайкать мемы. Кроме того, мемы переодически генерируются бекендом путём запросов к сторонним API-сервисам и выкладываются на сайт.

**Важно: Все мемы генерируются случайно на основании шуток, полученных со стороннего API сервиса**
**и не имеют к разработчику проекта никакого отношения, не выражают его позиции по каким-либо вопросам.**

Бэкенд написан на **Python 3.11.4, Django 4.2**.
Мемы генерируются путём запросов к следующим API сервисам:
- https://v2.jokeapi.dev/ (Сборник шуток)
- https://memegen.link/ (Сервис, использующий нейросети для генерации мемов по тексту)

Запросы и генерация осуществляются асинхронно с помощью **aiohttp**
Задачи по генерации управляются с помощью **celery + redis**
Подробнее можно посмотреть в pyproject.toml.

**По причине использования celery, проект не будет работать на Windows!**


## Деплой
#### Алгоритм действий для запуска проекта
Все команды выполняются из корневой папки проекта (ray_test)

1) Создать файл ".env" в корневой папке проекта со следующими переменными:
```
POSTGRES_DB=имя_БД_postgres
POSTGRES_USER=имя_юзера_БД_postgres
POSTGRES_PASSWORD=пароль_юзера_БД_postgres
POSTGRES_HOST=хост_postgres
POSTGRES_PORT=порт_postgres
REDIS_HOST=хост_redis
REDIS_PORT=порт_redis
```
2) Установить и активировать виртуальное окружение.
Установить зависимости через менеджер пактов pip.
Команды:
```
python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```
3) Создать супер-пользователя для взаимодействия со страницей администратора:
```
python src/manage.py createsuperuser
``` 
4) Запуск проекта.
Осуществляется командами:
```
(перед запуском не забываем дать права на запуск скрипта)
chmod +x scripts/entrypoint.sh

запуск:
scripts/entrypoint.sh
```
Скрипт прогонит тесты, подготовит и запустит django-проект, сервер redis и celery.
Приложние будет запущено на локальном хосте:
http://127.0.0.1:8000

## Взаимодействие с проектом
Весь функционал сайта доступен через незамысловатую
фронтенд страничку. Базовую страницу можно найти здесь:
http://127.0.0.1:8000/memes/

Админ-страница проекта:
http://127.0.0.1:8000/admin/

Генерация и загрузка мемов на сайт будет происходиться автоматически.
Каждые 3 минуты будет генерироваться кол-во мемов указанное в core.settings.MEMES_TO_GENERATE (по умолчанию - 3).

## Also
**Документацию** вью и моделей можно получить на эндпоинте http://127.0.0.1:8000/admin/doc/ при запущенном сервере.
Навигация по url фронтенда находится вот здесь: http://127.0.0.1:8000/admin/doc/views/#ns|memes


Проект покрыт простыми **тестами**. Запустить их можно командой "python src/manage.py test src" из корневой папки проекта.


## TO DO
1) Расширить область покрытия тестами
2) Добавить больше опций взаимодействия между пользователями, комменты, просмотр чужих лайков.
3) Найти более удачную интеграцию для генерации мемов
