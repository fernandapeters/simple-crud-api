import time
import random
import string
import uvicorn
import logging

from fastapi import FastAPI, HTTPException, Request

from .router import router
from . import database


logging.config.fileConfig('config/logging.conf', disable_existing_loggers=False)

logger = logging.getLogger(__name__)

database.Base.metadata.create_all(bind=database.engine)


def start_application():
    app_ = FastAPI()
    app_.include_router(router)
    return app_


app = start_application()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status code={response.status_code}")

    return response


@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.exception(e)
        if isinstance(e, HTTPException):
            raise e


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
