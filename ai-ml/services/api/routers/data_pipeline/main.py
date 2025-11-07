"""Main Data Pipeline API Router"""

import logging
from fastapi import APIRouter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import sub-routers
from services.api.routers.data_pipeline import ingestion, status, results

# Create main router
router = APIRouter(
    prefix="/api/v1/data",
    tags=["Data Pipeline"]
)

# Include sub-routers
router.include_router(ingestion.router)
router.include_router(status.router)
router.include_router(results.router)

logger.info("Data Pipeline API routers registered successfully")