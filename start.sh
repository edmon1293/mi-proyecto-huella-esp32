#!/bin/bash

echo "🚀 Iniciando aplicación..."

# Ejecutar migraciones
echo "📦 Ejecutando migraciones de base de datos..."
python manage.py migrate --noinput

# Crear datos iniciales
echo "👤 Creando usuarios iniciales..."
python manage.py create_initial_data

# Recolectar archivos estáticos
echo "📁 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Iniciar Gunicorn
echo "✅ Iniciando servidor..."
exec gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 120 mi_proyecto.wsgi:application
