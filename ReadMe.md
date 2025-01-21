# Crane Cloud Monitoring API

[![Prod](https://github.com/crane-cloud/monitoring-api/actions/workflows/prod.yml/badge.svg)](https://github.com/crane-cloud/monitoring-api/actions/workflows/prod.yml)

The Crane Cloud Monitoring API provides a backend service for monitoring resource usage (CPU, memory, network) within a Kubernetes environment. It interfaces with Prometheus to fetch and aggregate metrics data.

## Features

- RESTful API endpoints to fetch metrics for projects and applications.
- Integration with Prometheus for metrics collection.
- Docker containerization for easy deployment and scaling.
- Helm charts for Kubernetes deployments.

## Prerequisites

- Docker and Docker Compose
- Python 3.10
- Helm 3 for Kubernetes deployment
- Access to a Kubernetes cluster (for staging/production environments)

## Local Development Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/crane-cloud/monitoring-api.git
   cd monitoring-api
   ```

2. **Environment Variables:**

   Copy the `.env.example` to `.env` and modify the environment variables according to your local setup.

3. **Start the application:**

   Use Docker Compose to build and run the local development environment:

   ```bash
   make start
   ```

   This command builds the Docker image and starts the services defined in `docker-compose.yml`.

## API Documentation

Swagger documentation is available once the application is running, accessible at `/apidocs`.


