# my.ket.horse AI Coding Agent Instructions

This document provides guidance for AI coding agents to effectively contribute to the my.ket.horse project.

## Project Overview

my.ket.horse is a free, open-source URL shortening service built with Flask and MongoDB. It provides features like custom slugs, password protection, and URL statistics.

## Architecture

The application follows a standard Flask structure, with functionalities organized into blueprints.

- **`main.py`**: The main entry point of the application. It initializes the Flask app, registers blueprints, and handles errors.
- **`blueprints/`**: This directory contains the core logic of the application, with each file representing a blueprint for a specific feature (e.g., `url_shortener.py`, `stats.py`).
- **`templates/`**: Contains the HTML templates for the web interface.
- **`static/`**: Contains static assets like CSS, JavaScript, and images.
- **`utils/`**: Contains utility functions, such as database operations (`mongo_utils.py`).
- **`tests/`**: Contains the tests for the application.

## Development Workflow

### Running the Application

To run the application locally, you can use Docker or run it directly.

**Docker (Recommended):**

1.  Clone the repository.
2.  Rename `.env.example` to `.env`.
3.  Run `docker-compose up`.

**Directly:**

1.  Install the dependencies from `requirements.txt`.
2.  Run `python main.py`.

### Running Tests

The project uses `pytest` for testing. The tests are located in the `tests/` directory and use `mongomock` to simulate the MongoDB database, so no running database is required.

To run the tests, execute the following command:

```bash
pytest
```

## Key Conventions and Patterns

- **Blueprints**: The application is modularized using Flask Blueprints. When adding new features, create a new blueprint in the `blueprints/` directory and register it in `main.py`.
- **MongoDB**: The application uses MongoDB as its database. Database-related functions are located in `utils/mongo_utils.py`.
- **Error Handling**: The application has custom error handlers for 404 and 429 errors in `main.py`.
- **Rate Limiting**: The application uses `Flask-Limiter` for rate limiting. The configuration is in `blueprints/limiter.py`.

## External Dependencies

- **Flask**: The web framework used for the application.
- **PyMongo**: The Python driver for MongoDB.
- **geoip2**: Used for geolocation of IP addresses.
- **hCaptcha**: Used for captcha verification.

## Important Files

- **`main.py`**: The main application file.
- **`blueprints/url_shortener.py`**: The core logic for URL shortening.
- **`blueprints/stats.py`**: The logic for URL statistics.
- **`utils/mongo_utils.py`**: The utility functions for interacting with MongoDB.
- **`tests/`**: The directory containing all the tests.
