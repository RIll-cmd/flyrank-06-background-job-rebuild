import asyncio
from types import SimpleNamespace
from app import reports,report_failed

def test_exhausted_job_exposes_failure():
    reports['failed-test']={'id':'failed-test','status':'pending'}
    ctx=SimpleNamespace(event=SimpleNamespace(data={'event':{'data':{'id':'failed-test'}}}))
    asyncio.run(report_failed(ctx))
    assert reports['failed-test']['status']=='failed'
