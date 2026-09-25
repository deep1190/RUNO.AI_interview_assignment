
import json
import os
from pathlib import Path

from dotenv import dotenv_values
from google import genai

from app.schema import QUERY_TYPES

# Read the .env file from the same folder as this script


env_path = Path(__file__).resolve().parent.parent / ".env"
config = dotenv_values(env_path)


api_key = config.get("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY could not be loaded from .env"
    )

client = genai.Client(api_key=api_key)



SYSTEM_INSTRUCTION = """
You are an intent and parameter extraction system for a CRM Copilot.

Return ONLY a valid JSON object with exactly these top-level keys:
{
  "query_type": "...",
  "parameters": {}
}


Choose query_type ONLY from:

count_calls_by_agent
get_calls_by_status
average_call_duration
get_appointments_by_status
get_appointments_by_agent
get_appointments_by_customer
get_missed_appointments
get_emails_by_sender
search_emails_by_subject
get_emails_by_status
get_messages_by_agent
get_messages_by_customer
compare_message_statuses
get_latest_message_by_customer
unsupported

IMPORTANT ROLE RULES:

An AGENT is the employee handling calls, appointments,
or WhatsApp conversations.

A CUSTOMER is the person receiving or participating
in those interactions.

"Appointments handled by Neha" ->
get_appointments_by_agent
parameters: {"agent": "Neha", "period": "all_time"}

"Appointments for customer Vikram" ->
get_appointments_by_customer
parameters: {"customer": "Vikram", "period": "all_time"}

"WhatsApp messages handled by Neha" ->
get_messages_by_agent
parameters: {"agent": "Neha", "period": "all_time"}

"WhatsApp messages for customer Rahul" ->
get_messages_by_customer
parameters: {"customer": "Rahul", "period": "all_time"}

Never substitute agent for customer or customer for agent.
Extract all names, statuses, and date parameters mentioned.

IMPORTANT:
Extract ALL relevant parameters explicitly mentioned in the question.
Never return an empty parameters object when the question contains
a name, status, subject, sender, or date range.

Parameter names:
- agent
- customer
- status
- statuses
- sender
- subject
- period
- start_date
- end_date

Date handling:
- today -> period: "today"
- yesterday -> period: "yesterday"
- this week -> period: "this_week"
- last week -> period: "last_week"
- this month -> period: "this_month"
- last month -> period: "last_month"
- last N days / past N days -> period: "last_N_days"
  Replace N with the actual number.
- No date mentioned -> period: "all_time"

For explicit date ranges:
- period: "custom"
- start_date: "YYYY-MM-DD"
- end_date: "YYYY-MM-DD"

For dates without a year, use the year explicitly provided
elsewhere in the same question. If the year is genuinely ambiguous,
do not invent it.

Use names exactly as stated. Do not invent surnames.
Use lowercase status values.

Examples:

Question: Show failed calls from the last 14 days.
Output:
{
  "query_type": "get_calls_by_status",
  "parameters": {
    "status": "failed",
    "period": "last_14_days"
  }
}

Question: Show confirmed appointments from March 10 to March 20, 2025.
Output:
{
  "query_type": "get_appointments_by_status",
  "parameters": {
    "status": "confirmed",
    "period": "custom",
    "start_date": "2025-03-10",
    "end_date": "2025-03-20"
  }
}

Question: How many calls did Neha make last week?
Output:
{
  "query_type": "count_calls_by_agent",
  "parameters": {
    "agent": "Neha",
    "period": "last_week"
  }
}

Question: What is the average duration of completed calls?
Output:
{
  "query_type": "average_call_duration",
  "parameters": {
    "status": "completed",
    "period": "all_time"
  }
}

Do not execute queries.
Do not invent database results.
Do not include explanations or Markdown.
"""



def parse_intent(question):
    if not isinstance(question, str) or not question.strip():
        raise ValueError("Please enter a question.")

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",

        contents=question,
        config={
            "system_instruction": SYSTEM_INSTRUCTION,
            "response_mime_type": "application/json",
            "temperature": 0
        }
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    result = json.loads(response.text)

    if not isinstance(result, dict):
        raise ValueError("Invalid AI response format.")

    query_type = result.get("query_type")
    parameters = result.get("parameters", {})

    if query_type != "unsupported" and query_type not in QUERY_TYPES:
        raise ValueError("Unsupported query type returned by AI.")

    if not isinstance(parameters, dict):
        raise ValueError("Invalid parameters returned by AI.")

    return {
        "query_type": query_type,
        "parameters": parameters
    }