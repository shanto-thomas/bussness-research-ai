# Business Research AI

API and Streamlit app for researching a business idea. You describe the idea, choose research areas, and the app returns a written report plus a PDF.

Specialist agents cover market, competitors, customers, pricing, finance, legal, and technology. They search the web with DuckDuckGo and read pages when a source URL is available. A synthesis step merges those results, and a report agent writes the final document.

## Requirements

- Python 3.13 or newer
- [uv](https://docs.astral.sh/uv/)
- An OpenAI API key

## Setup

```bash
uv sync
cp .env.example .env
```

Set `OPENAI_API_KEY` in `.env`. The other values have defaults:

| Variable | Default | Purpose |
|---|---|---|
| `APP_NAME` | Business Research AI | API title |
| `APP_ENV` | development | Shown by `/health` |
| `DEBUG` | true | Debug flag |
| `LLM_MODEL` | gpt-5.6-luna | Chat model |
| `LLM_TIMEOUT` | 60 | Model timeout in seconds |
| `LLM_MAX_RETRIES` | 2 | Model retries |

`.env` is gitignored.

## Run

Start the API:

```bash
uv run uvicorn business_research_ai.main:app --host 127.0.0.1 --port 8000
```

Interactive docs are at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

Start the Streamlit UI in a second terminal:

```bash
uv run streamlit run frontend/app.py
```

The UI calls `http://127.0.0.1:8000` unless you set `API_BASE_URL`.

## How a session works

1. `POST /api/v1/research/session` creates an in-memory session.
2. The first `POST /api/v1/research/session/{session_id}/message` stores the business idea.
3. Later messages are classified as one area, all remaining areas, or report generation.
4. Each area runs its specialist agent. Search tools are limited to 5 calls per tool, and the model is limited to 8 calls per run. Failed searches are retried twice.
5. Report generation writes the synthesis, the report, and `generated_reports/{session_id}.pdf`.

Sessions live in the API process. Restarting the API clears them.

`GET /api/v1/research/session/{session_id}` returns the idea, chat history, completed areas, research text, report, and PDF path.

`POST /api/v1/research` with `{ "business_idea": "..." }` runs every area in one request and returns the report JSON as a string. The Streamlit **Full report** tab uses this endpoint. **Guided research** uses the session endpoints.

## Tests

```bash
uv run pytest
```


