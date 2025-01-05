# 🌊 Welcome to Plouf!

Plouf is an open-source, self-hosted application designed to simplify the life of pool owners by offering an intuitive, user-friendly platform for tracking pool maintenance. With Plouf, users can log, review, and manage their pool’s health, ensuring sparkling, clean water all year round.

## 🚀 Features

- User-Friendly Maintenance Logging: Record key details such as pH levels, chlorine concentrations, and cleaning dates.
- Interactive Dashboard: Visualize maintenance history and receive reminders for future tasks.
- Self-Hosted Solution: Run Plouf on your own infrastructure using Docker Compose, giving you full control over your data.
- API-Driven Backend: FastAPI powers the backend, providing robust and scalable data processing.
- Responsive Frontend: A modern interface built with React ensures seamless usage on all devices.

## 🛠 Tech Stack

Backend: Python (FastAPI)
Frontend: Flask
Database: MongoDB
Containerization: Docker and Docker Compose for easy deployment and orchestration

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/tristanqtn/Plouf.git
cd Plouf
```

Build Docker images (this may take a few minutes, but it ensures that all dependencies are installed correctly):

```bash
docker compose build --no-cache
```

dcu
Start the application:

```bash
docker compose up
```

Access the frontend at http://localhost:3000 and the API at http://localhost:8000.

## 📚 Documentation

For more detailed information on setting up and using Plouf, please refer to each module documentation. Each component of the application is documented in detail, including installation instructions, API endpoints, and frontend components.

- [Backend Documentation](./backend/README.md)
- [Frontend Documentation](./frontend/README.md)

## 🤝 Contributing

We welcome contributions from the community! Please refer to the [CONTRIBUTING.md](./CONTRIBUTING.md) file for more information on how to get started.

## 📝 License

Plouf is licensed under the MIT License. See [LICENSE](./LICENSE) for more details.
