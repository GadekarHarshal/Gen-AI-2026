
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
- Evaluation of RAG configurations.

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
| Accuracy | 100% | 100% |

**Selected Configuration: Config B**

Config B was selected because it achieved the same evaluation score while generating fewer chunks. It also retrieves more context per question.

**Evaluation Note:** The evaluation checks expected response behaviour, including citations and handling of unavailable information. It does not independently verify every factual statement.

## Technologies Used

- Python
- FastAPI
- Gemini API
- ChromaDB
- Embeddings
- Retrieval-Augmented Generation (RAG)
- Scikit-learn
- Git and GitHub
- Visual Studio Code


## Day 10 - Streamlit UI and Semester Planner

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

### Run the Streamlit Application

```bash
python -m streamlit run ui/app.py
```

Open http://localhost:8501 in your browser.
