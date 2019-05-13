# CLASSQUIZ

CLASSQUIZ is a system that aims to increase the participation of students within high attendance classes, through the carrying of surveys.

The system developed consists of 3 mains parts:

- Individual Terminals, through which the students can answer the surveys;

- A server, located within the classroom, which validates the students ID, their answers;

- A web application, which allows the creating and execution of the surveys.


## Installation

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

**Requirements:**

After activating the Virtual Environment, run the following command to install the required packages:
```bash
pip3 install -r requirements.txt
```

## Migrations

With all the above set up, navigate to `quiz_dev/django_quiz/` directory, containing the file `manage.py`, and run the following:
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

## Usage

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

**Network credentials:**

SSID: CLASSQUIZ

PASSWORD: password


## Terminal Firmware Installation

To upload `quiz_dev/firmware/firmware.ino` to the terminal through Arduino IDE, you'll need to do the following:

1. Install Arduino IDE and open it

2. Go to File > Preferences

3. Enter `http://arduino.esp8266.com/stable/package_esp8266com_index.json` into the “Additional Board Manager URLs” field, then click ”OK”

4. Go to Tools > Board > Board Manager

5. Scroll down, select the ESP8266 board menu and install “esp8266”

6. Choose your ESP8266 board from Tools > Board > NodeMCU 1.0 (ESP-12E Module)

7. Install the package MFRC522 *by GithubCommunity* from Sketch > Include Libraries > Manage Libraries

8. Following the previous step, install the package ESP8266RestClient *by fabianofranca*

7. Finally, re-open your Arduino IDE

*NOTE:* Existing terminals are already updated.


## Additional Notes

Since this project works without an Internet connection, JavaScript and CSS libraries usually obtained through CDN are already installed within the directory `django_quiz/quiz/static/quiz/`.


## ClassQuiz Development Blog

https://classquiz.wordpress.com/


## Credits

**Author:** João Carlos da Silva moreira (jcmoreira@ua.pt)


## FIXME

