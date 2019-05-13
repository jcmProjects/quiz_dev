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


# ClassQuiz development blog

https://classquiz.wordpress.com/


# FIXME

