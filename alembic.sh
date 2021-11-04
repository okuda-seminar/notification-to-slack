#!/bin/sh
alembic upgrade head
python test/test_alembic.py
