#!/usr/bin/env python3
"""
REGIQ AI/ML - Export Engine
Chart and dashboard export system.
"""

import io
import os
import sys
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import base64

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

# Optional rendering backends. We try matplotlib first (the most common
# install), then Pillow as a last-resort raster fallback. PDF generation
# uses matplotlib's PdfPages when available, otherwise ReportLab.
try:
    import matplotlib
    matplotlib.use("Agg")  # ensure headless mode
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    MATPLOTLIB_AVAILABLE = True
except Exception:  # pragma: no cover
    MATPLOTLIB_AVAILABLE = False

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except Exception:  # pragma: no cover
    PIL_AVAILABLE = False

try:
    from reportlab.pdfgen import canvas as rl_canvas
    from reportlab.lib.pagesizes import letter
    REPORTLAB_AVAILABLE = True
except Exception:  # pragma: no cover
    REPORTLAB_AVAILABLE = False

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class ExportConfig:
    """Export configuration."""
    export_id: str
    format: str  # png, svg, pdf, json
    width: int = 800
    height: int = 600
    quality: int = 100
    background_color: str = "#FFFFFF"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


class ExportEngine:
    """
    Chart and dashboard export engine.
    
    Provides export capabilities for visualizations in multiple formats.
    """
    
    def __init__(self):
        """Initialize export engine."""
        self.logger = logging.getLogger(__name__)
        self.supported_formats = ["png", "svg", "pdf", "json"]
        
        self.logger.info("Export engine initialized")
    
    def export_chart(self, chart_spec: Dict[str, Any], config: ExportConfig) -> Dict[str, Any]:
        """
        Export chart to specified format.
        
        Args:
            chart_spec: Chart specification
            config: Export configuration
            
        Returns:
            Export result
        """
        try:
            if config.format not in self.supported_formats:
                raise ValueError(f"Unsupported format: {config.format}")
            
            if config.format == "json":
                return self._export_json(chart_spec, config)
            elif config.format == "svg":
                return self._export_svg(chart_spec, config)
            elif config.format == "png":
                return self._export_png(chart_spec, config)
            elif config.format == "pdf":
                return self._export_pdf(chart_spec, config)
            
        except Exception as e:
            self.logger.error(f"Export failed: {str(e)}")
            return {"error": str(e)}
    
    def _export_json(self, chart_spec: Dict[str, Any], config: ExportConfig) -> Dict[str, Any]:
        """Export as JSON."""
        return {
            "format": "json",
            "data": json.dumps(chart_spec, indent=2),
            "size": len(json.dumps(chart_spec)),
            "exported_at": datetime.utcnow().isoformat()
        }
    
    def _export_svg(self, chart_spec: Dict[str, Any], config: ExportConfig) -> Dict[str, Any]:
        """Export as SVG (mock implementation)."""
        # This would integrate with actual SVG generation library
        svg_content = f"""
        <svg width="{config.width}" height="{config.height}" xmlns="http://www.w3.org/2000/svg">
            <rect width="100%" height="100%" fill="{config.background_color}"/>
            <text x="50%" y="50%" text-anchor="middle" dy=".3em">
                {chart_spec.get('title', 'Chart')}
            </text>
        </svg>
        """
        
        return {
            "format": "svg",
            "data": svg_content.strip(),
            "size": len(svg_content),
            "exported_at": datetime.utcnow().isoformat()
        }
    
    def _export_png(self, chart_spec: Dict[str, Any], config: ExportConfig) -> Dict[str, Any]:
        """Render the chart spec to a real PNG and return it base64-encoded."""
        if MATPLOTLIB_AVAILABLE:
            buf = self._render_with_matplotlib(chart_spec, config, image_format="png")
            if buf is not None:
                return {
                    "format": "png",
                    "data": base64.b64encode(buf).decode("ascii"),
                    "encoding": "base64",
                    "width": config.width,
                    "height": config.height,
                    "exported_at": datetime.utcnow().isoformat(),
                    "renderer": "matplotlib",
                }

        if PIL_AVAILABLE:
            buf = self._render_with_pil(chart_spec, config)
            if buf is not None:
                return {
                    "format": "png",
                    "data": base64.b64encode(buf).decode("ascii"),
                    "encoding": "base64",
                    "width": config.width,
                    "height": config.height,
                    "exported_at": datetime.utcnow().isoformat(),
                    "renderer": "pillow",
                }

        # Final degraded fallback — a 1x1 transparent PNG so downstream
        # consumers always get a valid image they can render.
        transparent_1x1 = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
        )
        return {
            "format": "png",
            "data": base64.b64encode(transparent_1x1).decode("ascii"),
            "encoding": "base64",
            "width": config.width,
            "height": config.height,
            "exported_at": datetime.utcnow().isoformat(),
            "renderer": "fallback",
            "warning": "No PNG renderer (matplotlib/Pillow) installed",
        }

    def _export_pdf(self, chart_spec: Dict[str, Any], config: ExportConfig) -> Dict[str, Any]:
        """Render the chart spec to a real PDF and return it base64-encoded."""
        if MATPLOTLIB_AVAILABLE:
            buf = self._render_pdf_with_matplotlib(chart_spec, config)
            if buf is not None:
                return {
                    "format": "pdf",
                    "data": base64.b64encode(buf).decode("ascii"),
                    "encoding": "base64",
                    "exported_at": datetime.utcnow().isoformat(),
                    "renderer": "matplotlib",
                }

        if REPORTLAB_AVAILABLE:
            buf = self._render_pdf_with_reportlab(chart_spec, config)
            if buf is not None:
                return {
                    "format": "pdf",
                    "data": base64.b64encode(buf).decode("ascii"),
                    "encoding": "base64",
                    "exported_at": datetime.utcnow().isoformat(),
                    "renderer": "reportlab",
                }

        # Minimal valid PDF stub — a 1-page empty document; ensures clients
        # can still open the file even when no renderer is available.
        minimal_pdf = (
            b"%PDF-1.4\n"
            b"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
            b"2 0 obj<</Type/Pages/Count 1/Kids[3 0 R]>>endobj\n"
            b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]>>endobj\n"
            b"xref\n0 4\n0000000000 65535 f \n0000000010 00000 n \n0000000053 00000 n \n0000000094 00000 n \n"
            b"trailer<</Size 4/Root 1 0 R>>\nstartxref\n150\n%%EOF"
        )
        return {
            "format": "pdf",
            "data": base64.b64encode(minimal_pdf).decode("ascii"),
            "encoding": "base64",
            "exported_at": datetime.utcnow().isoformat(),
            "renderer": "fallback",
            "warning": "No PDF renderer (matplotlib/ReportLab) installed",
        }

    # --------------------------------------------------------------------- #
    # Rendering helpers                                                     #
    # --------------------------------------------------------------------- #
    def _build_matplotlib_figure(self, chart_spec: Dict[str, Any], config: ExportConfig):
        """Translate a generic chart_spec dict into a matplotlib Figure.

        Supports a small set of common chart kinds (bar, line, pie). For
        unrecognized shapes we render a labeled text card so the output
        still carries the spec's title.
        """
        chart_type = (chart_spec.get("type") or chart_spec.get("chart_type") or "bar").lower()
        title = chart_spec.get("title", "Chart")
        data = chart_spec.get("data") or chart_spec.get("series") or {}

        fig = plt.figure(
            figsize=(config.width / 100, config.height / 100),
            dpi=100,
            facecolor=config.background_color,
        )
        ax = fig.add_subplot(111)

        try:
            if chart_type == "bar" and isinstance(data, dict):
                labels = list(data.keys())
                values = [float(v) for v in data.values()]
                ax.bar(labels, values)
            elif chart_type == "line" and isinstance(data, dict):
                labels = list(data.keys())
                values = [float(v) for v in data.values()]
                ax.plot(labels, values, marker="o")
            elif chart_type == "pie" and isinstance(data, dict):
                ax.pie(
                    [float(v) for v in data.values()],
                    labels=list(data.keys()),
                    autopct="%1.1f%%",
                )
            else:
                ax.axis("off")
                ax.text(
                    0.5, 0.5,
                    json.dumps(data, default=str)[:500] or "(no data)",
                    ha="center", va="center", wrap=True,
                )
        except Exception as exc:
            ax.clear()
            ax.axis("off")
            ax.text(0.5, 0.5, f"Render error: {exc}", ha="center", va="center")

        ax.set_title(title)
        fig.tight_layout()
        return fig

    def _render_with_matplotlib(
        self, chart_spec: Dict[str, Any], config: ExportConfig, image_format: str = "png"
    ) -> Optional[bytes]:
        try:
            fig = self._build_matplotlib_figure(chart_spec, config)
            buf = io.BytesIO()
            fig.savefig(buf, format=image_format, facecolor=fig.get_facecolor())
            plt.close(fig)
            return buf.getvalue()
        except Exception as exc:
            self.logger.error(f"matplotlib PNG rendering failed: {exc}")
            return None

    def _render_pdf_with_matplotlib(
        self, chart_spec: Dict[str, Any], config: ExportConfig
    ) -> Optional[bytes]:
        try:
            fig = self._build_matplotlib_figure(chart_spec, config)
            buf = io.BytesIO()
            with PdfPages(buf) as pdf:
                pdf.savefig(fig, facecolor=fig.get_facecolor())
            plt.close(fig)
            return buf.getvalue()
        except Exception as exc:
            self.logger.error(f"matplotlib PDF rendering failed: {exc}")
            return None

    def _render_with_pil(self, chart_spec: Dict[str, Any], config: ExportConfig) -> Optional[bytes]:
        """Render a simple labeled card using Pillow as a fallback."""
        try:
            img = Image.new("RGB", (config.width, config.height), config.background_color)
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.load_default()
            except Exception:
                font = None

            title = chart_spec.get("title", "Chart")
            draw.text((20, 20), title, fill="#111111", font=font)

            data = chart_spec.get("data") or chart_spec.get("series") or {}
            if isinstance(data, dict) and data:
                y = 60
                max_val = max((float(v) for v in data.values() if isinstance(v, (int, float))), default=1.0) or 1.0
                bar_width = max(10, (config.width - 60) // max(1, len(data)))
                for i, (label, value) in enumerate(data.items()):
                    try:
                        v = float(value)
                    except (TypeError, ValueError):
                        v = 0.0
                    height = int((config.height - 120) * (v / max_val))
                    x0 = 20 + i * bar_width
                    x1 = x0 + bar_width - 4
                    y1 = config.height - 40
                    y0 = y1 - height
                    draw.rectangle([x0, y0, x1, y1], fill="#3B82F6")
                    draw.text((x0, y1 + 4), str(label)[:8], fill="#111111", font=font)
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            return buf.getvalue()
        except Exception as exc:
            self.logger.error(f"Pillow rendering failed: {exc}")
            return None

    def _render_pdf_with_reportlab(
        self, chart_spec: Dict[str, Any], config: ExportConfig
    ) -> Optional[bytes]:
        try:
            buf = io.BytesIO()
            c = rl_canvas.Canvas(buf, pagesize=letter)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(72, 720, str(chart_spec.get("title", "Chart")))
            c.setFont("Helvetica", 10)
            payload = json.dumps(chart_spec, indent=2, default=str)
            y = 690
            for line in payload.splitlines()[:60]:
                c.drawString(72, y, line[:90])
                y -= 12
                if y < 72:
                    break
            c.showPage()
            c.save()
            return buf.getvalue()
        except Exception as exc:
            self.logger.error(f"ReportLab rendering failed: {exc}")
            return None
    
    def get_supported_formats(self) -> List[str]:
        """Get supported export formats."""
        return self.supported_formats.copy()
    
    def __str__(self) -> str:
        """String representation."""
        return f"ExportEngine({len(self.supported_formats)} formats)"
