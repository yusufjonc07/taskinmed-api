from fastapi import APIRouter
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from starlette.responses import Response

metrics_router = APIRouter(tags=["Website Montoring | Metrics"])


#Expose metrics endpoint
@metrics_router.get("/metrics")
def metrics():
    metrics_data = generate_latest()  # Get all default metrics
    return Response(content=metrics_data, media_type=CONTENT_TYPE_LATEST)