import json
import requests
from pathlib import Path

DATA_FILE = Path("data/records.json")
RAW_FOLDER = Path("data/raw")


def fetch_documents():
    RAW_FOLDER.mkdir(parents=True, exist_ok=True)

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        records = json.load(file)

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

        except requests.exceptions.RequestException as error:
            print(f"Failed to download {course_id}: {error}")

    print(f"\nSuccessfully downloaded: {downloaded} documents")


if __name__ == "__main__":
    fetch_documents()