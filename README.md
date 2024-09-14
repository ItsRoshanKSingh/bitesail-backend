# BiteSail-backend

Backend for BiteSail - A Django and Django REST Framework-based API service for a personalized recipe recommendation system, supporting user authentication, recipe management, and machine learning-based recommendations for culinary discovery and exploration.

## Project Structure

```
bitesail-backend/
├── project/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   └── core/
│       ├── __init__.py
│       ├── management/
│       |   ├── __init__.py
│       |   ├── commands/
│       |       ├── __init__.py
│       |       ├── wait_for_db.py
│       ├── tests/
│       ├── apps.py
│       ├── models.py
│       ├── serializers.py
│       └── urls.py
├── requirements.txt
├── requirements.dev.txt
├── Dockerfile
├── docker-compose.yml
└── manage.py
```

## Prerequisites

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

1. **Clone the Repository**

   ```sh
   git clone https://github.com/ItsRoshanKSingh/bitesail-backend.git
   cd bitesail-backend
   ```

2. **Build and Run the Docker Containers**

   Use Docker Compose to build and start the containers:

   ```sh
   docker-compose up --build
   ```

   This command builds the Docker images and starts the containers for the Django application and PostgreSQL database.

3. **Access the Application**

   Open your web browser and navigate to `http://localhost:8000` to access the Django application.

## Accessing API Documentation

### Swagger UI

To explore and test the API endpoints, navigate to the following URL in your web browser:

- **Swagger UI**: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)

### API Schema

For a raw OpenAPI schema of your API, visit:

- **API Schema**: [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)


## Docker Configuration

- **Dockerfile**: Defines the environment for the Django application, using Python 3.11 on an Alpine base image.
- **docker-compose.yml**: Configures the services for the Django application and PostgreSQL database, defining how they interact and are connected.

## Environment Variables

For PostgreSQL, set the following environment variables:
- `POSTGRES_DB`: Name of the database.
- `POSTGRES_USER`: Username for the database.
- `POSTGRES_PASSWORD`: Password for the database.

## Running Migrations

After starting the containers, apply the initial migrations:

```sh
docker-compose run web python manage.py migrate
```

## Stopping the Containers

To stop and remove the containers, run:

```sh
docker-compose down
```

## Testing

Run tests within the Docker container using:

```sh
docker-compose run web python manage.py test -v2
```
where,v2 Shows each test that runs, including those that passed
---


## Code Quality and Linting

### Flake8

`flake8` is used for checking code style and quality.

#### Running Flake8

To run `flake8` in your Docker container:
1. Run `flake8`:

   ```bash
   docker-compose run --rm web flake8
   ```

## Troubleshooting

- **Container Logs**: Check container logs for errors:

  ```sh
  docker-compose logs
  ```

- **Database Connection Issues**: Verify that the database container is running and environment variables are correctly configured.

## Contributing

Contributions are welcome! Please submit pull requests or open issues for any improvements or bug fixes. Ensure new code adheres to the project's code style and includes tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please contact the maintainer at [Roshan Singh](mailto:ItsRoshanKSingh@gmail.com).