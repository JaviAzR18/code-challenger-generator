# Code Challenge Generator

A small full-stack app that generates multiple-choice coding questions with an LLM, lets signed-in users answer them, and keeps a personal history.

This is a learning/demo project: it wires auth, an API, a database, and an LLM together. It does **not** try to make the generated questions perfect.

## What it does

- User signs in (Clerk).
- User picks a difficulty and requests a new challenge.
- The backend asks Gemini for a JSON object (`title`, four `options`, `correct_answer_id`, `explanation`).
- The challenge is stored, quota is decremented, and the UI shows the question.
- History lists previous challenges for that user.

## Architecture

```
React (Vite)  --JWT-->  FastAPI  -->  Gemini (OpenAI-compatible API)
                              |
                              +-->  SQLite (SQLAlchemy)
```

- **Frontend:** React + React Router. Clerk issues a JWT; `useApi` sends it as `Authorization: Bearer`.
- **Backend:** FastAPI. Protected routes verify the token with Clerk, then generate, persist, and return challenges.
- **Auth:** Clerk. User id comes from the JWT `sub` claim. Quota is created on first use if it does not exist.
- **Data:** SQLite via SQLAlchemy. Challenges and per-user quotas live in `database.db`.
- **LLM:** Gemini, called with the official OpenAI Python client and Gemini’s compatibility `base_url`. The model is expected to return JSON (`response_format: json_object`). There is a light check that required fields exist—no scoring, no retry loop, no human review of quality.

## Repo structure

```
frontend/                 Vite + React
  src/auth/               Clerk provider and sign-in/up
  src/challenges/          Generator UI and MCQ view
  src/history/             Past challenges
  src/utils/api.js         Authenticated fetch to FastAPI

backend/
  server.py               Uvicorn entrypoint (port 8000)
  src/app.py              FastAPI app, CORS, routers
  src/ai_generator.py     Gemini call + JSON parse
  src/utils.py            Clerk JWT verification
  src/routes/challenges.py Generate, history, quota
  src/routes/webhooks.py  Optional Clerk webhook (not mounted)
  src/database/            Models and helpers
```

## Decisions

- **Gemini over OpenAI billing:** generation uses Gemini (`gemini-3.6-flash`) through `https://generativelanguage.googleapis.com/v1beta/openai/` so the existing OpenAI SDK shape stays. The app is not tied to OpenAI’s paid quota.
- **JSON in the prompt, not a product-grade pipeline:** the system prompt asks for a fixed schema. That is enough to render a quiz. Wrong answers, weak distractors, or mismatched difficulty are accepted as LLM variance.
- **SQLite:** local file, no extra infra. Options are stored as a JSON string.
- **Simple quota:** 50 generations per user, reset on a time window in the backend. Enough to cap abuse in a demo.
- **Clerk on the API, not only the UI:** the frontend is a client; the backend still authenticates every generate/history/quota call.
- **Webhooks are optional:** `webhooks.py` can create quota on `user.created`. The router is commented out in `app.py`; quota is created lazily when generating if missing.

## Run locally

**Backend** (`backend/`):

- Python 3.13+, [uv](https://docs.astral.sh/uv/)
- `src/.env`: `GEMINI_API_KEY`, `CLERK_SECRET_KEY`, `CLERK_JWT_KEY` (and webhook secret only if you enable that route)
- `uv run .\server.py` → `http://localhost:8000`

**Frontend** (`frontend/`):

- Clerk publishable key in the Vite env the app already uses
- `npm install` and `npm run dev` → typically `http://localhost:5173`

CORS is open for local development. `authorized_parties` in Clerk verification currently allow `localhost:5173` and `5174`.
