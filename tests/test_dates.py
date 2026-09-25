
"""Date-filter smoke tests using a historical reference; no database writes."""

import unittest
from datetime import datetime

from app.date_utils import get_date_range, build_date_filter


REFERENCE = datetime(2025, 3, 28, 12, 0)


class DateTests(unittest.TestCase):

    def test_supported_relative_periods(self):
        for period in (
            "today",
            "yesterday",
            "this_week",
            "last_week",
            "last_3_days",
            "last_7_days",
            "last_14_days",
            "this_month",
            "last_month",
        ):
            with self.subTest(period=period):
                self.assertIsNotNone(
                    get_date_range(period, reference_date=REFERENCE)
                )

    def test_custom_range(self):
        self.assertIsNotNone(
            get_date_range(
                period="custom",
                start_date="2025-03-01",
                end_date="2025-03-15",
            )
        )

    def test_date_filter_includes_bounds(self):
        result = build_date_filter(
            "timestamp",
            "custom",
            start_date="2025-03-10",
            end_date="2025-03-20",
        )

        self.assertIn("timestamp", result)
        self.assertEqual(result["timestamp"]["$gte"][:10], "2025-03-10")
        self.assertEqual(result["timestamp"]["$lt"][:10], "2025-03-21")


if __name__ == "__main__":
    unittest.main()
