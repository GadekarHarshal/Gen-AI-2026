import json
from pathlib import Path
from data.sample_records import sample_records

OUTPUT_FILE = Path("data/records.json")


def clean_records():
    cleaned_records = []

    for row in sample_records:
        try:
            record = {
                "course_id": str(row["course_id"]).strip(),
                "course_name": str(row["course_name"]).strip(),
                "discipline": str(row["discipline"]).strip(),
                "institute": str(row["institute"]).strip(),
                "duration_weeks": row["duration_weeks"],
                "course_url": str(row["course_url"]).strip()
            }

            if not all([
                record["course_id"],
                record["course_name"],
                record["discipline"],
                record["institute"],
                record["course_url"]
            ]):
                raise ValueError("Missing required field")

            if not record["duration_weeks"]:
                     raise ValueError("Missing course duration")

            cleaned_records.append(record)

        except (KeyError, TypeError, ValueError) as error:
            print(f"Skipping bad row: {error}")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(cleaned_records, file, indent=4)

    print(f"\nTotal records processed: {len(sample_records)}")
    print(f"Valid records saved: {len(cleaned_records)}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    clean_records()