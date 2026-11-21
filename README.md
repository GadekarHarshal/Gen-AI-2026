![NPTELPicker CI](https://github.com/GadekarHarshal/Gen-AI-2026/actions/workflows/ci.yml/badge.svg)

# NPTELPicker
### NPTEL Course Discovery and Selection Assistant

## Project Card

**1. Product:**

NPTELPicker – An AI-powered assistant that helps students discover and select suitable NPTEL courses.

**2. Target User:**

A second-year Computer Engineering student at Sanjivani University who needs to select one NPTEL course for credit transfer and wants to learn skills useful for placements.

**3. Problem:**

Students find it difficult to select suitable NPTEL courses from the large course catalogue. They need recommendations based on their branch, academic year, learning goals, course duration, credits and exam dates.

**4. Data Sources:**

- SWAYAM NPTEL Portal: https://swayam.gov.in/nc_details/NPTEL
- NPTEL Course Page: https://nptel.ac.in/courses/106102157
- Published Google Sheet exported as CSV.
- Collected NPTEL course metadata.

## Project Goal

To recommend suitable NPTEL courses based on a student's branch, year and learning goals using available course information.

## Main Features

- NPTEL course recommendations.
- Course search and filtering.
- Retrieval-Augmented Generation (RAG).
- Semantic search using embeddings.
- AI-powered question answering with source citations.
- Course information retrieval using ChromaDB.
- LangGraph-based AI agent.
- Semester Planner with course selection and timeline.
- Feedback collection.
- Dockerized FastAPI backend and Streamlit frontend.

## Day 1 Activities

- Created the NPTELPicker project card.
- Used Python variables and f-strings.
- Implemented user interaction using input().
- Created a menu-driven program using a while loop.
- Implemented conditional statements using if/elif/else.

## Day 8 Activities – RAG and Evaluation

- Implemented the RAG pipeline in `app/rag.py`.
- Retrieved relevant course information from ChromaDB.
- Integrated Gemini to generate answers using retrieved context.
- Added the `POST /ask` API endpoint.
- Implemented source citations in generated answers.
- Added a rule to return "I don't know" when the available information does not contain the answer.
- Created an evaluation dataset containing 15 questions.
- Compared two RAG configurations.

### RAG Configuration Comparison

| Parameter | Config A | Config B |
|---|---:|---:|
| Chunk Size | 250 | 500 |
| Overlap | 25 | 50 |
| Top-K | 3 | 5 |
| Total Chunks | 40 | 20 |
| Questions Tested | 15 | 15 |
| Passed | 15 | 15 |
| Behaviour Score | 100% | 100% |

**Selected Configuration: Config B**

Config B was selected because it achieved the same evaluation score while generating fewer chunks. It also retrieves more context per question.

**Evaluation Note:** The evaluation checks expected response behaviour, including citations and handling of unavailable information. It does not independently verify every factual statement.

## Day 9 Activities – AI Agent and LangGraph

- Implemented the Course Plan Checker tool.
- Created a hand-written AI agent loop.
- Integrated LangGraph StateGraph workflow.
- Implemented conversation memory using thread IDs.
- Added human approval for course plan execution.
- Added FastAPI endpoints for agent interaction and approval.

## Day 10 – Streamlit UI and Semester Planner

### Features

- Streamlit-based AI Chat Assistant.
- FastAPI and LangGraph agent integration.
- Source citations in chat responses.
- Persistent thumbs-up and thumbs-down feedback.
- Semester Planner with course selection.
- Interactive course timeline using Altair.
- Manual exam-date entry and exam clash detection.
- Weekly workload estimation and warnings.
- Semester plan export to CSV.

### Testing

- 8 automated tests passed.
- Feedback persistence tests.
- Exam clash detection tests.
- Weekly workload calculation tests.

## Day 11 – Testing, Code Quality and Dockerization

### S1 – Testing and Code Quality

- Created a root `tests/` directory.
- Added 12 Day 11 automated tests.
- Tested course record loading and searching.
- Tested the FastAPI `/health` endpoint.
- Tested the `/ask` endpoint using a fake LLM without making real Gemini API calls.
- Tested the Course Plan Checker tool.
- Integrated Ruff for Python code quality checks.
- Verified the complete project test suite.

### S2 – Dockerization

- Created a `Dockerfile` for the application.
- Created `.dockerignore` to exclude unnecessary files and sensitive information.
- Created `docker-compose.yml` to manage FastAPI and Streamlit services.
- Configured Docker networking between the frontend and backend.
- Configured Gemini environment variables through `Day06/.env`.
- Mounted the existing ChromaDB directory for data persistence.
- Successfully built and started both Docker containers.

### Day 11 Testing Results

| Test | Result |
|---|---|
| Day 11 tests | 12 passed |
| Complete project tests | 45 passed |
| Ruff checks | Passed |
| Docker image build | Passed |
| FastAPI container | Passed |
| Streamlit container | Passed |
| Backend connectivity | Passed |
| Semester Planner | Passed |
| AI Chat with Gemini | Passed |

## Technologies Used

- Python
- FastAPI
- Streamlit
- Google Gemini API
- ChromaDB
- LangGraph
- Embeddings
- Retrieval-Augmented Generation (RAG)
- Scikit-learn
- Pandas
- Altair
- Docker
- Docker Compose
- Pytest
- Ruff
- Git and GitHub
- Visual Studio Code

## Installation and Setup

### Prerequisites

- Python 3.13
- Docker Desktop
- Docker Compose
- Google Gemini API key

### Environment Configuration

Create or configure the environment file:

`Day06/.env`

Add the following variables:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
```

Never commit your actual API key to GitHub.

## Run Locally

### 1. Create and activate virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start FastAPI

```bash
python -m uvicorn app.main:app --reload
```

Backend URL: http://localhost:8000

API documentation: http://localhost:8000/docs

### 4. Start Streamlit

Open another terminal and activate the virtual environment.

```bash
python -m streamlit run ui/app.py
```

Frontend URL: http://localhost:8501

## Run with Docker

Docker allows the FastAPI backend and Streamlit frontend to run together in separate containers.

### 1. Start Docker Desktop

Make sure Docker Desktop is running.

### 2. Build and start the application

From the project root directory, execute:

```bash
docker compose up --build
```

To run the containers in the background:

```bash
docker compose up -d --build
```

### 3. Access the application

| Service | URL |
|---|---|
| Streamlit Frontend | http://localhost:8501 |
| FastAPI Backend | http://localhost:8000 |
| API Documentation | http://localhost:8000/docs |
| Health Check | http://localhost:8000/health |

### 4. Check running containers

```bash
docker compose ps
```

### 5. View application logs

API logs:

```bash
docker compose logs api
```

Streamlit logs:

```bash
docker compose logs ui
```

### 6. Stop the application

```bash
docker compose down
```

**Note:** Docker Compose uses `Day06/.env` to provide Gemini credentials to the backend. The local ChromaDB directory is mounted into the API container to preserve its data.

## Project Repository

GitHub: https://github.com/GadekarHarshal/Gen-AI-2026



## Live Deployment

NPTELPicker is deployed on Render.

| Service | Live URL |
|---|---|
| Streamlit Frontend | https://nptelpicker-ui.onrender.com |
| FastAPI Backend | https://nptelpicker-api.onrender.com |
| API Documentation | https://nptelpicker-api.onrender.com/docs |
| Health Check | https://nptelpicker-api.onrender.com/health |

### Deployment Features

- Backend deployed as a FastAPI web service.
- Frontend deployed as a separate Streamlit web service.
- Google Gemini API integration.
- ChromaDB course indexing during backend startup.
- GitHub Actions CI pipeline.
- Automated code-quality checks using Ruff.
- Automated testing using Pytest.
- Docker image build verification.

**Hosting Platform:** Render

**CI/CD Platform:** GitHub Actions