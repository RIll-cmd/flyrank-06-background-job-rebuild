# Actual rebuild checkpoints

Each check was performed before its stage commit.

## Stage 0
2026-11-05T07:31:36.594673+00:00 — `python -m uvicorn app:app --port 8106`; GET http://localhost:8106/health → 200 {"status":"ok"}

## Stage 1
POST http://localhost:8386/e/dev test/hello; after 7 seconds GET /v1/events/01M6NA0FJ9RA9RK4WQ1EVZXY40/runs → {"data":[{"run_id":"01M6NA0FSVNNVKT29T87WM0DC8","run_started_at":"2026-11-05T07:33:11.099Z","function_id":"8836d247-0e03-5e8a-adae-f0ee1e9f890c","function_version":0,"environment_id":"00000000-0000-0000-0000-000000000000","event_id":"01M6NA0FJ9RA9RK4WQ1EVZXY40","status":"Completed","ended_at":"2026-11-05T07:33:16.15184Z","output":"Hello from the background!"}],"metadata":{"fetched_at":"2026-11-05T07:33:17.8686666Z","cached_until":"2026-11-05T07:33:32.8686666Z"}}

The registered function has the real 5-second `wait` sleep. Fresh completed Inngest run evidence: hello-proof.json.
