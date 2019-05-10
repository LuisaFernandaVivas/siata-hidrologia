- React 16.4.0
- Django 1.11
- Django Rest Framework 3.8.2
- Django CORS Headers 2.2.0
- Python 3.5 (and up)

### Recommended Start
```
Se genera el ambiente virtual, primero descargando virtualen

sudo apt-get install virtualenv

s un entorno de ejecución para JavaScrip

se descarga el repositorio en la ruta 

git clone ...

luego se accede a la carpeta y se instala el ambiente virtual con el siguiente código

virtualenv -p python3 .

se activa el ambienta virtual
source bin/activate

en el directorio src, se instalan totos los paquetes necesarios para el funcionamiento del backened de django
cd src
pip install -r requirements.txt

luego se intala el entorno de ejecución de javascript necesario para el funcionamiento del frontend


cd reactify-ui
npm install
npm install react-cookies -save
npm install whatwg-fetch --save
npm install leaflet
npm install d3 .
npm install jquery

python manage.py migrate 
python manage.py makemigrations meta
python manage.py makemigrations data
python manage.py makemigrations hydraulics



ALTER TABLE  data_databasin ADD UNIQUE (fk_id,date)

s un entorno de ejecución para JavaScrip
configure el archivo que se encuentra en la ruta 
src/django-project/setting.py

