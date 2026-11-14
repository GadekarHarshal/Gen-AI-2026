
# NPTELPicker – Prompt Comparison Evaluation

## 1. Objective

The objective is to compare two prompt versions for the NPTELPicker assistant using 10 predefined student questions.

The comparison evaluates accuracy, relevance, course recommendations, course comparison, and handling of unavailable information.

## 2. Prompt Versions

### Version 1 – Basic System Prompt

File: `prompts/system_prompt.txt`

This version uses general NPTELPicker instructions.

It:
- Answers NPTEL-related questions.
- Uses only the provided course dataset.
- Avoids inventing course information.
- Identifies unavailable information.
- Returns a structured JSON response.

### Version 2 – System Prompt with Task-Specific Prompts

Files:
- `prompts/system_prompt.txt`
- `prompts/course_recommendation.txt`
- `prompts/course_comparison.txt`

This version combines the system prompt with additional instructions for course recommendations and comparisons.

It:
- Provides structured course recommendations.
- Considers student branch, year, interests and goals.
- Provides structured course comparisons.
- Explicitly handles missing course information.
- Avoids unsupported claims about placements and credit transfer.

## 3. Evaluation Dataset

Both versions use the same dataset:

`data/records.json`

The dataset contains 20 NPTEL course records with course names, IDs, disciplines, institutes, durations, URLs and levels.

It does not contain weekly syllabus details, examination dates, examination centres or university credit-transfer policies.

## 4. Evaluation Questions and Comparison

| ID | Question | Version 1 – Basic Prompt | Version 2 – Task-Specific Prompt |
|---|---|---|---|
| Q1 | What topics are covered in Week 9 of IIT Delhi Computer Architecture? | Can identify the course but should state that weekly topics are unavailable. | Gives clearer guidance to identify missing syllabus information without guessing. |
| Q2 | Is Joy of Computing using Python suitable for beginners? | Should identify that the course is not present in the dataset. | Gives a more structured explanation of missing course information. |
| Q3 | How many credits are recommended for an 8-week NPTEL course? | Should avoid inventing credit information because it is absent from the dataset. | Maintains the same restriction and clearly identifies missing information. |
| Q4 | How many credits can I earn by completing a 12-week NPTEL course? | Should state that credit details are unavailable. | Provides clearer guidance against unsupported credit claims. |
| Q5 | Suggest one 12-week core course and one 4-week placement-useful course for a Second Year Computer Engineering student. | Can identify matching course durations but may provide a less structured recommendation. | Provides dedicated recommendation instructions and considers branch, duration and student goals. |
| Q6 | What is the exact examination date and examination centre for AI for Earth Observation (noc26_cs98)? | Should state that examination information is unavailable. | Explicitly reinforces that examination dates and centres must not be invented. |
| Q7 | Compare Cloud Computing by IIT Kharagpur and Software Testing by IIIT Bangalore. | Can identify Cloud Computing but should report that Software Testing is not found. | Provides a structured comparison while identifying the missing second course. |
| Q8 | Which is better for placements: Python Programming or Data Structures and Algorithms? | Can identify the available Data Structures and Algorithms course but lacks sufficient information about Python Programming. | Gives a more balanced recommendation and avoids unsupported placement claims. |
| Q9 | Will Savitribai Phule Pune University accept NPTEL courses for credit transfer? | Should state that university credit-transfer policy is unavailable. | Explicitly requires official supporting information before making such a claim. |
| Q10 | I can study for 6 hours per week. Suggest a course matching my study time and placement goals. | Can suggest courses from the dataset but cannot verify weekly workload. | Provides better guidance to consider study availability while identifying missing workload information. |

## 5. Evaluation Criteria

Each question can be assessed using five criteria:

1. Accuracy – Correctness of the answer.
2. Grounding – Whether the answer is supported by the dataset.
3. Relevance – Whether it addresses the question.
4. Completeness – Whether important requested details are covered.
5. Hallucination Prevention – Whether unavailable information is handled honestly.

Each criterion can receive:

| Score | Meaning |
|---|---|
| 0 | Incorrect or unsupported |
| 1 | Partially correct |
| 2 | Correct and relevant |

Maximum possible score: 100 points per prompt version.

## 6. Comparison Summary

Version 1 establishes the basic behavior of the NPTELPicker assistant. It provides general instructions for answering questions using the available course records.

Version 2 adds dedicated instructions for recommendations and comparisons.

Expected advantages of Version 2:
- More structured recommendations.
- Clearer course comparisons.
- Better consideration of student requirements.
- More explicit handling of unavailable information.
- Better guidance against unsupported placement and credit-transfer claims.

Both versions must respect the same dataset limitations.

## 7. Evaluation Status

This document contains a qualitative, dataset-based prompt comparison.

The 10 questions have been compared against the instructions in both prompt versions. The comparison is not a record of 20 live Gemini responses, and no measured accuracy scores are claimed.

Actual model performance scores can only be reported after executing both prompt versions separately against all 10 questions.

## 8. Conclusion

The basic system prompt provides general instructions for the NPTELPicker assistant.

The task-specific prompts improve the instructions for course recommendations and course comparisons.

Version 2 is designed to provide more structured and requirement-oriented answers while maintaining the same grounding and hallucination-prevention rules.

The comparison demonstrates the intended differences between the two prompt designs using the 10 predefined questions.
