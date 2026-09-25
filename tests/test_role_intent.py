
"""Live Gemini intent checks. Run manually; consumes API quota."""

import unittest

from app.intent_parser import parse_intent


CASES = [
    (
        "How many appointments did Neha handle?",
        "get_appointments_by_agent",
        "agent",
        "Neha",
    ),
    (
        "Show appointments for customer Vikram.",
        "get_appointments_by_customer",
        "customer",
        "Vikram",
    ),
    (
        "Show WhatsApp messages handled by Neha.",
        "get_messages_by_agent",
        "agent",
        "Neha",
    ),
    (
        "Show WhatsApp messages for customer Rahul.",
        "get_messages_by_customer",
        "customer",
        "Rahul",
    ),
]


class RoleIntentTests(unittest.TestCase):

    def test_role_routing(self):
        for question, expected_type, field, value in CASES:
            with self.subTest(question=question):
                result = parse_intent(question)

                self.assertEqual(
                    result["query_type"],
                    expected_type,
                )

                self.assertEqual(
                    result["parameters"][field],
                    value,
                )


if __name__ == "__main__":
    unittest.main()
