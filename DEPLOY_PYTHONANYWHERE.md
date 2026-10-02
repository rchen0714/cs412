# Deploy TerrierStudy on PythonAnywhere

This publishes the existing `cs412` project (Django 5.2, app `terrier_study`) at:

https://rchen0714.pythonanywhere.com

The home page redirects to TerrierStudy. The old path still works:

https://rchen0714.pythonanywhere.com/terrier_study/

Blog, quotes, mini_insta, restaurant, voter_analytics, dadjokes, and the other class apps stay in the project. Do not delete them.

Use a **Bash console** on PythonAnywhere for the commands below (Consoles tab, then Bash). The `$` is the prompt. Do not type `$`.

## 1. Create the account

1. Open https://www.pythonanywhere.com/registration/register/beginner/ and create a **Beginner (free)** account.
2. The username has to be **`rchen0714`**. The public site is always `https://<username>.pythonanywhere.com`, and these instructions use that name.
3. Confirm the email PythonAnywhere sends. You cannot start a web app until the address is confirmed.
4. Log in at https://www.pythonanywhere.com/login/.

If that username already exists and it is your account, log in with it. Do not create a second account. A different username would be a different website, and you would change `PYTHONANYWHERE_HOST` in the WSGI file in step 6.

## 2. Clone the project

In a Bash console:

```bash
cd /home/rchen0714
git clone https://github.com/rchen0714/cs412.git
cd /home/rchen0714/cs412
```

That creates `/home/rchen0714/cs412` (the folder that contains `manage.py`).

If GitHub asks you to log in, the repository is private. Create a GitHub personal access token and use that as the password. Your GitHub account password will not work. A public repository clones with no login.

Leave `db.sqlite3` in place. It is the site's data, not an empty file. See "Database" below.

## 3. Create the virtualenv and install packages

PythonAnywhere uses pip, not Pipenv. The Pipfile asks for **Python 3.13**. Use that same version for the virtualenv and the web app.

```bash
mkvirtualenv --python=/usr/bin/python3.13 cs412-virtualenv
pip install -r /home/rchen0714/cs412/requirements.txt
```

The virtualenv's full path is:

`/home/rchen0714/.virtualenvs/cs412-virtualenv`

If the console says `mkvirtualenv: command not found`, run this instead:

```bash
python3.13 -m venv /home/rchen0714/.virtualenvs/cs412-virtualenv
source /home/rchen0714/.virtualenvs/cs412-virtualenv/bin/activate
pip install --upgrade pip
pip install -r /home/rchen0714/cs412/requirements.txt
```

If the Manual configuration screen in step 5 has no Python 3.13 choice, use 3.12 for **both** the virtualenv and the web app (`/usr/bin/python3.12`). Django 5.2.5 supports 3.12 and 3.13. The two must match.

`pip install` can take several minutes. Plotly is large. Wait until the prompt comes back. You only install once.

## 4. Make a new secret key

The secret that used to be in `settings.py` was committed on GitHub. Do not reuse it.

With the virtualenv still active:

```bash
cd /home/rchen0714/cs412
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the whole line it prints. You will paste it into the WSGI file. Do not commit it, and do not put it in `settings.py`.

## 5. Create the web app

1. Open the **Web** tab.
2. Click **Add a new web app**.
3. Confirm the domain `rchen0714.pythonanywhere.com`.
4. Choose **Manual configuration**. Do not choose the Django option. That option starts a brand-new project and will not use this code.
5. Choose **Python 3.13** (or 3.12, if that is what you used in step 3).
6. On the Web tab, find **Virtualenv** and enter:

   `cs412-virtualenv`

   PythonAnywhere should expand it to `/home/rchen0714/.virtualenvs/cs412-virtualenv`.
7. Under **Code**, set both of these to the project folder:

   - Source code: `/home/rchen0714/cs412`
   - Working directory: `/home/rchen0714/cs412`

## 6. Replace the WSGI file

The file to edit is **not** `cs412/wsgi.py` inside the project. On the Web tab, under Code, click the link to the WSGI configuration file. It is this path:

`/var/www/rchen0714_pythonanywhere_com_wsgi.py`

Delete everything in that file and paste this. Replace `paste-the-new-key-here` with the key from step 4.

```python
import os
import sys

path = "/home/rchen0714/cs412"
if path not in sys.path:
    sys.path.insert(0, path)

os.environ["DJANGO_SETTINGS_MODULE"] = "cs412.settings"

# Production. Local runserver stays in debug mode when these are unset.
os.environ["DJANGO_DEBUG"] = "False"
os.environ["DJANGO_SECRET_KEY"] = "paste-the-new-key-here"

# Default host is already rchen0714.pythonanywhere.com.
# Uncomment the next line only if you need a different host.
# os.environ["PYTHONANYWHERE_HOST"] = "rchen0714.pythonanywhere.com"

# Uncomment after you create a new Google Maps key for this domain.
# os.environ["GOOGLE_MAPS_API_KEY"] = "paste-a-new-maps-key-here"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Save the file. The quotes around the secret key stay. The key itself must not contain a quote character. `get_random_secret_key()` does not emit quotes.

`DJANGO_DEBUG=False` is required. Without a `DJANGO_SECRET_KEY`, the site will refuse to start, on purpose.

## 7. Static and media files

On the Web tab, open **Static files**. Add these two rows. The URL needs the leading slash. The path is the full directory.

| URL | Directory |
| --- | --- |
| `/static/` | `/home/rchen0714/cs412/staticfiles` |
| `/media/` | `/home/rchen0714/cs412/media` |

Do not use `/rc071404/static/` or `/rc071404/media/` here. That prefix is only for `cs-webapps.bu.edu`. On PythonAnywhere the settings leave `STATIC_URL` at `/static/` and `MEDIA_URL` at `/media/`.

`/media/` serves uploaded images already in the repository (blog and mini_insta) and anything uploaded later.

## 8. Migrate, collectstatic, and the admin user

In the Bash console, from the project directory, with the virtualenv active (`workon cs412-virtualenv` if the prompt does not show it):

```bash
cd /home/rchen0714/cs412
python manage.py migrate
python manage.py collectstatic --noinput
```

`migrate` should report that there are no migrations to apply. The tables are already in `db.sqlite3`. Do not delete that file and do not run `flush`.

`collectstatic` copies CSS and the Django admin styles into `/home/rchen0714/cs412/staticfiles`. Re-run it after you change files in `static/`.

An admin account named `admin` is already in the database (email `rc071404@bu.edu`). Log in at https://rchen0714.pythonanywhere.com/admin/ with the password you used for that account. If you do not remember it, reset it. Do not create a second admin unless you want one:

```bash
python manage.py changepassword admin
```

To add a different superuser:

```bash
python manage.py createsuperuser
```

These commands do not read the WSGI file. They are safe with the default local settings. The **website** uses the WSGI values from step 6.

## 9. Reload

On the Web tab, click the green **Reload** button for `rchen0714.pythonanywhere.com`.

Then open:

- https://rchen0714.pythonanywhere.com/ (redirects to TerrierStudy)
- https://rchen0714.pythonanywhere.com/terrier_study/
- https://rchen0714.pythonanywhere.com/static/styles_terrierstudy.css (the CSS file itself, not a blank page)

If the site shows an error, open the **Error log** link on the Web tab. A red error at reload usually means the virtualenv path, the WSGI path, or `DJANGO_SECRET_KEY` is wrong.

## 10. Keep the free site online

Free web apps are turned off unless you extend them from the Web tab.

- Accounts created after 15 January 2026 show **Run until 1 month from today**. Click it at least once a month.
- Older free accounts may still show **Run until 3 months from today**. Click that before the date on the page.

PythonAnywhere emails a reminder about a week before the site is disabled. Log in and click the button. The site can stay free as long as you keep extending it. There is one free web app, one web worker, 512 MiB of disk, and 100 CPU-seconds per day.

## What is stored, and what you should not delete

`db.sqlite3` stays in git on purpose (about 19 MB). Cloning the repository is how the live site gets the existing TerrierStudy data:

- 14 buildings, 18 study rooms, 6 reviews, 4 favorites, 1 profile
- the `admin` user and the other practice logins
- the other class apps' rows (blog, mini_insta, dadjokes, marathon results, voter file)

SQLite is the right database on the free tier. PythonAnywhere keeps the file on disk. New signups, reviews, and favorites written on the live site are saved in `/home/rchen0714/cs412/db.sqlite3` on the server. A later `git pull` can overwrite that file if you also commit a database from your laptop. After the site is public, do not commit `db.sqlite3` from another machine over the server's copy. Copy the server file down first if you need a backup.

## Updating the site later

```bash
cd /home/rchen0714/cs412
workon cs412-virtualenv
git pull
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Then click **Reload** on the Web tab. `git pull` will not change the WSGI file, because that file lives outside the repository.

## Free-tier limits that affect this project

The Django code does not call other websites. There is no `requests` or `urllib` use. Free accounts can only make outbound HTTP calls to an allowlist, and that limit does not apply to your visitor's browser.

What the browser loads, from the visitor's own computer:

- The TerrierStudy map loads `https://maps.googleapis.com/maps/api/js`. Tiles and pins will fail if the Google key rejects `https://rchen0714.pythonanywhere.com`. The rest of the page still works. Several building and room photos are also plain image links to `www.bu.edu`, Wikimedia, Twitter, and Google image caches. Those are browser requests too.
- Stylesheets import Google Fonts (`fonts.googleapis.com`). If a browser blocks that, the page uses fallback fonts.
- Voter Analytics links out to `https://www.google.com/maps/search/...`. That is a normal link, not a server request.

Plotly (marathon details and voter graphs) pastes the chart library into the HTML. It does not download it from the internet. Those pages are still a poor fit for the free tier: the voter graph view walks about 59,000 voters in Python, and each chart adds several megabytes of JavaScript. A free account has 100 CPU-seconds per day and one web worker. TerrierStudy itself is small (14 buildings) and does not use Plotly. Opening the voter graphs page a few times can use up the day's CPU allowance, after which PythonAnywhere throttles the app.

Two JSON routes already error, separate from hosting: `/terrier_study/api/favorites/` has no queryset, and `/terrier_study/api/reviews/` asks for a `reviewer_name` field the model does not have. The HTML pages for favorites and reviews do not use those routes. Building and study-room JSON, which the map uses, returns 200.

## Optional deployment check

With the virtualenv active:

```bash
cd /home/rchen0714/cs412
DJANGO_DEBUG=False DJANGO_SECRET_KEY='the-same-key-as-in-the-wsgi-file' python manage.py check --deploy
```

`security.W008` will still warn that `SECURE_SSL_REDIRECT` is off. Leave it off. PythonAnywhere already redirects HTTP to HTTPS, and Django's redirect loops on that proxy.

## If something looks wrong

- **DisallowedHost / 400.** `PYTHONANYWHERE_HOST` must be `rchen0714.pythonanywhere.com` with no `https://` and no trailing slash. That value is the default. Reload after any WSGI edit.
- **CSS missing.** The static-files row must be URL `/static/` and directory `/home/rchen0714/cs412/staticfiles`, and `collectstatic` must have been run. Then reload.
- **Uploaded pictures missing.** The media row must be URL `/media/` and directory `/home/rchen0714/cs412/media`.
- **Map has no tiles.** The page still loads. The map is drawn by the visitor's browser, which calls Google. The key in the repository may only allow `cs-webapps.bu.edu`. In Google Cloud, add `https://rchen0714.pythonanywhere.com/*` to the key, or put a new key in `GOOGLE_MAPS_API_KEY` in the WSGI file and reload. Because the old key is public, creating a new one is safer.
- **`ImproperlyConfigured` about `DJANGO_SECRET_KEY`.** Paste a new key in the WSGI file. Do not turn `DJANGO_DEBUG` back on to hide that error.
