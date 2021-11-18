from os import sep
from os.path import join, dirname, realpath

PROJECT_ROOT = join(sep, *dirname(realpath(__file__)).split(sep)[: -1])
DB_ROOT = join(PROJECT_ROOT, 'db')
FIG_ROOT = join(PROJECT_ROOT, 'figs')
DB_PATH = join(DB_ROOT, "{DB_NAME}")
LOG_PATH = join(DB_ROOT, "{LOG_NAME}")
FIG_PATH = join(FIG_ROOT, "{FIG_NAME}.png")
