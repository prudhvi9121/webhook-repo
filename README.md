# Webhook Repo

A simple Flask + MongoDB backend with a minimal frontend to display webhook events.

## Setup

1. Clone the repo
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up MongoDB and update `.env` as needed
4. Run the backend:
   ```bash
   python backend/app.py
   ```
5. Open `frontend/index.html` in your browser

## Project Structure

- `backend/` — Flask server, MongoDB logic, utilities
- `frontend/` — Minimal UI, polling logic

## Environment Variables

See `.env` for MongoDB URI, DB name, and port. 