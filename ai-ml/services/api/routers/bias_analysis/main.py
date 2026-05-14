"""Bias Analysis API Router"""

import asyncio
import logging
import uuid
from datetime import datetime
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import JSONResponse

from services.api.auth.jwt_handler import get_current_user
from services.api.routers.bias_analysis.models import (
    ModelUploadRequest, ModelMetadataResponse,
    AnalysisTriggerRequest, AnalysisJobResponse,
    BiasMetricsResponse,
    ReportGenerationRequest, ReportGenerationResponse
)

# Optional imports of the real bias-analysis service classes. These all rely
# on numpy/pandas and may not be importable in every environment, so we wrap
# them defensively.
try:
    from services.bias_analysis.metrics.demographic_parity import DemographicParityAnalyzer
except Exception:  # pragma: no cover
    DemographicParityAnalyzer = None

try:
    from services.bias_analysis.metrics.equalized_odds import EqualizedOddsAnalyzer
except Exception:  # pragma: no cover
    EqualizedOddsAnalyzer = None

try:
    from services.bias_analysis.visualization.bias_visualizer import BiasVisualizer
except Exception:  # pragma: no cover
    BiasVisualizer = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory registries for uploaded models and analysis jobs so the
# upload → analyze → results flow is consistent across requests.
_model_registry: Dict[str, Dict[str, Any]] = {}
_analysis_registry: Dict[str, Dict[str, Any]] = {}


def _now_iso() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def _compute_real_bias_metrics(y_true, y_pred, protected_attribute) -> Dict[str, Any]:
    """Run the real bias metrics if numpy/sklearn are available. Returns dict."""
    metrics: Dict[str, Any] = {}
    if DemographicParityAnalyzer is not None:
        try:
            dp = DemographicParityAnalyzer().calculate_demographic_parity(
                y_true, y_pred, protected_attribute
            )
            metrics["demographic_parity"] = {
                "parity_score": dp.parity_score,
                "max_difference": dp.max_difference,
                "positive_rates": dp.positive_rates,
                "threshold_violation": dp.threshold_violation,
                "recommendations": dp.recommendations,
            }
        except Exception as e:
            metrics["demographic_parity_error"] = str(e)
    if EqualizedOddsAnalyzer is not None:
        try:
            eo = EqualizedOddsAnalyzer().calculate_equalized_odds(
                y_true, y_pred, protected_attribute
            )
            metrics["equalized_odds"] = {
                "equalized_odds_score": getattr(eo, "equalized_odds_score", None),
                "tpr_difference": getattr(eo, "tpr_difference", None),
                "fpr_difference": getattr(eo, "fpr_difference", None),
                "threshold_violation": getattr(eo, "threshold_violation", None),
            }
        except Exception as e:
            metrics["equalized_odds_error"] = str(e)
    return metrics

# Create router
router = APIRouter(
    prefix="/api/v1/bias-analysis",
    tags=["Bias Analysis"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/models/upload",
    response_model=ModelMetadataResponse,
    summary="Upload ML Model",
    description="Upload a machine learning model for bias analysis."
)
async def upload_model(
    model_file: UploadFile = File(...),
    model_name: str = Form(...),
    description: str = Form(""),
    target_variable: str = Form(...),
    protected_attributes: str = Form(...),
    current_user: dict = Depends(get_current_user),
) -> ModelMetadataResponse:
    """Upload a machine learning model and register it for later analysis."""
    try:
        logger.info(f"Uploading model: {model_name}")

        import json
        try:
            protected_attrs = json.loads(protected_attributes)
            if not isinstance(protected_attrs, list):
                protected_attrs = [protected_attrs]
        except json.JSONDecodeError:
            protected_attrs = [protected_attributes]

        # Read the file to record its size; we don't persist the binary here,
        # only its metadata. A production implementation would push it to
        # blob storage and store the path in the registry.
        contents = await model_file.read()
        file_size = len(contents)

        model_id = f"model_{uuid.uuid4().hex[:12]}"
        upload_date = _now_iso()

        _model_registry[model_id] = {
            "name": model_name,
            "filename": model_file.filename,
            "content_type": model_file.content_type,
            "size": file_size,
            "description": description,
            "target_variable": target_variable,
            "protected_attributes": protected_attrs,
            "uploaded_by": current_user.get("sub") if isinstance(current_user, dict) else None,
            "uploaded_at": upload_date,
            "status": "uploaded",
        }

        return ModelMetadataResponse(
            model_id=model_id,
            name=model_name,
            model_type="sklearn",
            framework="scikit-learn",
            version="1.0.0",
            upload_date=upload_date,
            file_size=file_size,
            description=description,
            target_variable=target_variable,
            feature_columns=[],
            protected_attributes=protected_attrs,
            training_data_size=0,
            performance_metrics={},
            bias_analysis_status="pending",
        )
    except Exception as e:
        logger.error(f"Error uploading model: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload model"
        )


@router.post(
    "/analyze",
    response_model=AnalysisJobResponse,
    summary="Trigger Bias Analysis",
    description="Trigger bias analysis for an uploaded model."
)
async def trigger_analysis(
    request: AnalysisTriggerRequest,
    current_user: dict = Depends(get_current_user),
) -> AnalysisJobResponse:
    """Trigger bias analysis for a model — records a job entry."""
    try:
        logger.info(f"Triggering analysis for model: {request.model_id}")

        if request.model_id not in _model_registry:
            # Accept ad-hoc models too — analytic clients shouldn't have to
            # do a separate upload step for synthetic test runs.
            _model_registry[request.model_id] = {
                "name": f"ad-hoc-{request.model_id}",
                "status": "uploaded",
                "uploaded_at": _now_iso(),
            }

        analysis_id = f"analysis_{uuid.uuid4().hex[:12]}"
        _analysis_registry[analysis_id] = {
            "model_id": request.model_id,
            "status": "running",
            "created_at": _now_iso(),
            "params": request.dict() if hasattr(request, "dict") else {},
        }

        return AnalysisJobResponse(
            analysis_id=analysis_id,
            model_id=request.model_id,
            status="running",
            created_at=_analysis_registry[analysis_id]["created_at"],
        )
    except Exception as e:
        logger.error(f"Error triggering analysis: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to trigger analysis"
        )


@router.get(
    "/results/{analysis_id}",
    response_model=BiasMetricsResponse,
    summary="Get Bias Analysis Results",
    description="Retrieve detailed bias analysis results."
)
async def get_analysis_results(
    analysis_id: str,
    current_user: dict = Depends(get_current_user),
) -> BiasMetricsResponse:
    """Get bias analysis results from the in-memory registry."""
    try:
        logger.info(f"Retrieving results for analysis: {analysis_id}")

        job = _analysis_registry.get(analysis_id)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Analysis {analysis_id} not found",
            )

        metrics = job.get("metrics") or {}
        dp = metrics.get("demographic_parity") or {}
        eo = metrics.get("equalized_odds") or {}

        return BiasMetricsResponse(
            analysis_id=analysis_id,
            demographic_parity_difference=dp.get("max_difference") or 0.0,
            equal_opportunity_difference=eo.get("tpr_difference") or 0.0,
            disparate_impact=dp.get("parity_score") or 0.0,
            statistical_parity_difference=dp.get("max_difference") or 0.0,
            consistency_score=dp.get("parity_score") or 0.0,
            feature_importance_bias=metrics.get("feature_importance_bias") or {},
            group_metrics=metrics.get("group_metrics") or (dp.get("positive_rates") or {}),
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving analysis results: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve analysis results"
        )


@router.post(
    "/reports/generate",
    response_model=ReportGenerationResponse,
    summary="Generate Bias Analysis Report",
    description="Generate a report for bias analysis results."
)
async def generate_report(
    request: ReportGenerationRequest,
    current_user: dict = Depends(get_current_user),
) -> ReportGenerationResponse:
    """Generate a bias analysis report."""
    try:
        logger.info(f"Generating report for analysis: {request.analysis_id}")
        
        # TODO: Implement actual report generation using bias_analysis service
        # This is a placeholder implementation
        response = ReportGenerationResponse(
            report_id="report_12345",
            analysis_id=request.analysis_id,
            status="pending",
            created_at="2025-11-07 10:30:00",
            format=request.format
        )
        
        return response
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate report"
        )


@router.post(
    "/score",
    summary="Get Bias Scores",
    description="Calculate bias scores and fairness metrics for a model."
)
async def get_bias_scores(
    request: Dict[str, Any],
    current_user: dict = Depends(get_current_user),
) -> Dict[str, Any]:
    """Compute fairness metrics from y_true, y_pred, and a protected attribute."""
    try:
        model_id = request.get("modelId") or request.get("model_id") or "unknown"
        logger.info(f"Calculating bias scores for model: {model_id}")

        y_true = request.get("y_true")
        y_pred = request.get("y_pred")
        protected = request.get("protected_attribute") or request.get("protected")

        real_metrics: Dict[str, Any] = {}
        if y_true is not None and y_pred is not None and protected is not None:
            real_metrics = await asyncio.to_thread(
                _compute_real_bias_metrics, y_true, y_pred, protected
            )

        # Derive a summary score (1 - max(parity_diff, eo_diff)).
        dp = real_metrics.get("demographic_parity") or {}
        eo = real_metrics.get("equalized_odds") or {}
        dp_diff = float(dp.get("max_difference") or 0.0)
        eo_diff = float(eo.get("tpr_difference") or 0.0)
        overall_score = max(0.0, 1.0 - max(dp_diff, eo_diff))

        return {
            "model_id": model_id,
            "demographic_parity": dp.get("parity_score"),
            "equalized_odds": eo.get("equalized_odds_score"),
            "overall_fairness_score": round(overall_score, 4),
            "fairness_metrics": real_metrics,
            "computed": bool(real_metrics),
            "source": "bias_analysis_service" if real_metrics else "fallback",
        }
    except Exception as e:
        logger.error(f"Error calculating bias scores: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to calculate bias scores"
        )


@router.post(
    "/explain",
    summary="Get Model Explanations (SHAP/LIME)",
    description="Generate SHAP and LIME explanations for model predictions."
)
async def get_explanation(
    request: Dict[str, Any],
    current_user: dict = Depends(get_current_user),
) -> Dict[str, Any]:
    """Get model explanations using SHAP or LIME."""
    try:
        analysis_id = request.get("analysis_id", "unknown")
        explainer_type = request.get("explainer_type", "shap")
        logger.info(f"Generating {explainer_type} explanation for analysis: {analysis_id}")
        
        # Return sample SHAP/LIME values
        if explainer_type.lower() == "shap":
            return {
                "analysis_id": analysis_id,
                "explainer_type": "shap",
                "shap_values": {
                    "feature_1": 0.15,
                    "feature_2": -0.08,
                    "feature_3": 0.23
                },
                "global_importance": {
                    "feature_1": 0.35,
                    "feature_2": 0.25,
                    "feature_3": 0.40
                }
            }
        else:  # lime
            return {
                "analysis_id": analysis_id,
                "explainer_type": "lime",
                "local_explanation": {
                    "prediction": 1,
                    "probabilities": [0.3, 0.7],
                    "features": {
                        "feature_1": {"weight": 0.2, "value": 0.5},
                        "feature_2": {"weight": -0.15, "value": 0.3}
                    }
                }
            }
    except Exception as e:
        logger.error(f"Error generating explanation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate explanation"
        )


@router.get(
    "/metrics",
    summary="Get Fairness Metrics",
    description="Retrieve comprehensive fairness metrics for an analysis."
)
async def get_fairness_metrics(
    analysis_id: str,
    current_user: dict = Depends(get_current_user),
) -> Dict[str, Any]:
    """Get fairness metrics for a specific analysis (from the registry)."""
    try:
        logger.info(f"Retrieving fairness metrics for analysis: {analysis_id}")

        job = _analysis_registry.get(analysis_id)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Analysis {analysis_id} not found",
            )

        metrics = job.get("metrics") or {}
        dp = metrics.get("demographic_parity") or {}
        eo = metrics.get("equalized_odds") or {}

        return {
            "analysis_id": analysis_id,
            "demographic_parity_difference": dp.get("max_difference"),
            "equal_opportunity_difference": eo.get("tpr_difference"),
            "statistical_parity_difference": dp.get("max_difference"),
            "consistency_score": dp.get("parity_score"),
            "overall_fairness_score": metrics.get("overall_fairness_score"),
            "metrics": metrics,
            "computed": bool(metrics),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving fairness metrics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve fairness metrics"
        )


@router.get(
    "/visualize",
    summary="Get Visualization Data",
    description="Generate data for bias visualization dashboards."
)
async def get_visualization_data(
    current_user: dict = Depends(get_current_user),
) -> Dict[str, Any]:
    """Get visualization data for bias analysis."""
    try:
        logger.info("Generating visualization data")
        
        return {
            "bias_distribution": {
                "labels": ["Low", "Medium", "High"],
                "values": [60, 30, 10]
            },
            "fairness_metrics_chart": {
                "metrics": ["Demographic Parity", "Equal Opportunity", "Disparate Impact"],
                "scores": [0.85, 0.82, 0.91]
            },
            "feature_bias_heatmap": {
                "features": ["feature_1", "feature_2", "feature_3"],
                "bias_scores": [0.02, 0.15, 0.08]
            }
        }
    except Exception as e:
        logger.error(f"Error generating visualization data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate visualization data"
        )