# NPTELPicker – Project Interview Preparation

## 1. Project Introduction (60 Seconds)

NPTELPicker is an AI-powered NPTEL Course Discovery and Selection Assistant developed to help students choose suitable NPTEL courses based on their academic branch, year and learning goals.

The application uses Python, FastAPI and Streamlit. I integrated Google Gemini for AI-powered responses and implemented Retrieval-Augmented Generation using LangChain, embeddings and ChromaDB to retrieve relevant course information.

I also developed a LangGraph-based AI agent with a Course Plan Checker, a Semester Planner with exam clash detection and weekly workload estimation.

For deployment, I used Docker, GitHub Actions and Render. I also implemented response caching, API performance monitoring and input validation.

The main objective is to simplify NPTEL course selection and help students choose courses that support their academic and placement goals.

## 2. Frequently Asked Project Interview Questions

### Q1. What problem does NPTELPicker solve?

Students often find it difficult to select appropriate NPTEL courses from a large catalogue. They need to consider their branch, academic year, course duration, credits, exam dates and career goals.

NPTELPicker simplifies this process by providing course discovery, filtering and AI-powered recommendations.

### Q2. Why did you use RAG?

I used Retrieval-Augmented Generation to make the answers more relevant to the available NPTEL course information.

Instead of relying only on the LLM's internal knowledge, the system retrieves relevant course information from ChromaDB and provides that context to Gemini for generating answers.

### Q3. What is ChromaDB and why did you use it?

ChromaDB is a vector database used to store and retrieve embeddings.

I used it to store course-related information and perform semantic search. It helps retrieve relevant information based on the meaning of a student's query.

### Q4. What is semantic search?

Semantic search retrieves information based on meaning rather than only exact keyword matching.

For example, a student searching for "AI courses for placements" can retrieve relevant courses even if the exact phrase is not present in the course description.

### Q5. Why did you use LangGraph?

I used LangGraph to implement the AI agent workflow.

It helps manage the agent's execution flow, conversation state and interactions with tools such as the Course Plan Checker.

### Q6. What is the role of Google Gemini?

Google Gemini is the LLM provider used to generate AI-powered responses.

It receives the student query and relevant retrieved context, then generates a contextual response.

### Q7. What is the role of FastAPI?

FastAPI provides the backend APIs and connects the frontend with the AI components.

It handles chat requests, semantic search, RAG-based question answering and agent interactions.

### Q8. Why did you use Streamlit?

I used Streamlit to develop the frontend quickly using Python.

It provides the AI Chat Assistant, Semester Planner, course selection interface and feedback functionality.

### Q9. How did you deploy the project?

I used Docker for containerization and Render for cloud deployment.

The FastAPI backend and Streamlit frontend were deployed as separate services. GitHub Actions automates code quality checks, testing and Docker image building.

### Q10. What improvements did you implement for performance and security?

I implemented an in-memory response cache using OrderedDict to avoid repeated Gemini API calls for identical prompts.

I also added Gemini request latency and token usage monitoring, Pydantic input validation and prompt injection protection instructions.

## 3. Important Technical Concepts to Revise

| Concept | What to Explain |
|---|---|
| RAG | Retrieval + context + generation |
| Embeddings | Converting text into numerical vectors |
| ChromaDB | Vector storage and similarity search |
| LangGraph | Agent workflow and state management |
| Gemini | LLM response generation |
| FastAPI | Backend API development |
| Streamlit | Python frontend |
| Docker | Application containerization |
| GitHub Actions | Automated CI pipeline |
| Render | Cloud deployment |
| Caching | Reusing previously generated responses |
| Pydantic | Request validation |

## 4. Project Architecture Explanation

The student interacts with the Streamlit frontend.

The frontend communicates with the FastAPI backend. The backend handles requests through the relevant API endpoints.

For RAG-based questions, relevant information is retrieved from ChromaDB and passed to Google Gemini.

The LangGraph agent supports agent-based workflows and the Course Plan Checker.

Finally, the generated response is returned to the frontend.

## 5. Project Challenges

### Challenge 1: Gemini API Integration

I faced API errors and model availability issues during integration. I resolved these by updating the model configuration and handling API errors.

### Challenge 2: Vector Database Integration

I needed to convert course information into embeddings and store it in ChromaDB. I implemented document chunking, embeddings and semantic retrieval.

### Challenge 3: Deployment

Deploying the frontend and backend separately required correct API configuration and communication between the two services.

### Challenge 4: Repeated API Calls

Repeated queries could generate unnecessary Gemini API requests. I implemented an in-memory response cache to reduce duplicate calls.

## 6. Future Improvements

- Expand the NPTEL course dataset.
- Improve personalized recommendations.
- Add more academic disciplines.
- Improve recommendation evaluation.
- Introduce persistent and shared caching.
- Expand automated security testing.