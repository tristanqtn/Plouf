# 🌊 Welcome to Plouf Frontend!

This is the frontend service of Plouf. It is a Flask application that allows users to interact with the Plouf backend.

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

## 🚀 Running the Frontend

To run the backend locally, use the following command:

```bash
poetry run python -m app.main
```

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
