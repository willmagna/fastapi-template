# fast-api

A small social-style backend: register and log in with JWTs, upload images and videos via [ImageKit](https://imagekit.io/), and read a feed of posts. Stack: **FastAPI**, **SQLAlchemy** (async) + **SQLite**, **fastapi-users**, optional **Streamlit** demo (`frontend.py`).

## Stack

| Area | Choice |
|------|--------|
| HTTP API | FastAPI |
| Auth | fastapi-users (JWT) |
| Database | SQLite (`test.db`), created on startup |
| Media | ImageKit uploads |
| Demo UI | Streamlit → `http://localhost:8000` |

Open **[http://localhost:8000/docs](http://localhost:8000/docs)** for interactive OpenAPI when the server is running.

## Requirements

- **Python 3.13+** (`pyproject.toml`)
- **[uv](https://docs.astral.sh/uv/)** (recommended)
- **ImageKit** account and keys

## Setup

1. Clone the repo and enter the project directory.

2. Copy environment template and fill in values:

   ```bash
   cp .env.example .env
   ```

   | Variable | Notes |
   |----------|--------|
   | `JWT_SECRET_KEY` | Long random string; signs JWTs |
   | `IMAGEKIT_PRIVATE_KEY` | Server uploads |
   | `IMAGEKIT_PUBLIC_KEY` | Listed in `.env.example` for parity with ImageKit; wire in app if you need client-side upload |
   | `IMAGEKIT_URL_ENDPOINT` | e.g. `https://ik.imagekit.io/your_id` — used for URL transforms in Streamlit |

3. Install dependencies:

   ```bash
   uv sync
   ```

## Run the API

```bash
uv run python main.py
```

Runs **uvicorn** on **0.0.0.0:8000** with reload (`app.app:app`).

Equivalent:

```bash
uv run uvicorn app.app:app --reload --host 0.0.0.0 --port 8000
```

## Run the Streamlit app (optional)

Terminal 1: API as above. Terminal 2:

```bash
uv run streamlit run frontend.py
```

Use the URL Streamlit prints (usually **http://localhost:8501**).

**Note:** `frontend.py` calls `/upload`, `/feed`, and `/posts/{id}`. The router mounts posts under **`/posts`**, so working paths are **`POST /posts/upload`**, **`GET /posts/feed`**, and **`DELETE /posts/posts/{post_id}`**. If the UI returns 404 on feed or upload, update those URLs in `frontend.py` to match `/docs`.

## Main HTTP surfaces

- **Auth / users** — fastapi-users routes (register, JWT login, `/users/me`, etc.) — see `/docs`
- **Posts** (Bearer token required):
  - `POST /posts/upload` — multipart file + optional caption
  - `GET /posts/feed` — feed JSON
  - `DELETE /posts/posts/{post_id}` — delete (path reflects current router prefix + handler path)

## Repo layout

```
fast-api/
├── main.py              # Dev server entry
├── frontend.py          # Streamlit client
├── .env.example         # Env template
├── pyproject.toml
├── uv.lock
├── app/
│   ├── app.py           # FastAPI app + routers
│   ├── db.py            # Engine, models, session
│   ├── users.py         # JWT + UserManager
│   ├── images.py        # ImageKit client
│   ├── schemas.py
│   └── modules/posts/   # Routes + controllers
└── test.db              # Created when the API runs
```

## Troubleshooting

- **JWT errors** — Set `JWT_SECRET_KEY` in `.env` and restart the API.
- **Upload failures** — Check `IMAGEKIT_PRIVATE_KEY` and ImageKit dashboard.
- **Port 8000 busy** — Change port in `main.py` or pass `--port` to uvicorn; update `frontend.py` URLs if you use Streamlit.
