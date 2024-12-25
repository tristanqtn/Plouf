# 🌊 Welcome to Plouf Backend!

This is the backend service for the **Plouf** project, which manages and handles swimming pool data. The backend is built using Python, Pydantic, and MongoDB. This README will guide you through the setup, running, and testing of the project.

## 🛠️ Backend Structure

The backend structure is organized as follows:

- **`app/`**: The main application code.

  - **`main.py`**: Entry point for the application, starts the server and handles routing.
  - **`Mongo.py`**: Handles interactions with the MongoDB database (CRUD operations).
  - **`Pools.py`**: Contains the models for pools and pool logs, including validation logic.
  - **`routes/`**: Contains FastAPI routers for handling API endpoints.
    - **`heallth/`**: Contains the health check endpoint.
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

## 🚀 Running the Backend

To run the backend locally, use the following command:

```bash
poetry run python -m app.main
```

This will start the backend server. By default, the application will listen for requests on the specified port (check your `main.py` for configuration).

## 🧪 Running Tests

To run the tests and make sure everything works correctly, use:

```bash
poetry run pytest
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
