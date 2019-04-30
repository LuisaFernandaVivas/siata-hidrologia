- React 16.4.0
- Django 1.11
- Django Rest Framework 3.8.2
- Django CORS Headers 2.2.0
- Python 3.5 (and up)

### Recommended Start
```

virtualenv -p python3 .
source bin/activate
cd src
pip install -r requirements.txt
cd reactify-ui
npm install
npm install react-cookies -save
npm install whatwg-fetch --save
npm install leaflet
npm install d3 .
npm install jquery

for improve query performance add this statement to the database
ALTER TABLE  data_databasin ADD UNIQUE (fk_id,date)
