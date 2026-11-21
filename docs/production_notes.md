# NPTELPicker – Production Notes

## 1. Deployment

- Backend: FastAPI
- Frontend: Streamlit
- Hosting: Render
- LLM Provider: Google Gemini
- Vector Database: ChromaDB

## 2. Performance Monitoring

The application logs the following information for Gemini requests:

- Model name
- Request latency in milliseconds
- Input token count
- Output token count
- Total token count

## 3. Response Caching

An in-memory LRU-style cache is implemented using OrderedDict.

- Maximum cache size: 100 entries
- Repeated prompts return cached responses.
- Cache hits avoid additional Gemini API calls.
- The cache is cleared when the application process restarts.

## 4. Observed Performance

Sample measurements from local testing:

| Metric | Observed Result |
|---|---:|
| Gemini request latency | 945.88 ms |
| Input tokens | 8 |
| Output tokens | 52 |
| Total tokens | 60 |
| Cache test | Cache HIT on repeated prompt |

Note: These are sample observations from individual tests, not formal production benchmarks.

## 5. Validation and Security

- Question input is stripped of surrounding whitespace.
- Question length is restricted to 3–1000 characters.
- Semantic search query length is restricted to 1–1000 characters.
- Prompt instructions include protection against prompt injection.
- Three manual prompt-injection test cases were checked.

## 6. Testing

- Pytest: 45 tests passed.
- Ruff: All checks passed.
- Python syntax compilation: Passed.

## 7. Production Considerations

- Configure GEMINI_API_KEY securely through environment variables.
- Monitor API usage and rate limits.
- The current response cache is in-memory and instance-specific.
- Render free-tier services may sleep when inactive.
- ChromaDB persistence and indexing should be monitored after restarts.