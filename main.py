import os
import uvicorn
import structlog

from authentication import authorize_request
from request import CompletePromptParameters
from response import CompleteResponse

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse
from provider.google import VertexAI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
instrumentator = Instrumentator().instrument(app).expose(app)
vertex_ai_client = VertexAI(os.getenv("GCP_PROJECT_ID", "sscs-play"),
                            os.getenv("GCP_REGION", "us-west1"))

structlog.configure(
    processors=[
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer(),
    ]
)
logger = structlog.get_logger(__name__)


@app.middleware("http")
async def log_request(request: Request, call_next):
    response = None
    try:
        response = await call_next(request)
    except Exception as ex:
        logger.error(str(ex), exc_info=ex)
        response = PlainTextResponse(str(ex), status_code=500)
    return response


@app.get("/project")
def hello():
    return vertex_ai_client.project_id


@app.post("/packages")
def complete(
        request: CompletePromptParameters,
        issuer: str = Depends(authorize_request)) -> CompleteResponse:
    response = vertex_ai_client.text(request.prompt,
                                     request.model_name,
                                     request.model_parameters.temperature,
                                     request.model_parameters.max_output_tokens,
                                     request.model_parameters.top_p,
                                     request.model_parameters.top_k)
    return response


@app.get("/healthz")
def healthz():
    return "OK"


if __name__ == "__main__":
    app_port = int(os.getenv('APP_PORT', 8001))
    uvicorn.run(app, host="0.0.0.0", port=app_port)
