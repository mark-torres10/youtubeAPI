# Project Technical Overview

## Overview

This project is a comprehensive podcast data management system that efficiently synchronizes podcast information from YouTube and Spotify, maps them together into a consolidated dataset, and exposes this data through a REST API. The data is then presented to users via a React frontend. It employs a range of modern technologies, including React, Python, Django, SQLite, Redis, Airflow, Docker, and Github Actions.

## Project Objectives

The primary objectives of this project are as follows:

1. **Data Synchronization**: To synchronize podcast data from YouTube and Spotify, ensuring that the most up-to-date information is available.

2. **Data Mapping**: To consolidate podcast information from various integrations, mapping relevant data together to create a unified dataset.

3. **API Creation**: To create a RESTful API with two GET endpoints:
   - `/api/channels`: Retrieves a list of podcast channels.
   - `/api/episodes`: Retrieves a list of podcast episodes.

4. **User-Friendly Frontend**: To provide users with an intuitive React-based frontend for easy access to the data.

## Technology Stack

The project leverages the following technologies:

### Frontend
- **React**: The frontend is built using React, a powerful JavaScript library for building user interfaces. React's component-based architecture makes it highly modular and easy to maintain.

### Backend
- **Python**: Python is the backend language of choice due to its versatility and a rich ecosystem of libraries for data manipulation and web development.
- **Django**: Django, a high-level Python web framework, powers the backend. It offers features such as ORM for database management, URL routing, and authentication.
- **SQLite**: SQLite serves as the project's lightweight relational database system for data storage.
- **Redis**: Redis is used for caching to enhance API performance.

### Orchestration
- **Airflow**: Apache Airflow is employed to orchestrate and schedule data synchronization and transformation tasks. It ensures data pipelines run efficiently and on schedule.

### Deployment
- **Docker**: Docker containers are used for creating a portable and consistent deployment environment. It encapsulates the application and its dependencies, ensuring seamless deployment across different platforms.

### CI/CD
- **Github Actions**: Github Actions automates the CI/CD pipeline, enabling continuous integration and deployment with ease. It ensures that code changes are tested, built, and deployed automatically.

## Architecture Overview

The project follows a microservices architecture, with separate components handling data synchronization, mapping, API creation, and frontend presentation. Here's a high-level overview of the architecture:

1. **Data Synchronization**:
   - Integration-specific scripts sync data from YouTube and Spotify at regular intervals.
   - Airflow orchestrates and schedules these sync tasks.

2. **Data Mapping**:
   - Consolidation scripts map and merge data from different integrations into a single dataset.
   - Data is stored in an SQLite database.

3. **Backend/API**:
   - Django-powered backend exposes two API endpoints (`/api/channels` and `/api/episodes`) to serve podcast channel and episode data.
   - Redis is used for caching to improve API response times.

4. **Frontend**:
   - React frontend provides a user-friendly interface to interact with the data.
   - Users can request and view podcast channels and episodes in a tabular format.

## Project Workflow

1. **Data Synchronization**:
   - Airflow triggers data sync tasks for YouTube and Spotify at specified intervals.
   - Sync scripts fetch and update podcast data.

2. **Data Mapping**:
   - Mapping scripts consolidate data from different integrations into a unified dataset.
   - Data is stored in the SQLite database.

3. **API Interaction**:
   - Users interact with the data through the RESTful API.
   - API requests are processed by the Django backend.
   - Redis caching enhances API response times.

4. **Frontend Display**:
   - React frontend communicates with the API to display podcast channel and episode data.
   - Users can view this data as tables.
