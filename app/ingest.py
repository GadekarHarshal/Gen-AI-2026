
import csv
import json
import re
from pathlib import Path
from dataclasses import asdict
from app.models import Record

CSV_FILE = Path("data/course_metadata.csv")
RAW_FOLDER = Path("data/raw")
OUTPUT_FILE = Path("data/records.json")


def clean_records():
    records = []

    # Read course information from CSV
    with open(CSV_FILE, "r", encoding="utf-8") as file:
        csv_records = list(csv.DictReader(file))

    # Match each downloaded HTML page with the CSV
    for html_file in RAW_FOLDER.glob("*.html"):
        try:
            html = html_file.read_text(encoding="utf-8")

            # Extract course ID from HTML content
            match = re.search(r"noc26_[a-z0-9]+", html)

            if not match:
                raise ValueError("Course ID not found in HTML")

            course_id = match.group(0)

            # Find matching course in CSV
            course = None

            for row in csv_records:
                if row["course_id"] == course_id:
                    course = row
                    break

            if course is None:
                raise ValueError("Course not found in CSV")

            record = Record(
                course_id=course["course_id"],
                course_name=course["course_name"],
                discipline=course["discipline"],
                institute=course["institute"],
                duration_weeks=course["duration_weeks"],
                course_url=course["course_url"],
                level=course["level"]

            )

            records.append(asdict(record))
            print("Processed:", course_id)

        except (OSError, KeyError, ValueError) as error:
            print(f"Skipping {html_file.name}: {error}")

    # Save extracted records
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(records, file, indent=4)

    print("\nHTML files processed:", len(list(RAW_FOLDER.glob("*.html"))))
    print("Valid records saved:", len(records))
    print("Saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    clean_records()
