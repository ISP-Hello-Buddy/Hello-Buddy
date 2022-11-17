# Hello-Buddy
a web application for those who need some companion.

## Project Documents

All project documents are in the [Project Wiki](../../wiki/Home).

- [Vision Statement](../../wiki/Vision%20Statement)
- [User stories](../../wiki/User%20stories)
- [Requirements](../../wiki/Requirements)
- [Development Plan](../../wiki/Development%20Plan)

## Project Plan
- [Iteration 1](../../wiki/Iteration%201) and [Task Board](https://github.com/orgs/ISP-Hello-Buddy/projects/1/views/5)
- [Iteration 2](../../wiki/Iteration%202) and [Task Board](https://github.com/orgs/ISP-Hello-Buddy/projects/1/views/6)
- [Iteration 3](../../wiki/Iteration%203) and [Task Board](https://github.com/orgs/ISP-Hello-Buddy/projects/1/views/7)
- [Iteration 4](../../wiki/Iteration%204) and [Task Board](https://github.com/orgs/ISP-Hello-Buddy/projects/1/views/8)
- [Iteration 5](../../wiki/Iteration%205) and [Task Board](https://github.com/orgs/ISP-Hello-Buddy/projects/1/views/9)
- [Iteration 6](../../wiki/Iteration%206) and [Task Board](https://github.com/orgs/ISP-Hello-Buddy/projects/1/views/10)

## Code Review
- [Code Review Docs](https://docs.google.com/document/d/1RFhCYMuJuZ3QQoBI4gucfbdxvh8CyPY8-IAQZVW8HFE/edit#) and [Code Review Wiki](../../wiki/Code%20Review)
- [Code Review Summary](https://docs.google.com/document/d/1nu7uUv_mmL0KtEfbb8aDok8sVXAqvJvsyUHIno5fWPY/edit)

## How to install 
make sure that you have python in your computer
first, clone this repository by type this command in your terminal at your choosen path
```
git clone https://github.com/ISP-Hello-Buddy/Hello-Buddy.git
```
go to project directory
```
cd Hallo-Buddy
```

Start the virtual environment.

- on macos and linux
```
source env/bin/activate 
```
- on windows
```
. env/bin/activate
```
Before install programs form requirements please make sure in your computer have these things. 

- Geospatial libraries `Hint: PostGIS` 
- Spatial database `Hint: PostgreSQL` 
- `Note` : you can install program for GeoDjango Map Requirement from below [Click for see](https://github.com/ISP-Hello-Buddy/Hello-Buddy/tree/map#spacific-for-geodjango-map-requirement)

make sure that you install all the requirements by run this command, its can be whether pip, pip3
```
pip install -r requirements.txt
```
Create a new database by running migrations the database.
```
python3 manage.py migrate
```
In this time you can run server by use command 
```
python manage.py runserver
```
but you have python3 use command
```
python3 manage.py runserver
```
next you go to `http://127.0.0.1:8000/` or `localhost:8000/` for application.

## Spacific for GeoDjango Map Requirement

In general, GeoDjango installation requires:

1. Python and Django
2. Spatial database `Hint: PostgreSQL` 
3. Geospatial libraries `Hint: PostGIS` 

Platform-specific instructions

1.`For Mac OS`
- Pleas check your mac has xcode . If your mac has not xcode please run command
```
xcode-select --install
```

- Pleas check your mac has HomeBrew . If your mac has not HomeBrew please run command

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
```
brew install wget
```
- Before running any install command in Homebrew, it's good to ensure you are up to date.
```
brew update
```
- Install Spatial database
```
brew install postgresql
```
- Install Geospatial libraries
```
brew install postgis
```

2. `For Windows OS`

- Download and Install `PostgreSQL` Spatial database  
 - Download latest [PostgreSQL 12.x installer](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
  When the installer completes, it will ask to “Launch Stack Builder at exit?” 
 – keep this checked, as it is necessary to install PostGIS.
  
- Install `PostGIS` Geospatial libraries
- From within the Stack Builder to run outside of the installer, 
```
‣ Start PostgreSQL 12 Application Stack Builder.
‣ select PostgreSQL 12 (x64) on port 5432 from the drop down menu 
‣ Click next. Expand the Categories Spatial Extensions menu tree
‣ Select PostGIS X.Y for PostgreSQL 12.
‣ After clicking next, you will be prompted to confirm the selected package and “Download directory”. 
‣ Click next again, this will  download PostGIS .
‣ Click next to begin the PostGIS installer.
‣ Select the default options during install. 
‣ The install process includes three Yes/No dialog boxes, the default option for all three is “No”.
```

- Install `psycopg2`
- The psycopg2 Python module provides the interface between Python and the PostgreSQL database. psycopg2 can be installed via pip within your Python virtual environment.
- Install  `psycopy2` run this commmand
```
pip install psycopg2
```
 Note: You can find more detail on GeoDjango's [here](https://docs.djangoproject.com/en/4.1/ref/contrib/gis/install/#spatial-database).

