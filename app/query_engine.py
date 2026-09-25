
import re

from app.database import (
    call_logs,
    appointments,
    emails,
    whatsapp_messages,
)

from app.date_utils import build_date_filter


# ============================================================
# SHARED HELPERS
# ============================================================

def exact_match(value):
    """Case-insensitive exact match."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError("A non-empty text value is required.")

    return {
        "$regex": f"^{re.escape(value.strip())}$",
        "$options": "i",
    }


def name_match(value):
    """
    Match a complete name or a name prefix.

    Neha        -> Neha Kapoor
    Neha Kapoor -> Neha Kapoor

    Multiple people with the same first name may be included.
    """
    if not isinstance(value, str) or not value.strip():
        raise ValueError("A non-empty name is required.")

    value = value.strip()

    return {
        "$regex": rf"^{re.escape(value)}(?:\s|$)",
        "$options": "i",
    }


def date_filter(
    field,
    period="all_time",
    reference_date=None,
    start_date=None,
    end_date=None,
):
    """Create the date filter using date_utils.py."""
    return build_date_filter(
        field,
        period=period,
        reference_date=reference_date,
        start_date=start_date,
        end_date=end_date,
    )


def fetch_records(collection, query, timestamp_field, limit=50):
    """Return matching record count and a limited list of records."""
    if not isinstance(limit, int) or not 1 <= limit <= 500:
        raise ValueError("limit must be between 1 and 500.")

    total = collection.count_documents(query)

    records = list(
        collection.find(query, {"_id": 0})
        .sort(timestamp_field, -1)
        .limit(limit)
    )

    return {
        "total": total,
        "records": records,
    }


# ============================================================
# CALL LOGS
# ============================================================

def count_calls_by_agent(
    agent,
    period="all_time",
    reference_date=None,
    start_date=None,
    end_date=None,
):
    query = {
        "agent": name_match(agent),
    }

    query.update(
        date_filter(
            "call_time",
            period,
            reference_date,
            start_date,
            end_date,
        )
    )

    return {
        "query_type": "count_calls_by_agent",
        "agent": agent,
        "period": period,
        "count": call_logs.count_documents(query),
    }


def get_calls_by_status(
    status,
    period="all_time",
    agent=None,
    reference_date=None,
    start_date=None,
    end_date=None,
    limit=50,
):
    query = {
        "call_status": exact_match(status),
    }

    if agent:
        query["agent"] = name_match(agent)

    query.update(
        date_filter(
            "call_time",
            period,
            reference_date,
            start_date,
            end_date,
        )
    )

    result = fetch_records(
        call_logs,
        query,
        "call_time",
        limit,
    )

    return {
        "query_type": "get_calls_by_status",
        "status": status,
        "period": period,
        **result,
    }


def average_call_duration(
    status="completed",
    period="all_time",
    agent=None,
    reference_date=None,
    start_date=None,
    end_date=None,
):
    query = {
        "call_status": exact_match(status),
    }

    if agent:
        query["agent"] = name_match(agent)

    query.update(
        date_filter(
            "call_time",
            period,
            reference_date,
            start_date,
            end_date,
        )
    )

    pipeline = [
        {"$match": query},
        {
            "$group": {
                "_id": None,
                "average_minutes": {
                    "$avg": "$duration_minutes",
                },
                "total_calls": {
                    "$sum": 1,
                },
            }
        },
    ]

    results = list(call_logs.aggregate(pipeline))

    if not results:
        return {
            "query_type": "average_call_duration",
            "average_minutes": None,
            "total_calls": 0,
        }

    average = results[0]["average_minutes"]

    return {
        "query_type": "average_call_duration",
        "average_minutes": (
            round(average, 2)
            if average is not None
            else None
        ),
        "total_calls": results[0]["total_calls"],
    }


# ============================================================
# APPOINTMENTS
# ============================================================

def get_appointments_by_status(
    status,
    period="all_time",
    reference_date=None,
    start_date=None,
    end_date=None,
    limit=50,
):
    query = {
        "status": exact_match(status),
    }

    query.update(
        date_filter(
            "appointment_time",
            period,
            reference_date,
            start_date,
            end_date,
        )
    )

    result = fetch_records(
        appointments,
        query,
        "appointment_time",
        limit,
    )

    return {
        "query_type": "get_appointments_by_status",
        "status": status,
        "period": period,
        **result,
    }


def get_appointments_by_agent(
    agent,
    period="all_time",
    reference_date=None,
    start_date=None,
    end_date=None,
    limit=50,
):
    query = {
        "agent": name_match(agent),
    }

    query.update(
        date_filter(
            "appointment_time",
            period,
            reference_date,
            start_date,
            end_date,
        )
    )

    result = fetch_records(
        appointments,
        query,
        "appointment_time",
        limit,
    )

    return {
        "query_type": "get_appointments_by_agent",
        "agent": agent,
        "period": period,
        **result,
    }


def get_missed_appointments(
    period="all_time",
    reference_date=None,
    start_date=None,
    end_date=None,
    limit=50,
):
    result = get_appointments_by_status(
        status="missed",
        period=period,
        reference_date=reference_date,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
    )

    result["query_type"] = "get_missed_appointments"

    return result


# ============================================================
# EMAILS
# ============================================================

def get_emails_by_sender(
    sender,
    period="all_time",
    reference_date=None,
    start_date=None,
    end_date=None,
    limit=50,
):
    query = {
        "sender": exact_match(sender),
    }

    query.update(
        date_filter(
            "timestamp",
            period,
            reference_date,
            start_date,
            end_date,
        )
    )

    result = fetch_records(
        emails,
        query,
        "timestamp",
        limit,
    )

    return {
        "query_type": "get_emails_by_sender",
        "sender": sender,
        "period": period,
        **result,
    }


def search_emails_by_subject(
    subject,
    period="all_time",
    reference_date=None,
    start_date=None,
    end_date=None,
    limit=50,
):
    if not isinstance(subject, str) or not subject.strip():
        raise ValueError("A non-empty subject is required.")

    query = {
        "subject": {
            "$regex": re.escape(subject.strip()),
            "$options": "i",
        }
    }

    query.update(
        date_filter(
            "timestamp",
            period,
            reference_date,
            start_date,
            end_date,
        )
    )

    result = fetch_records(
        emails,
        query,
        "timestamp",
        limit,
    )

    return {
        "query_type": "search_emails_by_subject",
        "subject": subject,
        "period": period,
        **result,
    }


def get_emails_by_status(
    status,
    period="all_time",
    reference_date=None,
    start_date=None,
    end_date=None,
    limit=50,
):
    """
    Supports one status or multiple statuses.

    Example:
    status="bounced"
    status=["bounced", "failed"]
    """
    if isinstance(status, str):
        status_values = [status]
    elif isinstance(status, list) and status:
        status_values = status
    else:
        raise ValueError("Provide a status or non-empty status list.")

    query = {
        "status": {
            "$in": [
                re.compile(
                    f"^{re.escape(value.strip())}$",
                    re.IGNORECASE,
                )
                for value in status_values
            ]
        }
    }

    query.update(
        date_filter(
            "timestamp",
            period,
            reference_date,
            start_date,
            end_date,
        )
    )

    result = fetch_records(
        emails,
        query,
        "timestamp",
        limit,
    )

    return {
        "query_type": "get_emails_by_status",
        "status": status,
        "period": period,
        **result,
    }


# ============================================================
# WHATSAPP
# ============================================================

def get_messages_by_agent(
    agent,
    period="all_time",
    reference_date=None,
    start_date=None,
    end_date=None,
    limit=50,
):
    query = {
        "agent": name_match(agent),
    }

    query.update(
        date_filter(
            "timestamp",
            period,
            reference_date,
            start_date,
            end_date,
        )
    )

    result = fetch_records(
        whatsapp_messages,
        query,
        "timestamp",
        limit,
    )

    return {
        "query_type": "get_messages_by_agent",
        "agent": agent,
        "period": period,
        **result,
    }


def compare_message_statuses(
    statuses=None,
    period="all_time",
    reference_date=None,
    start_date=None,
    end_date=None,
):
    if statuses is None:
        statuses = ["delivered", "failed"]

    if not isinstance(statuses, list) or not statuses:
        raise ValueError("statuses must be a non-empty list.")

    base_query = date_filter(
        "timestamp",
        period,
        reference_date,
        start_date,
        end_date,
    )

    result = {}

    for status in statuses:
        query = dict(base_query)
        query["status"] = exact_match(status)

        result[status] = whatsapp_messages.count_documents(query)

    return result


def get_latest_message_by_customer(
    customer,
    period="all_time",
    reference_date=None,
    start_date=None,
    end_date=None,
):
    query = {
        "customer": name_match(customer),
    }

    query.update(
        date_filter(
            "timestamp",
            period,
            reference_date,
            start_date,
            end_date,
        )
    )

    return whatsapp_messages.find_one(
        query,
        {"_id": 0},
        sort=[("timestamp", -1)],
    )

def get_appointments_by_customer(
    customer,
    period="all_time",
    reference_date=None,
    start_date=None,
    end_date=None,
    limit=50,
):
    query = {"customer": name_match(customer)}

    query.update(
        date_filter(
            "appointment_time",
            period,
            reference_date,
            start_date,
            end_date,
        )
    )

    result = fetch_records(
        appointments,
        query,
        "appointment_time",
        limit,
    )

    return {
        "query_type": "get_appointments_by_customer",
        "customer": customer,
        "period": period,
        **result,
    }


def get_messages_by_customer(
    customer,
    period="all_time",
    reference_date=None,
    start_date=None,
    end_date=None,
    limit=50,
):
    query = {"customer": name_match(customer)}

    query.update(
        date_filter(
            "timestamp",
            period,
            reference_date,
            start_date,
            end_date,
        )
    )

    result = fetch_records(
        whatsapp_messages,
        query,
        "timestamp",
        limit,
    )

    return {
        "query_type": "get_messages_by_customer",
        "customer": customer,
        "period": period,
        **result,
    }
