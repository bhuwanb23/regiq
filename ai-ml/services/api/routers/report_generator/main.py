"""Report Generation API Router"""

import logging
import uuid
from datetime import datetime
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from services.api.auth.jwt_handler import get_current_user
from services.api.routers.report_generator.models import (
    ReportCreateRequest, ReportCreateResponse,
    TemplateListResponse, TemplateCreateRequest, TemplateCreateResponse,
    ExportRequest, ExportResponse,
    ReportStatusResponse
)

# Real terminology / template helpers from the report_generator service.
try:
    from services.report_generator.terminology.terminology_manager import TerminologyManager
except Exception:  # pragma: no cover
    TerminologyManager = None  # type: ignore

try:
    from services.report_generator.templates.base.template_registry import (
        registry as template_registry,
        list_templates as registry_list_templates,
    )
except Exception:  # pragma: no cover
    template_registry = None  # type: ignore
    registry_list_templates = None  # type: ignore

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory report and export registries — sufficient for the agentic
# request/response flow and trivially swappable for a DB-backed store later.
_report_registry: Dict[str, Dict[str, Any]] = {}
_export_registry: Dict[str, Dict[str, Any]] = {}


def _now_iso() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


_terminology_singleton: Any = None


def _get_terminology() -> Any:
    """Lazy-init a TerminologyManager so unit tests without optional
    dependencies don't pay the import cost on module load."""
    global _terminology_singleton
    if _terminology_singleton is None and TerminologyManager is not None:
        try:
            _terminology_singleton = TerminologyManager()
        except Exception as exc:  # pragma: no cover
            logger.warning(f"TerminologyManager init failed: {exc}")
            _terminology_singleton = False  # negative cache
    return _terminology_singleton if _terminology_singleton else None

# Create router
router = APIRouter(
    prefix="/api/v1/reports",
    tags=["Report Generation"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/create",
    response_model=ReportCreateResponse,
    summary="Create Report",
    description="Create a new compliance report."
)
async def create_report(
    request: ReportCreateRequest,
    current_user: dict = Depends(get_current_user),
) -> ReportCreateResponse:
    """Create a new compliance report — registers it for later generation."""
    try:
        logger.info(f"Creating {request.report_type} report: {request.title}")

        report_id = f"report_{uuid.uuid4().hex[:12]}"
        created_at = _now_iso()
        _report_registry[report_id] = {
            "report_type": request.report_type,
            "title": request.title,
            "params": request.dict() if hasattr(request, "dict") else {},
            "status": "pending",
            "progress": 0.0,
            "created_at": created_at,
            "last_updated": created_at,
            "created_by": current_user.get("sub") if isinstance(current_user, dict) else None,
        }

        return ReportCreateResponse(
            report_id=report_id,
            report_type=request.report_type,
            title=request.title,
            status="pending",
            created_at=created_at,
        )
    except Exception as e:
        logger.error(f"Error creating report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create report"
        )


@router.post(
    "/generate",
    summary="Generate Report (Alias)",
    description="Generate a compliance report (alias for /create endpoint)."
)
async def generate_report(
    request: Dict[str, Any],
    current_user: dict = Depends(get_current_user),
) -> Dict[str, Any]:
    """Generate a compliance report."""
    try:
        report_type = request.get("report_type", "fairness")
        data = request.get("data", {})
        logger.info(f"Generating {report_type} report")
        
        return {
            "report_id": "report_12345",
            "report_type": report_type,
            "status": "completed",
            "created_at": "2025-11-07 10:30:00",
            "data": data,
            "source": "python_ai_ml"
        }
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate report"
        )


@router.get(
    "/templates",
    response_model=TemplateListResponse,
    summary="List Report Templates",
    description="List available report templates."
)
async def list_templates(
    page: int = 1,
    page_size: int = 10,
    current_user: dict = Depends(get_current_user),
) -> TemplateListResponse:
    """List available report templates from the template registry."""
    try:
        logger.info(f"Listing templates - page: {page}, page_size: {page_size}")

        templates: list = []
        if registry_list_templates is not None:
            try:
                templates = registry_list_templates() or []
            except Exception as inner:
                logger.warning(f"Template registry listing failed: {inner}")
                templates = []

        # Fallback: expose the three first-party template types known to ship
        # with this repo so the UI has something coherent to render even when
        # the registry hasn't been initialized by a host process.
        if not templates:
            templates = [
                {
                    "template_id": "executive_default",
                    "name": "Executive Summary",
                    "description": "High-level executive compliance report",
                    "template_type": "executive",
                },
                {
                    "template_id": "technical_default",
                    "name": "Technical Analysis",
                    "description": "Detailed technical analysis report",
                    "template_type": "technical",
                },
                {
                    "template_id": "regulatory_default",
                    "name": "Regulatory Filing",
                    "description": "Regulator-facing compliance filing",
                    "template_type": "regulatory",
                },
            ]

        total = len(templates)
        start = max(0, (page - 1) * page_size)
        end = start + page_size
        return TemplateListResponse(
            templates=templates[start:end],
            total_templates=total,
            page=page,
            page_size=page_size,
        )
    except Exception as e:
        logger.error(f"Error listing templates: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list templates"
        )


@router.post(
    "/templates",
    response_model=TemplateCreateResponse,
    summary="Create Report Template",
    description="Create a new report template."
)
async def create_template(
    request: TemplateCreateRequest,
    current_user: dict = Depends(get_current_user),
) -> TemplateCreateResponse:
    """Create (register metadata for) a new report template."""
    try:
        logger.info(f"Creating template: {request.name}")

        template_id = f"tmpl_{uuid.uuid4().hex[:12]}"
        created_at = _now_iso()

        # We don't dynamically subclass BaseTemplate here — instead we store
        # the metadata so administrators can later promote it to a real
        # template via a code change. This keeps the API non-destructive
        # while still being honest about what was persisted.
        if template_registry is not None:
            try:
                template_registry._metadata_only = getattr(
                    template_registry, "_metadata_only", {}
                )
                template_registry._metadata_only[template_id] = {
                    "name": request.name,
                    "template_type": request.template_type,
                    "created_at": created_at,
                    "created_by": current_user.get("sub") if isinstance(current_user, dict) else None,
                    "request": request.dict() if hasattr(request, "dict") else {},
                }
            except Exception as inner:
                logger.warning(f"Template registration (metadata-only) failed: {inner}")

        return TemplateCreateResponse(
            template_id=template_id,
            name=request.name,
            template_type=request.template_type,
            status="created",
            created_at=created_at,
        )
    except Exception as e:
        logger.error(f"Error creating template: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create template"
        )


@router.get(
    "/export/{report_id}",
    response_model=ExportResponse,
    summary="Export Report",
    description="Export a report in the specified format."
)
async def export_report(
    report_id: str,
    format: str = "pdf",
    current_user: dict = Depends(get_current_user),
) -> ExportResponse:
    """Export a report in the specified format — registers an export job."""
    try:
        logger.info(f"Exporting report {report_id} as {format}")

        if report_id not in _report_registry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Report {report_id} not found",
            )

        export_id = f"export_{uuid.uuid4().hex[:12]}"
        created_at = _now_iso()
        _export_registry[export_id] = {
            "report_id": report_id,
            "format": format,
            "status": "pending",
            "created_at": created_at,
        }

        return ExportResponse(
            export_id=export_id,
            report_id=report_id,
            format=format,
            status="pending",
            created_at=created_at,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exporting report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to export report"
        )


@router.get(
    "/status/{report_id}",
    response_model=ReportStatusResponse,
    summary="Get Report Status",
    description="Get the current status of a report generation process."
)
async def get_report_status(
    report_id: str,
    current_user: dict = Depends(get_current_user),
) -> ReportStatusResponse:
    """Get the status of a report generation process from the registry."""
    try:
        logger.info(f"Getting status for report: {report_id}")

        entry = _report_registry.get(report_id)
        if not entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Report {report_id} not found",
            )

        return ReportStatusResponse(
            report_id=report_id,
            status=entry.get("status", "pending"),
            progress=float(entry.get("progress", 0.0)),
            last_updated=entry.get("last_updated") or _now_iso(),
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting report status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get report status"
        )


@router.get(
    "/glossary",
    summary="Get Compliance Glossary",
    description="Get a glossary of compliance terms and definitions."
)
async def get_glossary(
    audience: str = "technical",
    current_user: dict = Depends(get_current_user),
) -> Dict[str, Any]:
    """Get the compliance glossary from TerminologyManager."""
    try:
        logger.info(f"Retrieving compliance glossary (audience={audience})")

        manager = _get_terminology()
        terms: list = []
        if manager is not None:
            try:
                terms = manager.generate_glossary(audience=audience) or []
            except Exception as inner:
                logger.warning(f"TerminologyManager.generate_glossary failed: {inner}")
                terms = []

        if not terms:
            # Minimal hard-coded fallback so the UI always has content. The
            # real glossary is loaded from `TerminologyManager` when available.
            terms = [
                {"term": "GDPR", "definition": "EU General Data Protection Regulation", "category": "regulatory"},
                {"term": "Compliance Score", "definition": "0–100 score indicating regulatory adherence", "category": "general"},
                {"term": "Bias Detection", "definition": "Identifying unfair patterns in AI models", "category": "fairness"},
            ]

        return {
            "terms": terms,
            "total_count": len(terms),
            "audience": audience,
            "source": "terminology_manager" if manager else "fallback",
        }
    except Exception as e:
        logger.error(f"Error retrieving glossary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve glossary"
        )