from os import getenv, sep
from os.path import join, dirname, realpath

from dotenv import load_dotenv

PROJECT_ROOT = join(sep, *dirname(realpath(__file__)).split(sep)[: -1])

DB_ROOT = join(PROJECT_ROOT, 'db')
FIG_ROOT = join(PROJECT_ROOT, 'figs')

DB_PATH = join(DB_ROOT, "{DB_NAME}")
LOG_PATH = join(DB_ROOT, "{LOG_NAME}")
FIG_PATH = join(FIG_ROOT, "{FIG_NAME}.png")

load_dotenv()
GITHUB_TOKEN = getenv("GITHUB_TOKEN")
