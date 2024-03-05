<h1 align="center">
  <br>
  <a href="http://peykan.com/"><img src="docs/logo.jpeg" alt="Peykan" width="200"></a>
  <br>
    Peykan
  <br>
</h1>

<h4 align="center">A minimal Weather Application for <a href="http://peykan.com/" target="_blank">Peykan</a> Assginment.</h4>

<p align="center">
  <a href="https://img.shields.io/badge/test-pass-green">
    <img src="https://img.shields.io/badge/test-pass-brightgreen"
         alt="TestBadge">
  </a>
  <a href="https://img.shields.io/badge/python-3.10-blue">
    <img src="https://img.shields.io/badge/python-3.10-blue"
         alt="PythonVersionBadge">
  </a>


</p>

<p align="center">
  <a href="#project-setup">Project Setup</a> •
  <a href="#endpoints">EndPoints</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#libraries">Libraries</a> •
  <a href="#future-improvements">Future Improvements</a>
</p>


## project setup

1- compelete cookiecutter workflow (recommendation: leave project_slug empty) and go inside the project
```
cd peykan
```

2- SetUp venv
```
virtualenv -p python3.10 venv
source venv/bin/activate
```

3- install Dependencies
```
pip install -r requirements_dev.txt
pip install -r requirements.txt
```

4- create your env
```
cp .env.example .env
```

5- Create tables
```
python manage.py migrate
```

6- spin off docker compose
```
docker compose -f docker-compose.dev.yml up -d
```

7- run the project
```
python manage.py runserver
```

8- run the test
```bash
python manage.py test
```

## Endpoints
- `/`: here you can access to swagger ui and view and test all REST API endpoints.
- `/api/users/register` : you can create your acount with a POST request to this endpoint.
- `/api/auth/jwt/login` : you can login to your acount with a POST request to this endpoint.
- `/api/auth/jwt/refresh` : refresh token endpoint that gets a refresh token and give access token.
- `/api/cv/` : 
    - GET  = you can see your cv
    - POST = create a your cv 

## Changelog

- **v1**: <br> March 2024. <br>**Description**: Initial proposal by me.


## Architecture

The Clean Architecture, popularized by [Uncle Bob](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html), emphasizes several foundational principles:

1. **Framework Independence**: The system isn't reliant on external libraries or frameworks.
2. **Testability**: Business rules can be validated without any external elements.
3. **UI Independence**: Switching out the user interface won't affect the underlying system.
4. **Database Independence**: The system's business logic isn't tied to a specific database.
5. **Independence from External Agencies**: The business logic remains agnostic of external integrations.

![clean-arch-01](./docs/clean-arch-01.png)
*source: [yoan-thirion.gitbook.io](https://yoan-thirion.gitbook.io/knowledge-base/software-craftsmanship/code-katas/clean-architecture)

### ✨ Additional Features and Patterns in This Project

This project not only adheres to Uncle Bob's Clean Architecture principles but also incorporates modern adaptations and extended features to meet contemporary development needs:

- **GraphQL vs HTTP**:<br>The `entrypoints` module contains two API interfaces. `graphql` provides for a robust GraphQL API, while `http` focuses on RESTful API routes and controls.
- **RelationalDB vs NoSQL**:<br>The `repositories` module supports both relational and NoSQL databases. `relational_db` manages operations for databases like SQLite, MySQL, and PostgreSQL, whereas `nosql` manages operations for NoSQL databases like MongoDB and CouchDB.

Apart from following Uncle Bob's Clean Architecture, this project also incorporates:

- **Repository Pattern**:<br>An abstraction that simplifies the decoupling of the model layer from data storage, thereby promoting flexibility and maintainability in the codebase. [^1]
- **Unit of Work Pattern**:<br>This pattern ensures that all operations within a single transaction are completed successfully, or none are completed at all. [^2]
- **Dependency Injection Pattern**:<br>Helps in reducing direct dependencies between codes, increasing the testability and flexibility of modules. [^3]
- **Asynchronous SQLalchemy**:<br>By utilizing the asynchronous capabilities of SQLAlchemy 2.0, database operations are optimized for performance and efficiently handle multitasking. [^4]

### 🧱 Project Structure Overview & Clean Architecture Mapping

Based on Uncle Bob's Clean Architecture principles, this project's structure and architecture flow diagrams are aligned with these principles.

#### Directory Structure

Here's a glimpse of the project's high-level structure, highlighting primary directories and key files:

```ini
./
├── ...
├── src/
│   ├── di/                   - Dependency injection configurations for managing dependencies.
│   │   ├── dependency_injection.py
│   │   └── unit_of_work.py
│   │
│   ├── entrypoints/          - External interfaces like HTTP & GraphQL endpoints.
│   │   ├── graphql/          - GraphQL components for a flexible API.
│   │   └── http/             - RESTful API routes and controllers.
│   │                           ('Frameworks and Drivers' and part of 'Interface Adapters' in Clean Architecture)
│   │
│   ├── usecases/             - Contains application-specific business rules and implementations.
│   │                           ('Use Cases' in Clean Architecture)
│   │
│   ├── repositories/         - Data interaction layer, converting domain data to/from database format.
│   │   ├── nosql/            - Operations for NoSQL databases (e.g., MongoDB, CouchDB).
│   │   └── relational_db/    - Operations for relational databases (e.g., SQLite, MySQL, PostgreSQL).
│   │                           ('Interface Adapters' in Clean Architecture)
│   │
│   ├── models/               - Domain entities representing the business data.
│   │                           ('Entities' in Clean Architecture)
│   │
│   ├── common/               - Shared code and utilities.
│   ├── settings/
│   │   └── db/               - Database configurations.
│   │                           ('Frameworks and Drivers' in Clean Architecture)
│   │
│   └── main.py               - Main file to launch the application.
│
└── tests/
    ├── api_db_test.bats      - BATs tests for API and database interactions.
    ├── integration/          - Integration tests for testing module interactions.
    └── unit/                 - Unit tests for testing individual components in isolation.
```

#### Clean Architecture Flow Diagram

The Clean Architecture Flow Diagram visualizes the layers of Clean Architecture and how they interact. It consists of two images and an ASCII flow for clarity:

> For a detailed explanation of the ASCII flow, refer to [ascii-flow.md](./docs/ascii-flow.md).

![clean-arch-02](./docs/clean-arch-02.png)
*source: [yoan-thirion.gitbook.io](https://yoan-thirion.gitbook.io/knowledge-base/software-craftsmanship/code-katas/clean-architecture)*

![clean-arch-03](./docs/clean-arch-03.png)
*source: https://stackoverflow.com/a/73788685

