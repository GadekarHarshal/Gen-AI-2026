# Day 09 - AI Agent and LangGraph

## Objective
Build an AI agent that selects and executes the appropriate
NPTELPicker tool using a hand-written agent loop and LangGraph.

## 1. Course Plan Checker
File: `app/tools.py`

Features:
- Looks up courses using course IDs.
- Calculates credits using the planned mapping:
  - 12 weeks = 3 credits
  - 8 weeks = 2 credits
  - 4 weeks = 1 credit
- Estimates study workload.
- Checks whether available study hours are sufficient.
- Reports unknown course IDs.
- Reports exam clash checking as unavailable because exam
  dates are missing from the dataset.

Workload assumption:
3 estimated study hours per course per week.
This is a planning estimate, not official NPTEL workload.

## 2. Hand-Written Agent Loop
File: `app/agent_loop.py`

Features:
- Uses Gemini to select the appropriate tool.
- Selects RAG for course-related questions.
- Selects Course Plan Checker for planning questions.
- Extracts course IDs and available study hours.
- Requests missing information when necessary.

## 3. LangGraph Workflow
File: `app/graph.py`

Features:
- Uses LangGraph StateGraph.
- Routes questions to RAG or Course Plan Checker.
- Maintains conversation state using InMemorySaver.
- Supports human approval before executing course plans.
- Supports approval and rejection.

Note:
Memory and provider storage are maintained in application
memory. They are not persistent across server restarts.

## 4. API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | /agent | Execute the AI agent |
| POST | /agent/approve | Approve or reject a course plan |

Existing Day 6, Day 7 and Day 8 endpoints are preserved.

## 5. Tests

Test files:
- `Day09/tests/test_tools.py`
- `Day09/tests/test_agent_loop.py`
- `Day09/tests/test_graph.py`

Day 9 test results:
- Course planning tests: 6
- Agent loop tests: 7
- LangGraph tests: 7

Total Day 9 tests: 20

Full project test results:
25 passed.

## 6. Verification

- Manual RAG agent test: Passed.
- Course planning agent test: Passed.
- Conversation memory test: Passed.
- Approval workflow: Passed.
- Rejection workflow: Passed.
- Python compilation: Passed.
- Dependency check: Passed.

## 7. Limitations

- Exam clash checking is unavailable because examination dates
  are not present in the dataset.
- Workload is estimated using 3 hours per course per week.
- Credit mapping is a planned project rule.
- In-memory conversation state is lost after server restart.