import datetime
import inngest
import inngest.fast_api
from fastapi import FastAPI

app = FastAPI(title='Background report jobs rebuild')
client = inngest.Inngest(app_id='report-api', is_production=False, api_base_url='http://localhost:8386', event_api_base_url='http://localhost:8386')

@client.create_function(fn_id='say-hello', trigger=inngest.TriggerEvent(event='test/hello'))
async def say_hello(ctx: inngest.Context):
    await ctx.step.sleep('wait', datetime.timedelta(seconds=5))
    return 'Hello from the background!'

inngest.fast_api.serve(app, client, [say_hello])

@app.get('/health')
def health():
    return {'status': 'ok'}
