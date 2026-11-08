# Day 3 – NPTELPicker Data Ingestion

## Objective
Download NPTEL course HTML pages, match course IDs with course metadata, clean the records and save them in JSON format.

## Project Files
- `app/models.py` – Defines the Record dataclass.
- `app/fetch.py` – Downloads course HTML pages using Requests.
- `app/ingest.py` – Reads downloaded HTML files, extracts course IDs, matches them with CSV metadata and creates clean JSON records.
- `data/course_metadata.csv` – Contains course metadata.
- `data/raw/` – Stores downloaded HTML files.
- `data/records.json` – Stores the main 20-course dataset.

## Required Fields
`course_id`, `course_name`, `discipline`, `institute`, `duration_weeks`, `course_url`, `level`

## Commands to Run

```bash
python -m app.fetch
python -m app.ingest
```

## Test Results
- HTML files downloaded: 3
- HTML files processed: 3
- Valid records generated: 3
- JSON fields verified: 7
- Main 20-course dataset restored successfully.

## Implementation Note
The NPTEL HTML pages are JavaScript-rendered. The ingestion script extracts course IDs from the downloaded HTML and obtains the remaining metadata by matching those IDs against the local CSV file. It does not directly extract all course details from HTML.