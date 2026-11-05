import uuid
import datetime
import inngest
import inngest.fast_api
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title='Background report jobs rebuild')
client = inngest.Inngest(app_id='report-api', is_production=False, api_base_url='http://localhost:8386', event_api_base_url='http://localhost:8386')

reports = {}

async def report_failed(ctx: inngest.Context):
    original=ctx.event.data.get('event',{}).get('data',{})
    report_id=original.get('id')
    if report_id:
        reports[report_id]={'id':report_id,'status':'failed','error':'Report failed after three attempts'}
    print(f'FINAL FAILURE report_id={report_id}',flush=True)

@client.create_function(fn_id='say-hello', trigger=inngest.TriggerEvent(event='test/hello'))
async def say_hello(ctx: inngest.Context):
    await ctx.step.sleep('wait', datetime.timedelta(seconds=5))
    return 'Hello from the background!'

@client.create_function(fn_id='make-report', trigger=inngest.TriggerEvent(event='report/requested'), retries=2, on_failure=report_failed)
async def make_report(ctx: inngest.Context):
    item = ctx.event.data
    await ctx.step.sleep('wait-for-report', datetime.timedelta(seconds=8))
    def build():
        print(f'BUILD report_id={item["id"]} attempt={ctx.attempt+1}',flush=True)
        if item['topic'] == 'fail':
            raise RuntimeError('Intentional failure for retry exercise')
        result = f"Report about {item['topic']}"
        reports[item['id']] = {'id': item['id'], 'status': 'done', 'result': result}
        return result
    return await ctx.step.run('build-report', build)

@client.create_function(fn_id='heartbeat', trigger=inngest.TriggerCron(cron='* * * * *'))
async def heartbeat(ctx: inngest.Context):
    summary = {status: sum(item['status'] == status for item in reports.values()) for status in ['pending', 'done', 'failed']}
    print(f'Heartbeat at {datetime.datetime.now(datetime.timezone.utc).isoformat()}: {summary}', flush=True)
    return summary

inngest.fast_api.serve(app, client, [say_hello, make_report, heartbeat])

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.post('/reports', status_code=202)
async def create_report(request: Request):
    try: body = await request.json()
    except ValueError: body = {}
    topic = body.get('topic') if isinstance(body, dict) else None
    if not isinstance(topic, str) or not topic.strip():
        return JSONResponse({'error': 'topic required'}, status_code=400)
    report_id = str(uuid.uuid4())
    reports[report_id] = {'id': report_id, 'status': 'pending'}
    try:
        await client.send(inngest.Event(name='report/requested', data={'id': report_id, 'topic': topic.strip()}))
    except Exception:
        reports.pop(report_id, None)
        return JSONResponse({'error': 'job service unavailable'}, status_code=503)
    return reports[report_id]

@app.get('/reports/{report_id}')
def report(report_id: str):
    return reports.get(report_id) or JSONResponse({'error': 'Report not found'}, status_code=404)
