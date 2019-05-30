### Requerimientos Básicos

- React 16.4.0
- Django 1.11
- Django Rest Framework 3.8.2
- Django CORS Headers 2.2.0
- Python 3.5 (and up)
- virtualenv
- npm
- Git

### Recommended Start
```
Se genera el ambiente virtual, primero descargando e instalando virtualenv

sudo apt-get install virtualenv
sudo apt-get install python3 libmysqlclient-dev
sudo apt-get install npm binutils libproj-dev gdal-bin


s un entorno de ejecución para JavaScrip

se descarga el repositorio en la ruta 

git clone -b <branch> <ruta_del_git>

luego se accede a la carpeta y se instala el ambiente virtual con el siguiente código

virtualenv -p python3 .
El repositorio actual está instalado en python versión 3.6.5, asegúrese de haber instalado una version igual o posterior

se activa el ambienta virtual
source bin/activate

Se instalan todos los paquetes necesarios para el funcionamiento del backened de django
pip install -r requirements.txt

luego se instala el entorno de ejecución de javascript necesario para el funcionamiento del frontend


src/django-project-ui
npm install
npm install react-cookies -save
npm install whatwg-fetch --save
npm install leaflet
npm install d3 .
npm install jquery

A continuación se crea la base de datos en MySQL: 
  CREATE DATABASE hydrology;
  CREATE USER 'sample_user'@'localhost' IDENTIFIED BY 's@mple_p@ss';
  GRANT ALL PRIVILEGES ON * . * TO 'sample_user'@'localhost';
  FLUSH PRIVILEGES;
  
python manage.py migrate 
python manage.py makemigrations meta
python manage.py makemigrations data
python manage.py makemigrations hydraulics
  USE hydrology;
  ALTER TABLE  data_databasin ADD UNIQUE (fk_id,date);
python manage.py migrate

./manage.py shell < database_migration.py
./manage.py shell < basins.py
