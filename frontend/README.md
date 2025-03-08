# 🌊 Welcome to Plouf Frontend!

This is the frontend service of Plouf. It is a Streamlit application that allows users to interact with the Plouf backend.

**Current Version**: 2.1.0

## 🚀 Frontend Features

Currently, the frontend provides the following features:

- **View Pools**: View a list of all pools in the database
- **Add Pool**: Add a new pool to the database
- **Update Pool**: Update an existing pool in the database
- **Delete Pool**: Delete an existing pool from the database
- **Pool Log Management**: View, add, and delete logs for each pool
- **Pool Log Visualization**: Visualize logs for each pool using charts

## 🛠️ Frontend Structure

The frontend structure is organized as follows:

- **`app/`**: The main application code.
  - **`main.py`**: Entry point for the application, starts the server and UI.
  - **`config.py`**: Contains the configuration settings for the application.
  - **`templates/`**: Contains the Streamlit templates.
    - **`home.py`**: Home page for the frontend application.
    - **`health.py`**: Health and monitoring page.
    - **`pools.py`**: Contains the templates for managing pool logs.
    - **`pools_details.py`**: Contains the templates for managing pool logs.

During development, I encoutered some issues with sending requests from the Streamlit templates to the backend. This is mainly due to CORS issues. The solution was to create an intermediary API in the frontend that forwards requests to the backend. This way, the frontend can send requests to the intermediary API, which then forwards them to the backend. This is a workaround to avoid CORS issues.

## 📝 Requirements

Before running the frontend, ensure you have the following installed:

- Python 3.12 or later
- Poetry for dependency management
- A running instance of the Plouf backend

## 📦 Installation

1. **Clone the repository**:

   ```bash
    git clone https://github.com/tristanqtn/Plouf.git
    cd Plouf/frontend
   ```

2. **Install dependencies using Poetry**:

   ```bash
   poetry install
   ```

3. **Activate the virtual environment**:

   ```bash
   poetry shell
   ```

4. **Make sure you have Plouf backend running locally**
   - If you don't have the backend running locally, follow the instructions in the backend [README](../backend/README.md) to run the backend.

## 🐳 Build Docker Image

This backend is dockerized and can be run using Docker Compose. To build the Docker image, run the following command:

```bash
docker image build -t plouf-frontend .
```

Tag the image with the name `plouf-frontend:latest`:

```bash
docker tag plouf-frontend plouf-frontend:latest
```

Push the image to a container registry if needed:

```bash
docker push plouf-frontend:latest
```

When running the whole application in Docker Compose, the frontend is built automatically. You can skip this step. Just make sure not to have a previously built image with the same name.

## 🚀 Running the Frontend

To run the frontend locally, use the following command:

```bash
poetry run streamlit run /app/main.py --server.port=3000
```

This application requires the Plouf backend to be running. Make sure the backend is running before starting the frontend. It also needs some environment variables to be set. You can set them in a `.env` file in the root directory of the frontend. Here is an example of the `.env` file (a `.env.example` file is provided for reference):

```plaintext
BACKEND_ADDRESS="127.0.0.1"
BACKEND_PORT=8000

FRONTEND_ADDRESS="127.0.0.1"
FRONTEND_PORT=3000

FRONTEND_VERSION="0.1.0"
```

When running the whole application in Docker Compose, the environnement is not set anymore in the `.env` file but in the `docker-compose.yml` file. Be sure to set the environnement variables in the `frontend` service and delete the `.env` file.

This will start the frontend server. By default, the application will listen for requests on the specified port (check your `.env` file for configuration).

The frontend should be set to run on `0.0.0.0:3000` to be accessible. Since there's a port mapping on the local machine, the backend will be accessible at `http://localhost:3000`.

## 🛠️ Additional Commands

- To enter the Poetry shell:

  ```bash
  poetry shell
  ```

- To install or update dependencies:

  ```bash
  poetry install
  ```
