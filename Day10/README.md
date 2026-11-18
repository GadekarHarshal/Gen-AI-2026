
# Day 10 - Streamlit UI and Semester Planner

## Overview

Day 10 adds a Streamlit user interface to NPTELPicker with an AI Chat Assistant and Semester Planner.

## Features

### 1. AI Chat Assistant
- Interactive chat interface.
- Connects to FastAPI backend.
- Uses the LangGraph agent.
- Displays source citations.
- Supports thumbs-up and thumbs-down feedback.
- Saves feedback in `data/feedback.json`.

### 2. Semester Planner
- Select NPTEL courses.
- Enter study start dates.
- Enter exam dates manually.
- Display a semester timeline using Altair.
- Detect exam-date clashes.
- Estimate weekly study workload.
- Warn when workload exceeds available study hours.
- Download the semester plan as CSV.

## Technologies Used

- Python
- Streamlit
- FastAPI
- LangGraph
- Gemini
- ChromaDB
- Altair
- Pandas
- Pytest

## Project Structure

```text
Day10/
├── README.md
└── tests/
    ├── test_feedback.py
    └── test_planner.py

ui/
├── app.py
├── feedback.py
└── planner.py
```

## Testing

Run the automated tests:

```bash
python -m pytest Day10/tests -v
```

Result: 8 tests passed.

## Important Notes

- Exam dates are entered manually by students and are not official NPTEL dates.
- Weekly workload is estimated at 3 hours per selected course. This is a project assumption, not an official NPTEL workload.
- Feedback records are stored locally and excluded from Git using `.gitignore`.

## Run the Application

Start the FastAPI backend:

```bash
python -m uvicorn app.main:app --reload
```

Start the Streamlit frontend in another terminal:

```bash
python -m streamlit run ui/app.py
```

Open:

http://localhost:8501
