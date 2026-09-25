
from app.copilot import ask_copilot


def display_result(response):
    if response.get("answer"):
        print("\nCopilot:", response["answer"])
        return

    query_type = response.get("query_type", "")
    result = response.get("result", {})
    parameters = response.get("parameters", {})

    print("\n" + "-" * 55)
    print("COPILOT ANSWER")
    print("-" * 55)

    # Comparison queries return counts by status.
    if query_type == "compare_message_statuses":
        print("WhatsApp message status comparison:")
        for status, count in result.items():
            print(f"  {status.title()}: {count}")
        return

    # Average duration has a different result structure.
    if query_type == "average_call_duration":
        print("Average call duration:")
        for key, value in result.items():
            if key not in {"records", "query_type"}:
                print(f"  {key}: {value}")
        return

    # Latest message returns a single record.
    if query_type == "get_latest_message_by_customer":
        if not result:
            print("No matching message found.")
            return

        print("Latest WhatsApp message:")
        for key, value in result.items():
            print(f"  {key}: {value}")
        return

    # Standard list/count queries.
    total = result.get("total")

    if total is not None:
        print(f"Total matching records: {total}")
    else:
        print("Result:")
        print(result)
        return

    if parameters:
        print("\nApplied filters:")
        for key, value in parameters.items():
            print(f"  {key}: {value}")

    records = result.get("records", [])

    if records:
        print(f"\nShowing first {min(5, len(records))} records:")

        for index, record in enumerate(records[:5], start=1):
            print(f"\n{index}.")
            for key, value in record.items():
                print(f"   {key}: {value}")

        if total > len(records[:5]):
            print(f"\n...and {total - len(records[:5])} more matching records.")

    elif total == 0:
        print("\nNo matching records found.")


def main():
    print("=" * 55)
    print("RUNO CRM AI COPILOT")
    print("Ask about calls, appointments, emails and WhatsApp.")
    print("Type 'exit' to quit.")
    print("=" * 55)

    while True:
        question = input("\nYou: ").strip()

        if question.lower() in {"exit", "quit", "q"}:
            print("Goodbye!")
            break

        if not question:
            continue

        try:
            response = ask_copilot(question)
            display_result(response)

        except Exception as error:
            print(f"\nError: {error}")
            print("Please try again.")


if __name__ == "__main__":
    main()
