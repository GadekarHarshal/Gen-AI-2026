
# Day 7 - Semantic Search Evaluation

## 1. Overview

Semantic search was tested using 10 sample questions from Day05/questions.md.

The system uses:
- Gemini Embedding Model: gemini-embedding-001
- Vector Database: ChromaDB
- Collection: nptel_courses
- Embedding Dimensions: 3072
- Top Results: 3 per query

## 2. Evaluation Results

### Q1. What topics are covered in Week 9 of the IIT Delhi Computer Architecture course?

Top Results:
1. Computer Architecture - Distance: 0.2672
2. Computer Architecture and Organization - Distance: 0.3086
3. Advanced Distributed Systems - Distance: 0.3198

Observation: The system retrieved Computer Architecture as the closest matching course. Weekly syllabus details are not available in the current dataset.

### Q2. Is the Joy of Computing using Python course suitable for beginners?

Top Results:
1. Cloud Computing - Distance: 0.3816
2. Data Structure and Algorithms using Java - Distance: 0.3895
3. C Programming and Assembly Language - Distance: 0.4030

Observation: The expected Python course was not retrieved. The available course metadata does not contain beginner-level descriptions.

### Q3. How many credits are recommended for an 8-week NPTEL course?

Top Results:
1. Data Science for Engineers - Distance: 0.3624
2. Computer Graphics - Distance: 0.3647
3. Data Structure and Algorithms using Java - Distance: 0.3652

Observation: Relevant course records were retrieved, but credit recommendations are not included in the dataset.

### Q4. How many credits can I earn by completing a 12-week NPTEL course?

Top Results:
1. Computer Networks - Distance: 0.3436
2. Computer Architecture - Distance: 0.3491
3. Cloud Computing - Distance: 0.3515

Observation: The system retrieved 12-week-related courses. Credit information is unavailable in the current dataset.

### Q5. I am a Second Year Computer Engineering student. Suggest one 12-week core course and one 4-week placement-useful course.

Top Results:
1. Data Structure and Algorithms using Java - Distance: 0.3582
2. C-Based VLSI Design - Distance: 0.3593
3. Computer Networks - Distance: 0.3670

Observation: Data Structure and Algorithms using Java is a relevant core-course match. The dataset does not establish whether a suitable 4-week placement course is available.

### Q6. What is the exact examination date and examination centre for AI for Earth Observation (noc26_cs98)?

Top Results:
1. AI for Earth Observation - Distance: 0.2317
2. Artificial Intelligence: Foundations and Algorithms - Distance: 0.3540
3. Computer Vision - Distance: 0.3668

Observation: The correct course was retrieved. Examination date and examination centre details are unavailable and must not be invented.

### Q7. Compare Cloud Computing by IIT Kharagpur and Software Testing by IIIT Bangalore.

Top Results:
1. Cloud Computing - Distance: 0.2691
2. Computer Architecture and Organization - Distance: 0.3700
3. Data Structure and Algorithms using Java - Distance: 0.3702

Observation: Cloud Computing was retrieved correctly. The second requested course was not retrieved in the top three results, so the comparison is incomplete.

### Q8. Which is better for placements: Python Programming or Data Structures and Algorithms?

Top Results:
1. Data Structure and Algorithms using Java - Distance: 0.3176
2. Data Science for Engineers - Distance: 0.4055
3. Approximation Algorithm - Distance: 0.4073

Observation: Data Structure and Algorithms using Java is a relevant match for the placement-related query. The dataset does not provide comparative placement outcomes.

### Q9. Will Savitribai Phule Pune University accept NPTEL courses for credit transfer?

Top Results:
1. Computer Networks - Distance: 0.4013
2. Data Structure and Algorithms using Java - Distance: 0.4119
3. Data Science for Engineers - Distance: 0.4135

Observation: The retrieved courses do not answer the university credit-transfer question. Official university verification is required.

### Q10. I can study for 6 hours per week. Suggest an NPTEL course matching my available study time and placement goals.

Top Results:
1. Data Structure and Algorithms using Java - Distance: 0.3318
2. Data Science for Engineers - Distance: 0.3445
3. Approximation Algorithm - Distance: 0.3515

Observation: Relevant placement-related courses were retrieved. Weekly workload information is not available to verify the 6-hour requirement.

## 3. Evaluation Summary

- Total queries tested: 10
- Queries executed successfully: 10
- Results retrieved per query: 3
- Total retrieved results: 30
- Embedding model: gemini-embedding-001
- Vector database: ChromaDB

All 10 queries successfully generated embeddings and returned semantic search results.

This confirms that the semantic retrieval pipeline is operational. It does not mean that all 10 questions were answered correctly.

## 4. Limitations

1. The current dataset contains course metadata rather than detailed syllabus documents.
2. Credit recommendations are not included.
3. Examination dates and examination centres are unavailable.
4. University credit-transfer policies are not included.
5. Weekly workload and placement outcomes are unavailable.
6. Semantic search does not guarantee exact duration or eligibility filtering.

## 5. Conclusion

Day 7 successfully implements document chunking, Gemini embeddings, persistent ChromaDB storage and a FastAPI semantic search endpoint.

The system successfully retrieves relevant course records for natural-language queries.

Additional syllabus documents and structured academic information will be needed to improve retrieval accuracy and answer more detailed student questions.
