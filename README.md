# Foodgram Project 
 
## Описание проекта
 
Проект "Foodgram" - это веб-приложение, созданное для любителей кулинарии, которое позволяет пользователям делиться своими рецептами, находить интересные блюда, управлять списками покупок и подписываться на аккаунты других пользователей. Вот подробнее о ключевых функциях и особенностях "Foodgram":

### Рецепты и Публикации:
 
- Пользователи могут создавать свои рецепты, прикреплять фотографии, описания и список ингредиентов с указанием количества.
- Рецепты можно редактировать, обновлять и удалять.
- Каждый рецепт имеет уникальное название, которое должно быть уникальным в пределах приложения.
- Пользователи могут просматривать рецепты других пользователей.

### Подписки и Подписчики
- Пользователи могут подписываться на аккаунты других пользователей, чтобы видеть их новые рецепты в своей ленте.
- Лента пользователя отображает рецепты тех, на кого он подписан.

### Список Покупок
- Пользователи могут создавать списки покупок, в которых перечисляются ингредиенты для выбранных рецептов.
- Список покупок можно скачать в виде файла, который содержит все необходимые ингредиенты и их количество.
### Теги и Категории
- Рецепты могут быть отмечены тегами, позволяя пользователям легко находить рецепты по определенным категориям или типам блюд.
### Поиск и Фильтрация
- Пользователи могут искать рецепты по ключевым словам, названиям и тегам.
- Рецепты можно фильтровать по различным параметрам, таким как время приготовления и доступные ингредиенты.

Проект "Foodgram" обладает удобным интерфейсом, который позволяет пользователям легко создавать, искать и взаимодействовать с рецептами, а также делиться своими кулинарными находками с сообществом.

Сервис доступен по адресу: http://158.160.0.197/ 

 
### Инструкцию по запуску: 
### Запуск проекта:
1. Клонируйте проект:
```
git clone git@github.com:Scales313/foodgram-project-react.git
```
2. Подготовьте сервер:
```
scp docker-compose.yml <username>@<host>:/home/<username>/
scp nginx.conf <username>@<host>:/home/<username>/
scp .env <username>@<host>:/home/<username>/
```
3. Установите docker и docker-compose:
```
sudo apt install docker.io 
sudo apt install docker-compose
```
4. Создайте и войдеите в папуку проекта

```text
mkdir foodgram && cd foodgram/
```

5. создайте и заполните .env файл:

```text
touch .env
```

пример
```text
DEBUG=False
SECRET_KEY=Ваш ключ
ALLOWED_HOSTS= ваш хост
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=django_user
POSTGRES_PASSWORD=ваш пароль
DB_HOST=foodgram-db
DB_PORT=5432
```
6. Перенесите файлы из infra на серевер

```text
scp -r infra/* <server user>@<server IP>:/home/<server user>/foodgram/
```
7. Выполните команды 
```text
sudo docker compose -f docker-compose.yml pull
sudo docker compose -f docker-compose.yml down
sudo docker compose -f docker-compose.yml up -d
sudo docker compose -f docker-compose.yml exec backend python manage.py makemigrations
sudo docker compose -f docker-compose.yml exec backend python manage.py migrate
sudo docker compose -f docker-compose.yml exec backend python manage.py collectstatic
sudo docker compose -f docker-compose.yml exec backend cp -r /app/static/. /backend_static/static/
```

## Использованные технологии
 
- Python 
- Django 3.2.3 
- Django REST framework 3.12.4 
- Nginx 
- Docker 
- Postgres 
 
## Информация об авторе 
Сергей Капустин (capustin.serezha2012@yandex.ru) 
студент яндекс практикума 
 
# Сайт 
-http://158.160.0.197/ 
-админка 
``` 
логин: Adminq 
пароль: password 
``` 
