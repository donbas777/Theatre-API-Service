# Theatre API

API service for theatre management written on DRF

## Installing using GitHub

### Install PostgreSQL and create database

1. Clone the repository:
    ```bash
    git clone https://github.com/donbas777/Theatre_API_Service.git
    ```
   
2. Navigate to the project directory:
    ```bash
    cd Theatre_API_Service
    ```

3. Create a virtual environment:
    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:
    ```bash
    source venv/bin/activate
    ```

5. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

6. Set the following environment variables:
    ```bash
    set DB_HOST=<your db hostname>
    set DB_NAME=<your db name>
    set DB_USER=<your db username>
    set DB_PASSWORD=<your db user password>
    set SECRET_KEY=<your secret key>
    ```

7. Apply the database migrations:
    ```bash
    python manage.py migrate
    ```

8. Run the server:
    ```bash
    python manage.py runserver
    ```
   


## Run with Docker

Docker should be installed.

1. Build the Docker containers:
    ```bash
    docker-compose build
    ```

2. Start the Docker containers:
    ```bash
    docker-compose up
    ```

## Getting access

- Create a user via `/api/user/register/`
- Get an access token via `/api/user/token/`

## Features

- JWT authenticated
- Admin panel `/admin/`
- Documentation is located at `/api/doc/swagger/`
- Managing orders and tickets
- Creating plays with genres and actors
- Creating theatre halls
- Adding performances
- Filtering plays and performances
