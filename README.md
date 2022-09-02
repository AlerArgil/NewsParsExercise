# Test
Testing exercise

# install or update Google Chrome 105.*.****.** version

# Create Enviroment
python3.X -m venv testenv

# Init Enviroment
source testenv/bin/activate

# Install all packages
pip install -r requirements.txt

# collect statics
python manage.py collectstatic

# Copy content .env.example to .env and set database credentials
# Init migration
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Для запуска парсинга следует стукнутся на 
POST {DOMAIN}/parsing