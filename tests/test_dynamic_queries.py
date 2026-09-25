
"""Variation tests: partial names, role distinctions, and inclusive custom dates."""

import unittest

from app.query_engine import (
    count_calls_by_agent,
    get_appointments_by_status,
    get_calls_by_status,
    get_appointments_by_agent,
    get_appointments_by_customer,
    get_messages_by_agent,
    get_messages_by_customer,
)


class DynamicQueryTests(unittest.TestCase):

    def test_partial_agent_name(self):
        self.assertEqual(
         count_calls_by_agent(agent="Neha", period="all_time")["count"],

            124,
        )

    def test_custom_appointment_range(self):
        self.assertEqual(
            get_appointments_by_status(
                status="confirmed",
                period="custom",
                start_date="2025-03-10",
                end_date="2025-03-20",
            )["total"],
            62,
        )

    def test_custom_failed_calls(self):
        self.assertEqual(
            get_calls_by_status(
                status="failed",
                period="custom",
                start_date="2025-03-10",
                end_date="2025-03-20",
            )["total"],
            90,
        )

    def test_agent_and_customer_are_distinct(self):
        self.assertEqual(
            get_appointments_by_agent(
                agent="Neha",
                period="all_time",
            )["total"],
            162,
        )

        self.assertGreater(
            get_appointments_by_customer(
                customer="Vikram",
                period="all_time",
            )["total"],
            0,
        )

        self.assertEqual(
            get_messages_by_agent(
                agent="Neha",
                period="all_time",
            )["total"],
            273,
        )

        self.assertEqual(
            get_messages_by_customer(
                customer="Rahul",
                period="all_time",
            )["total"],
            159,
        )


if __name__ == "__main__":
    unittest.main()
