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

These metrics help monitor API performance and token consumption.

## 3. Response Caching

An in-memory LRU-style cache is implemented using `OrderedDict`.

- Maximum cache size: 100 entries.
- Repeated prompts return cached responses.
- Cache hits avoid additional Gemini API calls.
- Cache misses trigger a new Gemini API request.
- The oldest cached response is removed when the cache exceeds its maximum capacity.
- The cache is cleared when the application process restarts.

## 4. Observed Performance

Sample measurements collected during local testing:

| Metric | Observed Result |
|---|---:|
| Gemini request latency | 945.88 ms |
| Input tokens | 8 |
| Output tokens | 52 |
| Total tokens | 60 |
| Maximum cache capacity | 100 entries |
| Cache verification | Cache HIT |

### Response Cache Verification

- First request: Cache MISS; Gemini API was called.
- Second identical request: Cache HIT; cached response was returned.
- Repeated requests avoided additional Gemini API calls.

**Note:** These are sample observations from individual development tests, not formal production benchmarks. Actual performance may vary depending on network conditions and API load.

## 5. Validation and Security

- Question input is stripped of surrounding whitespace.
- Question length is restricted to 3–1000 characters.
- Semantic search query length is restricted to 1–1000 characters.
- Pydantic validation is applied to Chat and Agent questions.
- Prompt instructions include protection against prompt injection.
- Student inputs and retrieved documents are treated as untrusted content.
- Three manual prompt-injection test cases were checked:
  - Attempt to override previous instructions.
  - Attempt to reveal the system prompt.
  - Attempt to reveal the Gemini API key.
- All three test attempts were refused by the model.

## 6. Testing

The following development checks were completed:

| Test | Result |
|---|---|
| Complete Pytest suite | 45 tests passed |
| Ruff code quality checks | All checks passed |
| Python syntax compilation | Passed |
| Gemini latency monitoring | Verified |
| Token usage logging | Verified |
| Response cache MISS | Verified |
| Response cache HIT | Verified |
| Prompt-injection manual tests | 3/3 refused |

## 7. Production Considerations

- Configure `GEMINI_API_KEY` securely through environment variables.
- Never commit API keys or credentials to GitHub.
- Monitor Gemini API usage and rate limits.
- The current response cache is in-memory and instance-specific.
- Cached responses are lost when the application process restarts.
- Render free-tier services may sleep when inactive.
- ChromaDB persistence and indexing should be monitored after backend restarts.
- Monitor API latency and token consumption during actual usage.

