
import inspect

from app.demo_config import get_demo_metadata

from app.intent_parser import parse_intent

from app.query_engine import (
    count_calls_by_agent,
    get_calls_by_status,
    get_appointments_by_customer,
    get_messages_by_customer,
    average_call_duration,
    get_appointments_by_status,
    get_appointments_by_agent,
    get_missed_appointments,
    get_emails_by_sender,
    search_emails_by_subject,
    get_emails_by_status,
    get_messages_by_agent,
    compare_message_statuses,
    get_latest_message_by_customer,
)


QUERY_HANDLERS = {
    "count_calls_by_agent": count_calls_by_agent,
    "get_calls_by_status": get_calls_by_status,
    "get_appointments_by_customer": get_appointments_by_customer,
    "get_messages_by_customer": get_messages_by_customer,
    "average_call_duration": average_call_duration,
    "get_appointments_by_status": get_appointments_by_status,
    "get_appointments_by_agent": get_appointments_by_agent,
    "get_missed_appointments": get_missed_appointments,
    "get_emails_by_sender": get_emails_by_sender,
    "search_emails_by_subject": search_emails_by_subject,
    "get_emails_by_status": get_emails_by_status,
    "get_messages_by_agent": get_messages_by_agent,
    "compare_message_statuses": compare_message_statuses,
    "get_latest_message_by_customer": get_latest_message_by_customer,
}


QUERY_ALIASES = {
    "get_emails_by_subject": "search_emails_by_subject",
}


def ask_copilot(question):
    if not isinstance(question, str) or not question.strip():
        return {
            "question": question,
            "answer": "Please enter a question.",
        }

    try:
        intent = parse_intent(question)

        # Normalize broad undelivered-email requests.
        # In this dataset, undelivered means failed OR bounced.
        question_lower = question.lower()

        undelivered_phrases = (
            "undelivered",
            "not delivered",
            "weren't delivered",
            "were not delivered",
            "delivery unsuccessful",
            "delivery failed",
        )

        if (
            intent.get("query_type") == "get_emails_by_status"
            and any(
                phrase in question_lower
                for phrase in undelivered_phrases
            )
            and "only failed" not in question_lower
            and "only bounced" not in question_lower
        ):
            intent.setdefault("parameters", {})["status"] = [
                "failed",
                "bounced",
            ]

        # The following logic runs for ALL query types.
        query_type = intent.get("query_type", "unsupported")
        parameters = intent.get("parameters", {})

        if query_type == "unsupported":
            return {
                "question": question,
                "answer": "This question is not supported yet.",
            }

        query_type = QUERY_ALIASES.get(
            query_type,
            query_type,
        )

        handler = QUERY_HANDLERS.get(query_type)

        if handler is None:
            return {
                "question": question,
                "answer": "This query type is not supported yet.",
                "query_type": query_type,
            }

        if not isinstance(parameters, dict):
            raise ValueError(
                "Invalid parameters returned by Gemini."
            )

        # Only pass parameters accepted by the selected function.
        signature = inspect.signature(handler)
        allowed_parameters = set(signature.parameters)

        filtered_parameters = {
            key: value
            for key, value in parameters.items()
            if key in allowed_parameters
        }

        # Check whether required parameters are missing.
        for name, parameter in signature.parameters.items():
            if (
                parameter.default is inspect.Parameter.empty
                and name not in filtered_parameters
            ):
                return {
                    "question": question,
                    "query_type": query_type,
                    "answer": (
                        f"Please specify the required parameter: {name}."
                    ),
                }

        result = handler(**filtered_parameters)

        return {
            "question": question,
            "query_type": query_type,
            "parameters": filtered_parameters,
            "result": result,
            "date_context": get_demo_metadata(),
        }

    except (TypeError, ValueError) as error:
        return {
            "question": question,
            "answer": f"Unable to process the question: {error}",
        }
