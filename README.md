# Praxis Experts API

## Overview

The Praxis Experts API allows users to create and manage projects, with each project having a project manager (Praxis) and multiple experts. The experts are AI assistants configured to respond to user messages based on specific use cases.

## Features

- Create and manage projects.
- Assign experts to projects.
- Assign a project manager (Praxis) to each project.
- Poll for expert run completion.
- Retrieve project details.

## Setup

### Prerequisites

- Python 3.12 or higher
- Virtual environment (recommended)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/calvinmagezi/praxis-experts-api.git
   cd praxis-experts-api
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scriptsctivate`
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a `.env` file in the project root and add your OpenAI API key:

   ```env
   OPENAI_API_KEY=your_openai_api_key
   PRAXIS_ASSISTANT_ID=your_praxis_assistant_id
   ```

### Running the Application

1. **Start the Flask application:**

   ```bash
   flask run
   ```

   The application will be available at `http://127.0.0.1:5000`.

## API Endpoints

### Create a Project

- **URL:** `/projects`
- **Method:** `POST`
- **Request Body:**

  ```json
  {
    "project_name": "Example Project",
    "description": "Detailed description of the project."
  }
  ```

- **Response:**

  ```json
  {
    "project_id": 1,
    "experts": [],
    "manager": null
  }
  ```

### Create an Expert for a Project

- **URL:** `/projects/:project_id/experts`
- **Method:** `POST`
- **Request Body:**

  ```json
  {
    "use_case": "Detailed use case for the expert."
  }
  ```

- **Response:**

  ```json
  {
    "expert_id": "assistant_id",
    "messages": [
      {
        "role": "assistant",
        "content": "Response from the assistant."
      }
    ]
  }
  ```

### Assign Praxis as Project Manager

- **URL:** `/projects/:project_id/assign_praxis`
- **Method:** `POST`
- **Response:**

  ```json
  {
    "manager_id": "praxis_assistant_id"
  }
  ```

### List Projects

- **URL:** `/projects`
- **Method:** `GET`
- **Response:**

  ```json
  {
    "1": {
      "project_name": "Example Project",
      "description": "Detailed description of the project.",
      "experts": ["assistant_id"],
      "manager": "praxis_assistant_id"
    }
  }
  ```

### Get Project Details

- **URL:** `/projects/:project_id`
- **Method:** `GET`
- **Response:**

  ```json
  {
    "project_name": "Example Project",
    "description": "Detailed description of the project.",
    "experts": ["assistant_id"],
    "manager": "praxis_assistant_id"
  }
  ```

### Chat with Praxis Assistant

- **URL:** `/praxis`
- **Method:** `POST`
- **Request Body:**

  ```json
  {
    "message": "Tell me about the role of a Data Scientist."
  }
  ```

- **Response:**

  ```json
  {
    "response": "The role of a Data Scientist involves..."
  }
  ```

## Example Requests

### Create a Project

```bash
curl -X POST http://127.0.0.1:5000/projects -H "Content-Type: application/json" -d '{
    "project_name": "Market Analysis Project",
    "description": "A project to perform detailed market research and analysis."
}'
```

### Create an Expert for a Project

```bash
curl -X POST http://127.0.0.1:5000/projects/1/experts -H "Content-Type: application/json" -d '{
    "use_case": "The Market Research Analyst expert will assist in gathering, analyzing, and interpreting market data to provide actionable insights for business decision-making."
}'
```

### Assign Praxis as Project Manager

```bash
curl -X POST http://127.0.0.1:5000/projects/1/assign_praxis
```

### List Projects

```bash
curl -X GET http://127.0.0.1:5000/projects
```

### Get Project Details

```bash
curl -X GET http://127.0.0.1:5000/projects/1
```

### Chat with Praxis Assistant

```bash
curl -X POST http://127.0.0.1:5000/praxis -H "Content-Type: application/json" -d '{
    "message": "Tell me about the role of a Data Scientist."
}'
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
