# CLASSQUIZ

**Tema:** Desenvolvimento e implementação em contexto realista do sistema CLASSQUIZ

**Orientador:** Vítor Manuel Ferreira dos Santos

**Autor:** João Carlos da Silva moreira (jcmoreira@ua.pt)


# Installation

*This project requires Python 3.6 or higher.*

**MySQL:**
To install MySQL (version 5.6 or higher) on Ubuntu 18.04: https://dev.mysql.com/downloads/mysql/

During installation, setup root's password as: password

**Virtual Environment:**
```bash
pip3 install virtualenv
```
```bash
cd project_folder
virtualenv venv
```

To activate the Virtual Environment:
```bash
source venv/bin/activate
```

**Requirements**
After activating the Virtual Environment, run the following command to install the required packages:
```bash
pip3 install -r requirements.txt
```

# Migrations

With all the above set up, navigate to `quiz_dev/` folder, containing the file `manage.py` and run the following:
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```
```bash
python3 manage.py makemigrations users
python3 manage.py migrate users
```
```bash
python3 manage.py makemigrations quiz
python3 manage.py migrate quiz
```

# Usage

The commands required the Virtual Environment to be activated.

To create a new Super User:
```bash
python3 manage.py createsuperuser
```

To start the web application:
```bash
python3 manage.py runserver 0.0.0.0:8000
```

To access the main page, open the browser and navigate to `localhost:8000`.

To access the admin page, open the browser and navigate to `localhost:8000/admin`.

You'll need to create a new `Course` within the admin page. After that, you'll need to associate it with an existing `User` by creating a new `ProfileCourse`. 

When creating a new `ProfileCourse`, if the `Profile` option appears to be blank, you'll need to add a first and last name to the `User`. This can be done by editing it's `Profile`.

The CLASSQUIZ system will only work with it's dedicated terminals, and when connected to it's dedicated network.

Network credentials:

SSID: CLASSQUIZ

PASSWORD: password


# ClassQuiz development blog

https://classquiz.wordpress.com/


# FIXME

