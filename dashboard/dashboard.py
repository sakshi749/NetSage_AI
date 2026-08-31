import csv
import json
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CASES = BASE / "data" / "cases.csv"
AI_RESULTS = BASE / "data" / "ai_results.json"
REVIEWS = BASE / "data" / "reviewed_cases.csv"


def load_csv(path):
    with path.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    cases = load_csv(CASES)

    with AI_RESULTS.open("r", encoding="utf-8") as f:
        ai_results = json.load(f)

    concepts = Counter(c["concept_tag"] for c in cases)
    severities = Counter(c["severity"] for c in cases)
    statuses = Counter(r["diagnosis_status"] for r in ai_results)

    print("=" * 65)
    print("             NetSage AI - Project Dashboard")
    print("=" * 65)

    print(f"\nTotal Benchmark Cases: {len(cases)}")

    print("\nISSUE-TYPE DISTRIBUTION")
    print("-" * 40)

    for concept, count in sorted(concepts.items()):
        print(f"{concept:<15} : {count}")

    print("\nSEVERITY DISTRIBUTION")
    print("-" * 40)

    for severity, count in sorted(severities.items()):
        print(f"{severity:<15} : {count}")

    print("\nDIAGNOSTIC STATUS")
    print("-" * 40)

    for status, count in statuses.items():
        print(f"{status:<22} : {count}")

    if REVIEWS.exists():
        reviews = load_csv(REVIEWS)
        review_status = Counter(
            r["human_status"] for r in reviews
        )

        print("\nHUMAN REVIEW")
        print("-" * 40)

        for status, count in review_status.items():
            print(f"{status:<15} : {count}")

        accepted = review_status.get("Accepted", 0)

        agreement = (
            accepted / len(reviews) * 100
            if reviews else 0
        )

        print(
            f"\nAI-Human Agreement Rate: "
            f"{agreement:.2f}%"
        )

    else:
        print("\nHUMAN REVIEW")
        print("-" * 40)
        print("Review dataset not generated yet.")

    print("\nSAFETY CONTROL")
    print("-" * 40)
    print("Human approval required before remediation: YES")

    print("\n" + "=" * 65)
    print("Dashboard generation completed.")
    print("=" * 65)


if __name__ == "__main__":
    main()