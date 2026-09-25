
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

TIMEZONE = ZoneInfo("Asia/Kolkata")


def current_time(reference_date=None):
    if reference_date is not None:
        return reference_date

    return datetime.now(TIMEZONE)


def get_date_range(
    period="all_time",
    reference_date=None,
    start_date=None,
    end_date=None,
):
    now = current_time(reference_date)

    today = now.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )

    if period == "all_time":
        return None, None

    elif period == "today":
        start = today
        end = start + timedelta(days=1)

    elif period == "yesterday":
        end = today
        start = end - timedelta(days=1)

    elif period == "this_week":
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=7)

    elif period == "last_week":
        end = today - timedelta(days=today.weekday())
        start = end - timedelta(days=7)

    elif period == "this_month":
        start = today.replace(day=1)

        if start.month == 12:
            end = start.replace(year=start.year + 1, month=1)
        else:
            end = start.replace(month=start.month + 1)

    elif period == "last_month":
        end = today.replace(day=1)
        start = (end - timedelta(days=1)).replace(day=1)

    elif period.startswith("last_") and period.endswith("_days"):
        number = int(period.split("_")[1])

        if number < 1 or number > 3650:
            raise ValueError("Invalid number of days.")

        start = now - timedelta(days=number)
        end = now

    elif period == "custom":
        if not start_date or not end_date:
            raise ValueError(
                "Custom date range requires start_date and end_date."
            )

        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        if end < start:
            raise ValueError(
                "End date cannot be before start date."
            )

        end += timedelta(days=1)

    else:
        raise ValueError(f"Unsupported period: {period}")

    return (
        start.strftime("%Y-%m-%dT%H:%M:%S"),
        end.strftime("%Y-%m-%dT%H:%M:%S"),
    )


def build_date_filter(
    field,
    period="all_time",
    reference_date=None,
    start_date=None,
    end_date=None,
):
    start, end = get_date_range(
        period=period,
        reference_date=reference_date,
        start_date=start_date,
        end_date=end_date,
    )

    if start is None:
        return {}

    return {
        field: {
            "$gte": start,
            "$lt": end,
        }
    }
