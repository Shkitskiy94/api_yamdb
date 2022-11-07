# YaMDb | REST API Service 

### Описание:
Проект YaMDb собирает отзывы пользователей на фильмы, музыку, книги (произведения)

Пользователя могут публиковать отзывы на произведения, оценивать их (по шкале от 1 до 10), и обсуждать отзывы в комментариях

Средний рейтинг каждого произведения рассчитывается автоматически

Список категорий и жанров определен администратором, но может быть расширен в будущем.

### Ключевые особенности:
- Регистрация пользователей происходит путем отправки проверочного кода на e-mail
- Кастомные пользовательские роли: пользователь, модератор, админ
- Кастомная фильтрация по жанру и категориям
- Кастомная аутентификация по JWT токену

## Технологии и библиотеки:
- [Python](https://www.python.org/);
- [Django](https://www.djangoproject.com);
- [SQLite3](https://www.sqlite.org/index.html);
- [Simple-JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/);
- [Django REST Framework](https://www.django-rest-framework.org).

### Как запустить проект:

Клонируйте репозиторий:
```
git clone git@github.com:Shkitskiy94/api_yamdb.git
```

Измените свою текущую рабочую дерикторию:
```
cd /api_yamdb/
```

Создайте и активируйте виртуальное окружение (версия Python 3.7.9)

```
python -3.7 -m venv venv
```

```
source venv/scripts/activate
```

Обновите pip:
```
python3 -m pip install --upgrade pip
```

Установите зависимости из requirements.txt:

```
pip install -r requirements.txt
```

Создайте миграции:

```
python manage.py migrate
```
Запустите сервер:

```
python manage.py runserver
```
Полная документация прокта (redoc) доступна по адресу http://127.0.0.1:8000/redoc/


### Как зарегистрировать пользователя
1. Сделайте POST запрос, укаказав в теле "username" и "email" на эндпоинт "api/v1/auth/signup/"
2. YaMDb отправит проверочный код на указанный email 
3. Сделайте POST запрос указав "email" и "confirmation_code" в теле запроса на эндпоинт  "api/v1/auth/token/"/,в ответе вы получите JWT-токен

### Примеры работы с API
## Регистрация нового пользователя

Регистрация нового пользователя:

```
POST /api/v1/auth/signup/
```

```json
{
  "email": "string",
  "username": "string"
}

```

Получение JWT-токена:

```
POST /api/v1/auth/token/
```

```json
{
  "username": "string",
  "confirmation_code": "string"
}
```
## Пример работы API для авторизованных пользователей
Добавление категории:

```
Права доступа: Администратор.
POST /api/v1/categories/
```

```json
{
  "name": "string",
  "slug": "string"
}
```

Удаление категории:

```
Права доступа: Администратор.
DELETE /api/v1/categories/{slug}/
```

Добавление жанра:

```
Права доступа: Администратор.
POST /api/v1/genres/
```

```json
{
  "name": "string",
  "slug": "string"
}
```

Удаление жанра:

```
Права доступа: Администратор.
DELETE /api/v1/genres/{slug}/
```

Обновление публикации:

```
PUT /api/v1/posts/{id}/
```

```json
{
"text": "string",
"image": "string",
"group": 0
}
```

Добавление произведения:

```
Права доступа: Администратор. 
Нельзя добавлять произведения, которые еще не вышли (год выпуска не может быть больше текущего).

POST /api/v1/titles/
```

```json
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

Добавление произведения:

```
Права доступа: Доступно без токена
GET /api/v1/titles/{titles_id}/
```

```json
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```

Частичное обновление информации о произведении:

```
Права доступа: Администратор
PATCH /api/v1/titles/{titles_id}/
```

```json
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

Частичное обновление информации о произведении:
```
Права доступа: Администратор
DEL /api/v1/titles/{titles_id}/
```

По TITLES, REVIEWS и COMMENTS аналогично, более подробно по эндпоинту /redoc/

## Работа с пользователями:

Получение списка всех пользователей.

```
Права доступа: Администратор
GET /api/v1/users/ - Получение списка всех пользователей
```

Добавление пользователя:

```
Права доступа: Администратор
Поля email и username должны быть уникальными.
POST /api/v1/users/ - Добавление пользователя
```

```json
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
```

Получение пользователя по username:

```
Права доступа: Администратор
GET /api/v1/users/{username}/ - Получение пользователя по username
```

Изменение данных пользователя по username:

```
Права доступа: Администратор
PATCH /api/v1/users/{username}/ - Изменение данных пользователя по username
```

```json
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

Удаление пользователя по username:

```
Права доступа: Администратор
DELETE /api/v1/users/{username}/ - Удаление пользователя по username
```

Получение данных своей учетной записи:

```
Права доступа: Любой авторизованный пользователь
GET /api/v1/users/me/ - Получение данных своей учетной записи
```

Изменение данных своей учетной записи:

- Права доступа: Любой авторизованный пользователь
```
PATCH /api/v1/users/me/ # Изменение данных своей учетной записи
```

### API YaMDb ресурсы:
- AUTH: Аутентификация.
- USERS: Регистрация пользователей/редактирование информации
- TITLES: Произведения и информация о них
- CATEGORIES: Категории произведений (фильмы, музыка, книги)
- GENRES: Жанры. Одно произведение может иметь несколько жанров
- REVIEWS: Отзывы на произведения. Каждый отзыв относится к определенному произведению.
- COMMENTS: Комментарии к отзывам на произведения.


### Авторы (команда проекта "Dream Team"):
- [Шкитский Юрий](https://github.com/Shkitskiy94/api_final_yatube.git) (Тим-лид, разработчик) 

- [Полина Горшкова](https://github.com/pgorshkova) (разработчик)

- [Вячеслав Поликарский](https://github.com/slava512mb) (разработчик)
