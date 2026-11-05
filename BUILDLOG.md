# Actual rebuild checkpoints

Each check was performed before its stage commit.

## Stage 0
2026-11-05T07:31:36.594673+00:00 — `python -m uvicorn app:app --port 8106`; GET http://localhost:8106/health → 200 {"status":"ok"}

## Stage 1
POST http://localhost:8386/e/dev test/hello; after 7 seconds GET /v1/events/01M6NA0FJ9RA9RK4WQ1EVZXY40/runs → {"data":[{"run_id":"01M6NA0FSVNNVKT29T87WM0DC8","run_started_at":"2026-11-05T07:33:11.099Z","function_id":"8836d247-0e03-5e8a-adae-f0ee1e9f890c","function_version":0,"environment_id":"00000000-0000-0000-0000-000000000000","event_id":"01M6NA0FJ9RA9RK4WQ1EVZXY40","status":"Completed","ended_at":"2026-11-05T07:33:16.15184Z","output":"Hello from the background!"}],"metadata":{"fetched_at":"2026-11-05T07:33:17.8686666Z","cached_until":"2026-11-05T07:33:32.8686666Z"}}

The registered function has the real 5-second `wait` sleep. Fresh completed Inngest run evidence: hello-proof.json.

## Stage 2
Restarted API and synchronized Inngest. POST http://127.0.0.1:8106/reports topic cats, poll immediately then after 10 seconds. Windows localhost name resolution added >1s to a first probe, so timed the loopback IP directly. Real proof:
```json
{
  "observed_at": "2026-11-05T07:35:18.215951+00:00",
  "post_status": 202,
  "response_seconds": 0.021,
  "response": {
    "id": "cc8ef43f-26fd-4cda-919f-803aa464752d",
    "status": "pending"
  },
  "pending_poll": {
    "id": "cc8ef43f-26fd-4cda-919f-803aa464752d",
    "status": "pending"
  },
  "later_poll": {
    "id": "cc8ef43f-26fd-4cda-919f-803aa464752d",
    "status": "done",
    "result": "Report about cats"
  },
  "unknown_status": 404
}
```

## Stage 3
Live POST topic fail, then GET status; missing topic POST returned 400. SDK retries=2 gives three total attempts. Real logs:
```json
{
  "observed_at": "2026-11-05T07:37:25.067889+00:00",
  "failed_poll": {
    "id": "4f534c39-457b-4f66-8311-e167eb223333",
    "status": "failed",
    "error": "Report failed after three attempts"
  },
  "attempt_log": [
    "BUILD report_id=4f534c39-457b-4f66-8311-e167eb223333 attempt=1",
    "BUILD report_id=4f534c39-457b-4f66-8311-e167eb223333 attempt=2",
    "BUILD report_id=4f534c39-457b-4f66-8311-e167eb223333 attempt=3",
    "FINAL FAILURE report_id=4f534c39-457b-4f66-8311-e167eb223333"
  ],
  "missing_topic_status": 400
}
```
Retries are safe here because the build step has no external side effects; real email/charge jobs require idempotency to prevent duplicates.
