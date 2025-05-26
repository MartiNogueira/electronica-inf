#!/bin/bash

# 📁 Navegar al proyecto
cd /Users/martinogueira/electronica-inf-1/drivein-app/backend || exit

echo "🚀 Activando entorno virtual..."
source venv/bin/activate

echo "📦 Exportando FLASK_APP=run.py"
export FLASK_APP=run.py

echo "🧱 Creando tablas si no existen..."
flask shell <<EOF
from app import db
db.create_all()
EOF

echo "🌐 Levantando servidor Flask en http://localhost:5000"
flask run
