# How Large Language Models (LLMs) Work

## 1. What is an LLM?

LLM stands for Large Language Model. It is an Artificial Intelligence model trained on a large amount of text data to understand and generate human-like language.

Examples:
- ChatGPT
- Google Gemini
- Llama
- Claude

## 2. How does an LLM work?

An LLM generally works through these steps:

1. **Input:** The user enters a question or instruction.
2. **Tokenization:** The text is divided into smaller units called tokens.
3. **Processing:** The model processes tokens using a neural network architecture called Transformer.
4. **Prediction:** The model predicts the next likely token.
5. **Generation:** It generates a response one token at a time.
6. **Output:** The generated response is shown to the user.

## 3. What is a Token?

A token is a small unit of text processed by an LLM. It can be a word, part of a word, or a punctuation mark.

## 4. What is a Transformer?

A Transformer is a deep learning architecture used by modern LLMs.

It uses an attention mechanism to understand relationships between different words in a sentence.

## 5. What is Prompt Engineering?

Prompt engineering means writing clear instructions to get better responses from an AI model.

Example:

Bad prompt: Explain Python.

Good prompt: Explain Python loops with simple examples for beginners.

## 6. What is an API?

API stands for Application Programming Interface. It allows two software applications to communicate with each other.

In NPTELPicker, our FastAPI application will communicate with an LLM provider through an API.

## 7. What is RAG?

RAG stands for Retrieval-Augmented Generation.

It combines information retrieval with an LLM.

Steps:
1. User asks a question.
2. Relevant information is retrieved from a knowledge source.
3. Retrieved information is provided to the LLM.
4. The LLM generates an answer based on that information.

## 8. What is Hallucination?

Hallucination happens when an AI model generates incorrect or fabricated information but presents it confidently.

RAG can help reduce hallucinations by providing relevant source information.

## 9. LLM Usage in NPTELPicker

NPTELPicker will use an LLM to:
- Understand student questions.
- Recommend relevant NPTEL courses.
- Explain course details.
- Compare courses.
- Help students choose courses based on their goals.

## Conclusion

LLMs help applications understand and generate human-like language. In NPTELPicker, we will combine an LLM with course information to build an intelligent course recommendation assistant.



## 10. LLM Workflow Diagram

The following diagram explains how an LLM processes a user's question and generates an answer.

```text
+------------------+
|  User Prompt     |
|  (Input Question)|
+--------+---------+
         |
         v
+------------------+
|   Tokenization   |
| Convert text     |
| into tokens      |
+--------+---------+
         |
         v
+------------------+
|    LLM Model     |
| Processes tokens |
| and predicts     |
| next tokens      |
+--------+---------+
         |
         v
+------------------+
| Generated Answer |
|  (Final Output)  |
+------------------+
```

### Workflow Explanation

1. **Prompt:** The user enters a question.
2. **Tokens:** The input text is divided into smaller units called tokens.
3. **Model:** The LLM processes the tokens and generates a response.
4. **Answer:** The final generated answer is returned to the user.