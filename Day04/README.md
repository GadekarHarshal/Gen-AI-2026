# Day 4 - NPTELPicker

## 1. FastAPI
Created a FastAPI application with five endpoints.

- GET /health
- GET /records
- GET /records/{course_id}
- GET /search
- POST /questions

## 2. Data Analysis
Used pandas to analyse NPTEL course records.

Facts:
- Total courses: 20
- Total institutes: 7
- Most common institute: IIT Kharagpur

## 3. Smart Search
Implemented TF-IDF and cosine similarity.

Smart search finds relevant courses based on user queries.

## 4. Technologies
- Python
- FastAPI
- Pandas
- Scikit-learn
- Uvicorn

## 5. How to Run

Activate virtual environment:

.venv\Scripts\Activate.ps1

Start API:

uvicorn Day04.app.main:app --reload

Open:

http://127.0.0.1:8000/docs