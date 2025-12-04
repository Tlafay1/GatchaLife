from .settings import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "test_db.sqlite3",
    },
    "ticktick": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "test_ticktick.sqlite3",
    }
}
