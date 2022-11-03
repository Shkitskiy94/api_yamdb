Project YaMDb

YaMDb Project

The YaMDb project collects user reviews.

There are different categories like: "Books", "Films", "Music".

The list of categories (Category) can be expanded (for example, you can add the category "Fine Arts" or "Jewelry").

The works themselves are not stored in YaMDb; you cannot watch a movie or listen to music here.

**API YaMDb Resources **

YaMDb API Resources

USERS: users.

TITLES: titles that are being reviewed (a specific movie, book or song).

CATEGORIES: categories (types) of works ("Films", "Books", "Music").

GENRES: genres of works. One work can be linked to several genres.

REVIEWS: reviews of works. The review is tied to a specific work.

COMMENTS: Comments on reviews. The comment is linked to a specific review.

User registration algorithm

The user sends a POST request with the parameters username and email to / api / v1 / auth / email /

Yamdb sends an email with a confirmation code to the entered email address.

The user sends a POST request with the parameters username and confirmation_code (received by mail) to / api / v1 / auth / token /

In response to the request, he receives a token (JWT token). These operations are performed once, when a user is registered.

As a result, the user receives a token and can work with the API, sending this token with each request.Для обновления токена, нужно отправить повторный запрос на /api/v1/auth/email/ со своими username и email

User Roles:

Anonymous - can view descriptions of works, read reviews and comments.

Authenticated user (user) - can read everything, like Anonymous, additionally can publish reviews and rate works (films / books / songs), can comment on other people's reviews and rate them; can edit and delete their reviews and comments.

Moderator (moderator) - the same rights as the Authenticated user, plus the right to delete and edit any reviews and comments.

Administrator (admin) - full rights to manage the project and all its contents. Can create and delete works, categories and genres. Can assign roles to users.

_Superuser _ - the same rights as the Administrator, except that even if he changes the role to user, he will retain administrator rights

How to install: **
Clone the repository.

Create a virtual environment python -m venv venv in the main project folder

Activate virtual environment

Windows: source venv \ scripts \ activate
Linux / Mac: source venv / bin / activate
Install the requirements with python -m pip install -r requirements.txt

Perform migrations to the database:

python manage.py makemigrations python manage.py migrate

Run the project with the command: python manage.py runserver