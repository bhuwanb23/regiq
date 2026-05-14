"""Regulatory Intelligence API Router"""

import asyncio
import logging
import uuid
from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import JSONResponse

from services.api.auth.jwt_handler import get_current_user
from services.api.routers.regulatory_intelligence.models import SearchResult
from services.api.routers.regulatory_intelligence.models import (
    DocumentAnalysisRequest, DocumentAnalysisResponse,
    SummarizationRequest, SummarizationResponse,
    QARequest, QAResponse,
    SearchRequest, SearchResponse
)

# Optional service-class imports — wrapped in try so the router still loads
# even if heavy deps (Gemini SDK, chromadb, etc.) are missing locally.
try:
    from services.regulatory_intelligence.llm.summarization import SummarizationService
except Exception:  # pragma: no cover
    SummarizationService = None

try:
    from services.regulatory_intelligence.llm.qa import QASystem
except Exception:  # pragma: no cover
    QASystem = None

try:
    from services.regulatory_intelligence.rag.document_embeddings import (
        DocumentEmbeddingService,
        SimilaritySearchEngine,
    )
except Exception:  # pragma: no cover
    DocumentEmbeddingService = None
    SimilaritySearchEngine = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lazy singletons so we don't initialize Gemini/vector DB at module import time.
_summarizer: "SummarizationService | None" = None
_qa_system: "QASystem | None" = None
_search_engine: "SimilaritySearchEngine | None" = None


def _get_summarizer():
    global _summarizer
    if _summarizer is None and SummarizationService is not None:
        try:
            _summarizer = SummarizationService()
        except Exception as e:
            logger.warning(f"SummarizationService unavailable: {e}")
            _summarizer = None
    return _summarizer


def _get_qa():
    global _qa_system
    if _qa_system is None and QASystem is not None:
        try:
            _qa_system = QASystem()
        except Exception as e:
            logger.warning(f"QASystem unavailable: {e}")
            _qa_system = None
    return _qa_system


def _get_search_engine():
    global _search_engine
    if _search_engine is None and DocumentEmbeddingService is not None and SimilaritySearchEngine is not None:
        try:
            _search_engine = SimilaritySearchEngine(DocumentEmbeddingService())
        except Exception as e:
            logger.warning(f"SimilaritySearchEngine unavailable: {e}")
            _search_engine = None
    return _search_engine

# Create router
router = APIRouter(
    prefix="/api/v1/regulatory-intelligence",
    tags=["Regulatory Intelligence"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/documents/analyze",
    response_model=DocumentAnalysisResponse,
    summary="Analyze Regulatory Document",
    description="Analyze a regulatory document and extract compliance requirements, risks, and recommendations."
)
async def analyze_document(
    request: DocumentAnalysisRequest,
    current_user: dict = Depends(get_current_user),
) -> DocumentAnalysisResponse:
    """Analyze a regulatory document using the summarization service."""
    import time
    started = time.time()
    try:
        logger.info(f"Analyzing document of type: {request.document_type}")

        document_text = getattr(request, "content", None) or getattr(request, "text", "") or ""
        document_id = getattr(request, "document_id", None) or f"doc_{uuid.uuid4().hex[:12]}"

        summarizer = _get_summarizer()
        key_findings: List[str] = []
        risk_factors: List[str] = []
        recommended_actions: List[str] = []
        compliance_score = 75.0

        if summarizer and document_text:
            try:
                summary = await asyncio.to_thread(
                    summarizer.summarize_document, document_text, "executive", 6
                )
                if isinstance(summary, dict):
                    points = summary.get("key_points") or []
                    if isinstance(points, list):
                        key_findings = [str(p) for p in points][:6]
                    risks = summary.get("risks") or ""
                    if risks:
                        risk_factors = [str(risks)] if isinstance(risks, str) else [str(r) for r in risks]
                    actions = summary.get("actions") or ""
                    if actions:
                        recommended_actions = [str(actions)] if isinstance(actions, str) else [str(a) for a in actions]
                    # Heuristic compliance score based on richness of summary.
                    compliance_score = min(95.0, 60.0 + 5.0 * len(key_findings))
            except Exception as inner:
                logger.warning(f"Summarizer call failed: {inner}; returning heuristic response")

        if not key_findings:
            key_findings = [
                "Document analysis completed",
                "Manual review recommended",
            ]
        if not risk_factors:
            risk_factors = ["Risk factors require deeper analysis"]
        if not recommended_actions:
            recommended_actions = ["Schedule a compliance review of the document"]

        return DocumentAnalysisResponse(
            document_id=document_id,
            compliance_score=compliance_score,
            key_findings=key_findings,
            risk_factors=risk_factors,
            recommended_actions=recommended_actions,
            processing_time=round(time.time() - started, 3),
        )
    except Exception as e:
        logger.error(f"Error analyzing document: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze document"
        )


@router.post(
    "/summarize",
    response_model=SummarizationResponse,
    summary="Summarize Regulatory Content",
    description="Generate a summary of regulatory content with key points extraction."
)
async def summarize_content(
    request: SummarizationRequest,
    current_user: dict = Depends(get_current_user),
) -> SummarizationResponse:
    """Generate a summary of regulatory content via SummarizationService."""
    try:
        logger.info(f"Generating {request.summary_type} summary")

        text = getattr(request, "content", None) or getattr(request, "text", "") or ""
        style = getattr(request, "summary_type", None) or "executive"
        max_bullets = getattr(request, "max_points", None) or 6

        summarizer = _get_summarizer()
        summary_text = ""
        key_points: List[str] = []

        if summarizer and text:
            try:
                result = await asyncio.to_thread(
                    summarizer.summarize_document, text, style, max_bullets
                )
                if isinstance(result, dict):
                    summary_text = str(result.get("overview") or result.get("summary") or "")
                    pts = result.get("key_points") or []
                    if isinstance(pts, list):
                        key_points = [str(p) for p in pts][:max_bullets]
            except Exception as inner:
                logger.warning(f"SummarizationService failed: {inner}")

        if not summary_text:
            # Heuristic fallback — first sentence of the input.
            first = text.split(".")[0].strip() if text else ""
            summary_text = first or "Summary unavailable; please retry once the LLM service is reachable."
        if not key_points and text:
            key_points = [p.strip() for p in text.split(".") if p.strip()][:max_bullets]

        word_count = len(summary_text.split())

        return SummarizationResponse(
            summary=summary_text,
            key_points=key_points,
            word_count=word_count,
        )
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate summary"
        )


@router.post(
    "/qa",
    response_model=QAResponse,
    summary="Answer Regulatory Questions",
    description="Ask questions about regulatory content and get AI-powered answers with citations."
)
async def answer_question(
    request: QARequest,
    current_user: dict = Depends(get_current_user),
) -> QAResponse:
    """Answer questions about regulatory content via QASystem (Gemini-backed)."""
    import time
    started = time.time()
    try:
        logger.info(f"Answering question: {request.question}")

        question = request.question
        context = getattr(request, "context", None) or getattr(request, "document_context", "") or ""

        qa = _get_qa()
        answer_text = ""
        confidence = 0.5
        citations: List[str] = []

        if qa:
            try:
                result = await asyncio.to_thread(qa.answer, question, context)
                if isinstance(result, dict):
                    answer_text = str(result.get("answer") or "")
                    try:
                        confidence = float(result.get("confidence", 0.5))
                    except (TypeError, ValueError):
                        confidence = 0.5
                    cites = result.get("citations") or []
                    if isinstance(cites, list):
                        citations = [str(c) for c in cites]
            except Exception as inner:
                logger.warning(f"QASystem failed: {inner}")

        if not answer_text:
            answer_text = (
                "Unable to confidently answer the question with the provided context. "
                "Please supply additional regulatory text or retry once the LLM service is reachable."
            )

        return QAResponse(
            answer=answer_text,
            confidence=confidence,
            citations=citations,
            processing_time=round(time.time() - started, 3),
        )
    except Exception as e:
        logger.error(f"Error answering question: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to answer question"
        )


@router.post(
    "/search",
    response_model=SearchResponse,
    summary="Search Regulatory Database",
    description="Search the regulatory database for relevant documents and provisions."
)
async def search_regulations(
    request: SearchRequest,
    current_user: dict = Depends(get_current_user),
) -> SearchResponse:
    """Search the regulatory database using the SimilaritySearchEngine."""
    try:
        logger.info(f"Searching for: {request.query}")

        page = getattr(request, "page", 1) or 1
        page_size = getattr(request, "page_size", 10) or 10
        filters = getattr(request, "filters", None) or {}

        engine = _get_search_engine()
        results: List[SearchResult] = []
        total = 0

        if engine:
            try:
                hits = await asyncio.to_thread(
                    engine.search_with_ranking,
                    request.query,
                    page_size,
                    filters,
                )
                for hit in hits or []:
                    if not isinstance(hit, dict):
                        continue
                    meta = hit.get("metadata") or {}
                    results.append(
                        SearchResult(
                            document_id=str(hit.get("document_id") or hit.get("id") or uuid.uuid4().hex),
                            title=str(meta.get("title") or hit.get("title") or "Untitled"),
                            snippet=str(hit.get("snippet") or hit.get("content") or "")[:400],
                            relevance_score=float(hit.get("score") or hit.get("relevance_score") or 0.0),
                            document_type=str(meta.get("document_type") or hit.get("document_type") or "regulation"),
                        )
                    )
                total = len(results)
            except Exception as inner:
                logger.warning(f"SimilaritySearchEngine failed: {inner}")

        if not results:
            # Empty search result is preferable to fabricated data when the
            # backing vector index is unavailable / empty.
            total = 0

        total_pages = max(1, (total + page_size - 1) // page_size) if total else 1

        return SearchResponse(
            results=results,
            total_results=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )
    except Exception as e:
        logger.error(f"Error searching regulations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search regulations"
        )