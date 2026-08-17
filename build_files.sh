#!/usr/bin/env bash
# Vercel build script
# Vercel'де деплой учурунда аткарылат.
# Бул скрипт pip install кылгандан КИЙИН иштейт.
set -o errexit

echo "==> Collecting static files..."
python manage.py collectstatic --noinput

echo "==> Running database migrations..."
python manage.py migrate --noinput

echo "==> Build complete."
