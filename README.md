# ИРФАН — «Аруу жүрөк»

Диний-агартуу курсу үчүн Django 5 веб-тиркемеси. Башкы тил — кыргызча. Мазмун, катталуулар, сабактар, мугалимдер, жаңылыктар жана FAQ Django Admin аркылуу башкарылат.

## Талаптар

- Python 3.12+
- PostgreSQL 15+ (production үчүн; development режиминде SQLite автоматтык колдонулат)

## Орнотуу

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

Андан кийин сайт `http://127.0.0.1:8000/`, админ панель `http://127.0.0.1:8000/admin/` дарегинде ачылат.

## PostgreSQL

`.env` файлына төмөнкү сапты кошуңуз:

```env
DATABASE_URL=postgres://USER:PASSWORD@127.0.0.1:5432/aruu_jurok
DEBUG=False
ALLOWED_HOSTS=your-domain.kg,www.your-domain.kg
```

`SECRET_KEY` маанисин production'до сөзсүз алмаштырыңыз. `DEBUG=False` режиминде HTTPS колдонуу сунушталат.

## Негизги URL'дер

- `/` — башкы бет
- `/course/` — курс жөнүндө
- `/program/` — окуу программасы
- `/teachers/` — мугалимдер
- `/news/` — жаңылыктар
- `/register/` — катталуу формасы
- `/contact/` — байланыш
- `/admin/` — башкаруу панели

## API жана Swagger

Сервер иштеп турганда интерактивдүү Swagger документациясы:

```text
http://127.0.0.1:8000/api/docs/
```

OpenAPI схемасы:

```text
http://127.0.0.1:8000/api/schema/
```

Учурдагы ачык, окуу үчүн гана API endpoint'тери:

- `/api/categories/`
- `/api/teachers/`
- `/api/lessons/`
- `/api/news/`
- `/api/faq/`

Ар бир мугалим жана жаңылык `slug` аркылуу өзүнчө ачылат, мисалы: `/api/teachers/<slug>/`.

## Production

```bash
python manage.py collectstatic --noinput
gunicorn config.wsgi:application
```

Static файлдар WhiteNoise менен берилет. Медиа файлдар үчүн Nginx же булут сактагычты конфигурациялаңыз.

## Текшерүү

```bash
python manage.py check
python manage.py test
```
