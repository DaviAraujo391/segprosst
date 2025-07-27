#!/usr/bin/env bash
# build.sh

echo "📦 Rodando makemigrations..."
python manage.py makemigrations --noinput

echo "🛠️ Aplicando migrations..."
python manage.py migrate --noinput

echo "🎨 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput
