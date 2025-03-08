# 🌊 Welcome to Plouf Backend!

This is the backend service for the **Plouf** project, which manages and handles swimming pool data. The backend is built using Python, Pydantic, and MongoDB. This README will guide you through the setup, running, and testing of the project.

**Current Version**: 1.3.0

## 🚀 Backend Features

Currently, the backend provides the following features:

- **CRUD Operations**: Create, read, update, and delete operations for pools
- **Logging**: Record pool logs for each pool, including pH levels, chlorine concentrations, and cleaning dates, and view logs for each pool
- **Health Check**: A health check endpoint to verify the status of the backend and database.

## 🛠️ Backend Structure

The backend structure is organized as follows:

- **`app/`**: The main application code.

  - **`main.py`**: Entry point for the application, starts the server and handles routing.
  - **`Mongo.py`**: Handles interactions with the MongoDB database (CRUD operations).
  - **`Pools.py`**: Contains the models for pools and pool logs, including validation logic.
  - **`routes/`**: Contains FastAPI routers for handling API endpoints.
    - **`health/`**: Contains the health check endpoint.
    - **`pools/`**: Contains the CRUD endpoints for pools and pool logs.

- **`tests/`**: Unit and integration tests for the application.

## 📝 Requirements

Before running the backend, ensure you have the following installed:

- Python 3.12 or later
- Poetry for dependency management
- MongoDB (You can run it locally or use a cloud service like MongoDB Atlas)

## 📦 Installation

1. **Clone the repository**:

   ```bash
    git clone https://github.com/tristanqtn/Plouf.git
    cd Plouf/backend
   ```

2. **Install dependencies using Poetry**:

   ```bash
   poetry install
   ```

3. **Activate the virtual environment**:

   ```bash
   poetry shell
   ```

4. **Make sure you have MongoDB running locally**:
   - If you don't have MongoDB running locally, you can use Docker to run MongoDB:
     ```bash
     docker run -d -p 27017:27017 --name mongodb mongo
     ```
   - Or connect to a MongoDB cluster if you use MongoDB Atlas.

## 🐳 Build Docker Image

This backend is dockerized and can be run using Docker Compose. To build the Docker image, run the following command:

```bash
docker image build -t plouf-backend .
```

Tag the image with the name `plouf-backend:latest`:

```bash
docker tag plouf-backend plouf-backend:latest
```

Push the image to a container registry if needed:

```bash
docker push plouf-backend:latest
```

When running the whole application in Docker Compose, the backend is built automatically. You can skip this step. Just make sure not to have a previously built image with the same name.

## 🚀 Running the Backend

To run the backend locally, use the following command:

```bash
poetry run python -m app.main
```

This application requires a certain environment configuration to run. You can create a `.env` file in the root directory of the backend with the following content (a `.env.example` file is provided for reference):

```plaintext
MONGO_ADDRESS="localhost:27017"
MONGO_DATABASE="pool_database"
MONGO_COLLECTION="pool_collection"
MONGO_user="user"
MONGO_password="password"

BACKEND_ADDRESS="0.0.0.0"
BACKEND_PORT=8000
```

When running the whole application in Docker Compose, the environnement is not set anymore in the `.env` file but in the `docker-compose.yml` file. Be sure to set the environnement variables in the `backend` service and delete the `.env` file.

This will start the backend server. By default, the application will listen for requests on the specified port (check your `.env` file for configuration).

The backend should be set to run on `0.0.0.0:8000` to be accessible from the frontend. Since there's a port mapping on the local machine, the backend will be accessible at `http://localhost:8000`.

## 🧪 Running Tests

To run the tests and make sure everything works correctly, use:

```bash
poetry run pytest --disable-warnings
```

Debugging tests can be done with:

```bash
poetry run pytest --pdb -s
```

This will run all the unit and integration tests in the `tests/` directory.

## 🛠️ Additional Commands

- To enter the Poetry shell:

  ```bash
  poetry shell
  ```

- To install or update dependencies:

  ```bash
  poetry install
  ```

- To run your application:

  ```bash
  poetry run python -m app.main
  ```

- To run fastAPI in development mode:
  ```bash
  poetry run uvicorn app.main:app --reload
  ```

## 📚 API Documentation

The API documentation is available at `http://localhost:8000/docs` or `http://127.0.0.1:8000/redoc` when the backend is running. You can use the Swagger UI to interact with the API endpoints.

## Note

This application is not very secured, I know it's funny for a security engineer to develop an unsafe application. But I wanted to focus on the backend and the frontend, and I didn't want to spend too much time on the security part.

This why you shouldn't expose this application on the web. This is meants to be run locally in a private network. You clearly don't want to expose your pool pH level to the world ;) .

Here are some basic security measures that could be implemented:

- Use HTTPS
- Use a secret key for the JWT token to restrict access to the API
- Use a rate limiter to prevent brute force attacks
- Use a CORS policy to restrict access to the API
- Use prepared statements to prevent SQL injection

Feel free to contribute to the project and add these security measures if you want to!
