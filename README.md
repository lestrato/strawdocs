# strawdocs

*Version: 0.1*

## How to get started on your local development environment.
### Prerequisites:

program | download link
--- | ---
git | https://git-scm.com/downloads
python 2.7.x | https://www.python.org/downloads/
virtualenv | https://virtualenv.pypa.io/en/stable/installation/
mysql | http://dev.mysql.com/downloads/mysql/
Microsoft Visual C++ 9.0 | https://www.microsoft.com/en-us/download/details.aspx?id=44266

### Create project directory and environment

* `mkdir strawdocs && cd strawdocs`
* `virtualenv env`
* `source env/scripts/activate` *Activate the environment (each time you start a session working with the code)*

*Obtain source code and clone into code directory*

* `git clone https://github.com/lestrato/strawdocs.git main`
* `cd main`

*Your Directory structure will look like this:*
```
strawdocs
├── main
│   ├── apps  
│   ├── main
│   ├── static
├── env
```

### Install requirements
*from within strawdocs/main directory*

* `pip install -r requirements.txt`

*if you're having errors installing mysql-python, consider downloading the file for your appropriate platform from here:*
* http://www.lfd.uci.edu/~gohlke/pythonlibs/#mysql-python
* Install using: `pip install [file-name]`

### Customize local settings to your environment
* `cp main/settings.py.example main/settings.py`
* Edit the main/settings.py file and insert local credentials for DATABASES

### Migrate databases, build front-end components
* `./manage.py migrate`
* `./manage.py createsuperuser` or `winpty python manage.py createsuperuser` *follow prompts to create your first admin user account*

### Run a server locally for development
* `./manage.py runserver`
* Navigate to http://localhost:8000/
* Login with superuser or create new account
