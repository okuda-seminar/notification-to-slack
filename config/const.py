from os import sep
from os.path import join, dirname, realpath

PROJECT_ROOT = join(sep, *dirname(realpath(__file__)).split(sep)[: -1])
DB_ROOT = join(PROJECT_ROOT, 'dbs')
DB_PATH = join(DB_ROOT, "{DB_NAME}")
LOG_PATH = join(DB_ROOT, "{LOG_NAME}")