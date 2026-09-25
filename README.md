
# RUNO CRM AI Copilot

A natural-language AI copilot for querying CRM records across
calls, appointments, email conversations, and WhatsApp Business
conversations.

The application uses Google Gemini for intent understanding,
Python for query validation and execution, and MongoDB for
structured CRM data storage.

## Overview

CRM users often need answers to questions such as:

- How many calls did an agent handle?
- Which appointments were missed?
- Which emails failed to reach customers?
- How many WhatsApp messages were delivered or failed?
- What is the latest WhatsApp message for a customer?

Instead of requiring users to write database queries, this
application accepts questions in natural language and returns
matching CRM results.

## Features

- Natural-language question understanding using Google Gemini
- Read-only querying across four MongoDB collections
- Support for the original assignment query scenarios
- Dynamic agent, customer, status, and date parameters
- Relative and custom date filtering
- Separate handling of agent and customer relationships
- FastAPI endpoint with interactive Swagger documentation
- Command-line interface
- Automated database and AI integration tests
- Controlled execution through predefined query functions

## Technology Stack

- Python 3
- Google Gemini API
- MongoDB
- PyMongo
- FastAPI
- Uvicorn
- python-dotenv
- Pydantic

## Dataset

The application uses four MongoDB collections:

| Collection | Purpose | Records |
|---|---|---:|
| call_logs_samples | Call activity | 500 |
| appointment_samples | Appointments | 500 |
| emails_sample | Email conversations | 500 |
| whatsapp_sample | WhatsApp conversations | 500 |

Total: 2,000 CRM records.

The original dataset contains historical records from March 2025.

For meaningful demonstrations using the original dataset, use
`all_time` or specify a custom date range within March 2025.
Questions referring to the actual current day may legitimately
return zero records.

## Architecture

The application follows this workflow:

1. A user submits a question through the CLI or API.
2. Gemini converts the question into a structured intent.
3. The copilot validates the query type and parameters.
4. An approved query-engine function is selected.
5. The query engine applies filters and reads MongoDB.
6. The result is returned as structured data.

Gemini does not directly execute arbitrary MongoDB queries.

See [Architecture](docs/architecture.md) for the detailed diagram.

## Project Structure

```text
app/
    api.py
    cli.py
    copilot.py
    database.py
    date_utils.py
    intent_parser.py
    query_engine.py
    schema.py

tests/
    test_query_engine.py
    test_dynamic_queries.py
    test_dates.py
    test_role_intent.py
    test_copilot.py

docs/
    architecture.md

README.md
requirements.txt
.env.example
.gitignore
```

## Setup

### 1. Clone the repository

```bash
git clone <YOUR_PRIVATE_REPOSITORY_URL>
cd <YOUR_REPOSITORY_DIRECTORY>
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env`.

Set the MongoDB connection URI, database name, and Gemini API key.

Never commit the actual `.env` file.

### 5. Prepare MongoDB

Start MongoDB and ensure the four required collections are
available in the configured database.

The application expects the supplied CRM dataset to be imported
before queries are executed.

### 6. Start the API

```bash
python -m uvicorn app.api:app --reload
```

Open:

http://127.0.0.1:8000/docs

### 7. Run the CLI

```bash
python -m app.cli
```

## API

### Health check

```http
GET /health
```

### Ask a CRM question

```http
POST /ask
Content-Type: application/json
```

Example request:

```json
{
  "question": "Show emails that were not delivered successfully."
}
```

Example result summary:

```json
{
  "query_type": "get_emails_by_status",
  "parameters": {
    "status": ["failed", "bounced"],
    "period": "all_time"
  },
  "result": {
    "total": 324
  }
}
```

The actual API response also includes the original question
and matching CRM records.

## Supported Query Capabilities

### Calls

- Count calls handled by an agent
- Retrieve calls by status
- Calculate average call duration

### Appointments

- Retrieve appointments by status
- Retrieve appointments by agent
- Retrieve appointments by customer
- Retrieve missed appointments

### Emails

- Retrieve emails by sender
- Search email subjects
- Retrieve emails by delivery status

### WhatsApp

- Retrieve messages by agent
- Retrieve messages by customer
- Compare message statuses
- Retrieve the latest message for a customer

## Example Questions

1. How many calls did Neha handle?
2. Show failed calls from March 10 to March 20, 2025.
3. What was the average duration of completed calls?
4. Show confirmed appointments from March 10 to March 20, 2025.
5. Show appointments handled by Neha.
6. Show all missed appointments.
7. Show emails sent by support@crm.io.
8. Find emails with onboarding in the subject.
9. Show emails that were not delivered successfully.
10. Show WhatsApp messages handled by Amit.
11. Compare delivered and failed WhatsApp messages.
12. Show the latest WhatsApp message for customer Vikram.

Additional customer-specific queries are also supported.

## Testing

Run database and date tests:

```bash
python -m unittest tests.test_query_engine tests.test_dynamic_queries tests.test_dates -v
```

These tests do not call Gemini.

Run AI-dependent tests separately:

```bash
python -m unittest tests.test_role_intent tests.test_copilot -v
```

AI-dependent tests require a valid Gemini API key and available
API quota.

The database tests use expected values from the original
500-record-per-collection dataset. Results may differ if the
dataset is modified or replaced.

## Safety and Query Control

The application uses a predefined registry of supported
query handlers.

Parsed parameters are validated before execution, and only
approved function parameters are passed to the query engine.

The application performs read-only CRM retrieval. It does
not provide arbitrary database command execution.

## Limitations

- Requires a running MongoDB instance and imported dataset.
- Gemini requests depend on API availability and quota.
- Supported questions are limited to implemented query capabilities.
- The supplied dataset is historical, so current-relative date
  queries may return no records.
- This project does not modify CRM records or send communications.

## Development Approach

The implementation was developed incrementally through dataset
inspection, individual MongoDB query functions, date filtering,
Gemini intent parsing, copilot routing, CLI integration, API
integration, and automated testing.

The final application code is organized in `app/`, and the
consolidated tests are organized in `tests/`.



## Historical Dataset Demonstration Mode

The supplied CRM dataset contains historical records from March 2025.

To support meaningful demonstrations of relative-date queries
without modifying the original records, the application provides
an optional demonstration reference date.

Configure `.env`:

```dotenv
DEMO_MODE=true
DEMO_REFERENCE_DATE=2025-03-29
```

When enabled, relative periods such as today, yesterday,
this week, and last seven days are calculated using the
configured historical reference date.

Explicit custom dates remain unchanged.

Set `DEMO_MODE=false` to use the actual current date.

The feature changes date interpretation only; it does not
modify MongoDB records.
