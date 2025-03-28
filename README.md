# ServiceSphereV2
## A-Z Household Services Application V2
### Description Of Project
It is a multi-user app (requires one admin and other service professionals/customers) which acts as platform for providing comprehensive home servicing and solutions, made for the project of the MAD - II course (Jan 2025 term).

### Technologies Used
- **Flask**: Backend framework in Python for building the web application.
- **Flask-Restful**: For building restful APIs in Flask.
- **Flask-JWT-Extended**: For authentication of users handling JSON Web Tokens.
- **Flask-Caching**: For caching.
- **Vue JS**: JavaScript framework for building Frontend of the web application.
- **Vite**: For Frontend tooling.
- **SQLAlchemy**: ORM (Object-Relational Mapping) tool for database interactions.
- **SQLite3**: Database management system for storing application data.
- **CSS + Bootstrap5**: For design and styling.
- **Werkzeug**: For hashing passwords.
- **ChartJS**: For making charts.
- **Celery**: For asynchronous background tasks.
- **Redis**: For Caching and as a message broker.

## Setup Frontend

```sh
cd FrontendVue
```
```sh
npm install
```
```sh
npm run dev
```
## Setup Backend

### Run WSL and activate virtual environment
```sh
cd BackendFlask
```
```sh
wsl
```
```sh
python3 -m venv venv
```
```sh
source ../venv/bin/activate
```
### Install Dependencies
```sh
pip -r requirements.txt
```
### Start Redis
```sh
sudo service redis-server start
```
### Start Celery worker with beat
```sh
celery -A app.celery worker --loglevel=info --beat
```
### Run Flask Application
```sh
flask run
```
