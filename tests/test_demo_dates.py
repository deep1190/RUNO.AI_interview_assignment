
import unittest
from datetime import datetime
from unittest.mock import patch

from app.date_utils import get_date_range, current_time


class TestDemoDates(unittest.TestCase):

    @patch("app.demo_config.is_demo_mode", return_value=True)
    @patch("app.demo_config.get_reference_date")
    def test_demo_reference_date(self, mock_date, mock_mode):
        from datetime import date

        mock_date.return_value = date(2025, 3, 29)

        result = current_time()

        self.assertEqual(result.year, 2025)
        self.assertEqual(result.month, 3)
        self.assertEqual(result.day, 29)

    @patch("app.demo_config.is_demo_mode", return_value=True)
    @patch("app.demo_config.get_reference_date")
    def test_today_uses_demo_date(self, mock_date, mock_mode):
        from datetime import date

        mock_date.return_value = date(2025, 3, 29)

        start, end = get_date_range("today")

        self.assertEqual(start, "2025-03-29T00:00:00")
        self.assertEqual(end, "2025-03-30T00:00:00")

    @patch("app.demo_config.is_demo_mode", return_value=True)
    @patch("app.demo_config.get_reference_date")
    def test_last_seven_days_uses_demo_date(
        self, mock_date, mock_mode
    ):
        from datetime import date

        mock_date.return_value = date(2025, 3, 29)

        start, end = get_date_range("last_7_days")

        self.assertEqual(start, "2025-03-22T12:00:00")
        self.assertEqual(end, "2025-03-29T12:00:00")

    @patch("app.demo_config.is_demo_mode", return_value=True)
    @patch("app.demo_config.get_reference_date")
    def test_explicit_custom_dates_are_unchanged(
        self, mock_date, mock_mode
    ):
        from datetime import date

        mock_date.return_value = date(2025, 3, 29)

        start, end = get_date_range(
            period="custom",
            start_date="2025-03-10",
            end_date="2025-03-20",
        )

        self.assertEqual(start, "2025-03-10T00:00:00")
        self.assertEqual(end, "2025-03-21T00:00:00")

    def test_explicit_reference_date_takes_priority(self):
        reference = datetime(2025, 3, 15, 10, 30)

        result = current_time(reference)

        self.assertEqual(result, reference)


if __name__ == "__main__":
    unittest.main()
