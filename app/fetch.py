
import csv
import requests
from pathlib import Path

CSV_FILE = Path("data/course_metadata.csv")
RAW_FOLDER = Path("data/raw")


def fetch_documents():
    RAW_FOLDER.mkdir(parents=True, exist_ok=True)

    with open(CSV_FILE, "r", encoding="utf-8") as file:
        records = list(csv.DictReader(file))

    downloaded = 0

    for course in records[:3]:
        url = course["course_url"]
        course_id = course["course_id"]

        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()

            file_path = RAW_FOLDER / f"{course_id}.html"

            with open(file_path, "w", encoding="utf-8") as file:
                file.write(response.text)

            print(f"Downloaded: {course_id}")
            downloaded += 1

        except (requests.exceptions.RequestException, KeyError) as error:
            print(f"Failed to download {course_id}: {error}")

    print(f"\nSuccessfully downloaded: {downloaded} documents")


if __name__ == "__main__":
    fetch_documents()
