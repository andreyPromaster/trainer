# Service for learning the Belarusian language
This project helps people to learn Belarusian language
## Dependencies:
- Python 3.6
- Django 2.2.6
- MySQL


First, clone the repository to your local machine:

```bash
https://github.com/andreyPromaster/trainer.git
```

Install the requirements:

```bash
pip install -r requirements.txt
```

Create the database:
How to install Mysql you can visit this tutorial. You should complete the first 5 points
```bash
https://tproger.ru/articles/django-sqlite-to-mysql/
```
Then
```bash
python manage.py migrate
```

Finally, run the development server:

```bash
python manage.py runserver
```

The project will be available at **127.0.0.1:8000**.
