
"""Live end-to-end Gemini -> handler -> MongoDB tests. Run manually; uses API quota."""

import unittest

from app.copilot import ask_copilot


CASES = [
    ("Show all missed appointments.", "get_missed_appointments", 115),
    ("Show emails sent by support@crm.io.", "get_emails_by_sender", 245),
    ("Find emails with onboarding in the subject.", "search_emails_by_subject", 153),
    ("Show emails that were not delivered successfully.", "get_emails_by_status", 324),
    ("Show WhatsApp messages handled by Amit.", "get_messages_by_agent", 227),
    (
        "Show confirmed appointments from March 10 to March 20, 2025.",
        "get_appointments_by_status",
        62,
    ),
]


class CopilotTests(unittest.TestCase):

    def test_list_queries(self):
        for question, query_type, total in CASES:
            with self.subTest(question=question):
                response = ask_copilot(question)

                self.assertEqual(
                    response.get("query_type"),
                    query_type,
                    response,
                )

                self.assertEqual(
                    response.get("result", {}).get("total"),
                    total,
                    response,
                )

                if "not delivered" in question:
                    self.assertEqual(
                        set(response["parameters"]["status"]),
                        {"failed", "bounced"},
                    )

    def test_comparison(self):
        response = ask_copilot(
            "Compare delivered and failed WhatsApp messages."
        )

        self.assertEqual(
            response.get("query_type"),
            "compare_message_statuses",
        )

        self.assertEqual(response["result"]["delivered"], 156)
        self.assertEqual(response["result"]["failed"], 158)

    def test_latest_message(self):
        response = ask_copilot(
            "Show the latest WhatsApp message for customer Vikram."
        )

        self.assertEqual(
            response.get("query_type"),
            "get_latest_message_by_customer",
        )

        self.assertEqual(
            response["result"]["message_id"],
            "WA5045",
        )


if __name__ == "__main__":
    unittest.main()
