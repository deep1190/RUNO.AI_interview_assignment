
"""
RUNO CRM schema and supported query types.

These names describe the existing company-provided data.
They do not create or modify MongoDB collections.
"""

COLLECTIONS = {
    "calls": {
        "mongo_name": "call_logs_samples",
        "date_field": "call_time",
        "fields": [
            "call_id",
            "agent",
            "customer",
            "call_time",
            "duration_minutes",
            "call_status",
        ],
        "status_field": "call_status",
    },

    "appointments": {
        "mongo_name": "appointment_samples",
        "date_field": "appointment_time",
        "fields": [
            "appointment_id",
            "agent",
            "customer",
            "appointment_time",
            "status",
            "notes",
        ],
        "status_field": "status",
    },

    "emails": {
        "mongo_name": "emails_sample",
        "date_field": "timestamp",
        "fields": [
            "email_id",
            "sender",
            "receiver",
            "subject",
            "timestamp",
            "status",
        ],
        "status_field": "status",
    },

    "whatsapp": {
        "mongo_name": "whatsapp_sample",
        "date_field": "timestamp",
        "fields": [
            "message_id",
            "agent",
            "customer",
            "timestamp",
            "message",
            "status",
        ],
        "status_field": "status",
    },
}


QUERY_TYPES = {
    "count_calls_by_agent",
    "get_calls_by_status",
    "average_call_duration",

    "get_appointments_by_status",
    "get_appointments_by_agent",
    "get_appointments_by_customer",
    "get_missed_appointments",

    "get_emails_by_sender",
    "search_emails_by_subject",
    "get_emails_by_status",

    "get_messages_by_agent",
    "get_messages_by_customer",
    "compare_message_statuses",
    "get_latest_message_by_customer",
}
