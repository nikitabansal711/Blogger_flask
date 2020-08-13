# Blogger

## Technologies used:

>* Flask framework
>* Python
>* Html, css for templates in frontend
>* Database used: Postgresql
---

### To run the project:
 * Open up your command terminal
 * Clone the project using ```git clone git@gitlab.com:mountblue/cohort-13-python/flask-toyproject-nikita.git```


>#### Set up your own virtual environment using following comands:
 *  ```sudo apt-get install python3-pip```
 *  ```sudo pip3 install virtualenv```
 *  ```virtualenv venv```
 *  ```source venv/bin/activate```
 *  cd inside the app directory
 *  ```pip install -r requirements.txt```
 ---

 >#### Install postgresql
 * ```sudo apt update```
 * ```sudo apt install postgresql postgresql-contrib```
---

 >#### Specify the postgres user
 * specify your postgres superuser username and password in the <strong>.env</strong> file in DATABASE_URL environment variable
 * else activate postgres using ```sudo -u postgres psql```
 * create one using command: ```CREATE USER temp WITH PASSWORD 'password';```
 * give the superuser access using: ```ALTER USER temp WITH SUPERUSER;```
---

 >#### Run the code
 * cd inside the helper_python_scripts
 * run helper_create_db.py to create database using command: ```python helper_create_db.py```
 * run the command ```flask db upgrade``` to apply the migration scripts
 * run the command: ```python helper_data_loader.py``` to load sample data into the database
 * run the command: ```flask run``` to run the server 
 * Now you have the access to the BLOGGER website
 * For better understanding of the site, have a look at the snapshots file present in the root directory
 * Sample user credentials can be seen from <strong>sample_users.txt</strong> file to access their blogs and perfrom CRUD operations
 * In order to perform delete and update operations, click on the dustbin and pencil icon respectively while accessing Blogger
 * run command: ```python helper_db_dropper.py``` to drop database
---

 