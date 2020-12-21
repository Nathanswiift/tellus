"""
Config-fil
"""


class TellusConfig:
    DEV_ENV = "localhost"
    DEV_ENV_PORT = 5000

    DB_NAME = "booking"
    DB_HOST = "localhost"
    DB_USER = "taskeru"
    DB_PW = ""

    TEMPLATE_CACHE_PATH = "api/cache"
    TEMPLATE_PATH = "api/templates"

    ENCODE = "utf8"
