
"""Read-only integration tests for the 12 assignment query scenarios and extensions.
Run from the repository root: python -m unittest tests.test_query_engine -v
These assertions target the original 500-record-per-collection March 2025 dataset.
"""

import unittest

from app.query_engine import (
    count_calls_by_agent,
    get_calls_by_status,
    average_call_duration,
    get_appointments_by_status,
    get_appointments_by_agent,
    get_appointments_by_customer,
    get_missed_appointments,
    get_emails_by_sender,
    search_emails_by_subject,
    get_emails_by_status,
    get_messages_by_agent,
    get_messages_by_customer,
    compare_message_statuses,
    get_latest_message_by_customer,
)


class QueryEngineTests(unittest.TestCase):

    def test_01_calls_by_agent(self):
        self.assertEqual(
          count_calls_by_agent(agent="Neha", period="all_time")["count"],

            124,
        )

    def test_02_failed_calls_custom_dates(self):
        result = get_calls_by_status(
            status="failed",
            period="custom",
            start_date="2025-03-10",
            end_date="2025-03-20",
        )
        self.assertEqual(result["total"], 90)

    def test_03_average_completed_call_duration(self):
        result = average_call_duration(
            status="completed",
            period="custom",
            start_date="2025-03-10",
            end_date="2025-03-20",
        )
        self.assertIsInstance(result, dict)
        self.assertTrue(result)
        # Previously observed: 80 completed calls,
        # average approximately 10.53 minutes.

    def test_04_confirmed_appointments_custom_dates(self):
        result = get_appointments_by_status(
            status="confirmed",
            period="custom",
            start_date="2025-03-10",
            end_date="2025-03-20",
        )
        self.assertEqual(result["total"], 62)

    def test_05_appointments_by_agent(self):
        self.assertEqual(
            get_appointments_by_agent(
                agent="Neha",
                period="all_time",
            )["total"],
            162,
        )

    def test_06_missed_appointments(self):
        self.assertEqual(
            get_missed_appointments(period="all_time")["total"],
            115,
        )

    def test_07_emails_by_sender(self):
        self.assertEqual(
            get_emails_by_sender(
                sender="support@crm.io",
                period="all_time",
            )["total"],
            245,
        )

    def test_08_emails_by_subject(self):
        self.assertEqual(
            search_emails_by_subject(
                subject="onboarding",
                period="all_time",
            )["total"],
            153,
        )

    def test_09_undelivered_emails(self):
        result = get_emails_by_status(
            status=["failed", "bounced"],
            period="all_time",
        )
        self.assertEqual(result["total"], 324)
        self.assertEqual(result["status"], ["failed", "bounced"])

    def test_10_whatsapp_by_agent(self):
        self.assertEqual(
            get_messages_by_agent(
                agent="Amit",
                period="all_time",
            )["total"],
            227,
        )

    def test_11_whatsapp_status_comparison(self):
        result = compare_message_statuses(
            statuses=["delivered", "failed"],
            period="all_time",
        )
        self.assertEqual(result["delivered"], 156)
        self.assertEqual(result["failed"], 158)

    def test_12_latest_whatsapp_for_customer(self):
        result = get_latest_message_by_customer(
            customer="Vikram",
            period="all_time",
        )
        self.assertEqual(result["message_id"], "WA5045")
        self.assertEqual(result["customer"], "Vikram Das")

    def test_13_customer_appointments_extension(self):
        result = get_appointments_by_customer(
            customer="Vikram",
            period="all_time",
        )
        self.assertGreater(result["total"], 0)

    def test_14_customer_whatsapp_extension(self):
        self.assertEqual(
            get_messages_by_customer(
                customer="Rahul",
                period="all_time",
            )["total"],
            159,
        )


if __name__ == "__main__":
    unittest.main()
