#!/usr/bin/env python3
"""
REGIQ AI/ML - Report Output Generator
Converts assembled report sections into PDF and HTML deliverables.

This module provides:
- HTML report rendering with REGIQ-branded styling
- PDF generation via WeasyPrint (with pdfkit fallback)
- JSON export for API consumers
- Inline chart/visualization embedding (base64)
- File-system and in-memory output modes

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

import os
import sys
import json
import base64
import logging
import hashlib
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

logger = logging.getLogger(__name__)

# ── Optional heavy dependencies ──────────────────────────────────────────── #
try:
    import weasyprint
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False

try:
    import pdfkit
    PDFKIT_AVAILABLE = True
except ImportError:
    PDFKIT_AVAILABLE = False


# ── REGIQ Report CSS ─────────────────────────────────────────────────────── #
REGIQ_CSS = """
/* REGIQ Compliance Report Stylesheet */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --primary:   #1E3A5F;
    --accent:    #2E86AB;
    --success:   #27AE60;
    --warning:   #F39C12;
    --danger:    #E74C3C;
    --light-bg:  #F8FAFC;
    --border:    #E2E8F0;
    --text:      #2D3748;
    --muted:     #718096;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: 'Inter', Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: var(--text);
    background: #fff;
}

/* ── Cover page ── */
.cover-page {
    page-break-after: always;
    text-align: center;
    padding: 80px 60px;
    background: var(--primary);
    color: #fff;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.cover-page h1  { font-size: 28pt; font-weight: 700; margin-bottom: 12px; }
.cover-page h2  { font-size: 16pt; font-weight: 400; opacity: 0.85; margin-bottom: 40px; }
.cover-meta     { font-size: 10pt; opacity: 0.7; line-height: 2; }
.cover-badge    {
    display: inline-block;
    background: var(--accent);
    padding: 6px 18px;
    border-radius: 20px;
    font-size: 9pt;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 30px;
}

/* ── TOC ── */
.toc { page-break-after: always; padding: 40px 60px; }
.toc h2 { color: var(--primary); font-size: 18pt; margin-bottom: 24px; border-bottom: 2px solid var(--accent); padding-bottom: 8px; }
.toc-entry { display: flex; justify-content: space-between; padding: 5px 0; border-bottom: 1px dotted var(--border); }
.toc-entry a { color: var(--primary); text-decoration: none; }

/* ── Page layout ── */
.report-page { padding: 40px 60px; }

/* ── Section headings ── */
h1 { font-size: 22pt; color: var(--primary); margin: 30px 0 16px; }
h2 { font-size: 16pt; color: var(--primary); margin: 24px 0 12px; padding-bottom: 6px; border-bottom: 2px solid var(--accent); }
h3 { font-size: 13pt; color: var(--primary); margin: 18px 0 8px; }
h4 { font-size: 11pt; color: var(--accent); margin: 14px 0 6px; }
p  { margin-bottom: 10px; }

/* ── Metric cards ── */
.metric-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin: 20px 0; }
.metric-card {
    background: var(--light-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px;
    text-align: center;
}
.metric-card .value { font-size: 22pt; font-weight: 700; color: var(--primary); }
.metric-card .label { font-size: 9pt; color: var(--muted); text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px; }
.metric-card.good   { border-left: 4px solid var(--success); }
.metric-card.warn   { border-left: 4px solid var(--warning); }
.metric-card.bad    { border-left: 4px solid var(--danger); }

/* ── Status badges ── */
.badge { display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 8.5pt; font-weight: 600; }
.badge-green  { background: #D4EDDA; color: #155724; }
.badge-yellow { background: #FFF3CD; color: #856404; }
.badge-red    { background: #F8D7DA; color: #721C24; }
.badge-blue   { background: #D1ECF1; color: #0C5460; }

/* ── Tables ── */
table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 10pt; }
thead { background: var(--primary); color: #fff; }
th    { padding: 10px 12px; text-align: left; font-weight: 600; }
td    { padding: 9px 12px; border-bottom: 1px solid var(--border); }
tr:nth-child(even) td { background: var(--light-bg); }

/* ── Alert boxes ── */
.alert { border-radius: 6px; padding: 12px 16px; margin: 14px 0; border-left: 4px solid; }
.alert-info    { background: #EBF8FF; border-color: var(--accent); }
.alert-success { background: #F0FFF4; border-color: var(--success); }
.alert-warning { background: #FFFBEB; border-color: var(--warning); }
.alert-danger  { background: #FFF5F5; border-color: var(--danger); }
.alert-title   { font-weight: 700; margin-bottom: 4px; }

/* ── Charts ── */
.chart-container { text-align: center; margin: 20px 0; }
.chart-container img { max-width: 100%; border: 1px solid var(--border); border-radius: 6px; }
.chart-caption { font-size: 9pt; color: var(--muted); margin-top: 6px; font-style: italic; }

/* ── Glossary ── */
.regiq-glossary { margin: 20px 0; }
.regiq-glossary-list dt { font-weight: 600; color: var(--primary); margin-top: 12px; }
.regiq-glossary-list dd { margin-left: 20px; color: var(--text); margin-bottom: 4px; }

/* ── Footer ── */
.report-footer {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 8px 60px;
    font-size: 8pt;
    color: var(--muted);
    border-top: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
}

/* ── Print / PDF ── */
@page { margin: 0.8in 0.7in; size: A4; }
@media print {
    .cover-page { min-height: 100vh; }
    h2 { page-break-before: auto; }
    table, .metric-card { page-break-inside: avoid; }
}
"""


class ReportOutputGenerator:
    """
    Converts assembled report content into deliverable formats.

    Supported outputs: HTML (full page), PDF, JSON.
    Charts/visualizations are embedded as base64 data URIs.
    """

    def __init__(self, output_dir: Optional[Union[str, Path]] = None):
        self.logger = logging.getLogger(__name__)
        self.output_dir = Path(output_dir) if output_dir else Path(tempfile.gettempdir()) / "regiq_reports"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"ReportOutputGenerator ready — output_dir={self.output_dir}")

    # ------------------------------------------------------------------ #
    # Public interface                                                     #
    # ------------------------------------------------------------------ #

    def generate(
        self,
        sections: List[Dict[str, Any]],
        metadata: Dict[str, Any],
        formats: Optional[List[str]] = None,
        glossary_html: Optional[str] = None,
        charts: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Generate report in one or more formats.

        Args:
            sections:     List of {section_id, title, content (HTML string), order}.
            metadata:     Report metadata (title, report_type, generated_at, …).
            formats:      List of desired formats: ['html', 'pdf', 'json']. Default: ['html'].
            glossary_html: Pre-rendered glossary HTML to append.
            charts:       List of {chart_id, title, image_data (base64), caption}.

        Returns:
            Dict with keys matching requested formats, each containing
            {'path': str, 'size_bytes': int, 'content': bytes/str}.
        """
        formats = formats or ["html"]
        report_id = self._make_report_id(metadata)

        # Build full HTML document
        html_doc = self._build_html_document(sections, metadata, glossary_html, charts)

        results: Dict[str, Any] = {"report_id": report_id, "generated_at": datetime.utcnow().isoformat()}

        for fmt in formats:
            try:
                if fmt == "html":
                    results["html"] = self._save_html(html_doc, report_id)
                elif fmt == "pdf":
                    results["pdf"] = self._save_pdf(html_doc, report_id)
                elif fmt == "json":
                    results["json"] = self._save_json(sections, metadata, report_id)
                else:
                    self.logger.warning(f"Unsupported format requested: {fmt}")
            except Exception as exc:
                self.logger.error(f"Failed to generate {fmt}: {exc}")
                results[fmt] = {"error": str(exc)}

        return results

    # ------------------------------------------------------------------ #
    # HTML                                                                 #
    # ------------------------------------------------------------------ #

    def _build_html_document(
        self,
        sections: List[Dict[str, Any]],
        metadata: Dict[str, Any],
        glossary_html: Optional[str],
        charts: Optional[List[Dict[str, Any]]],
    ) -> str:
        """Assemble a complete, self-contained HTML document."""
        title = metadata.get("title", "REGIQ Compliance Report")
        report_type = metadata.get("report_type", "Compliance Report")
        generated_at = metadata.get("generated_at", datetime.utcnow().strftime("%d %B %Y, %H:%M UTC"))
        organization = metadata.get("organization", "Financial Institution")
        confidentiality = metadata.get("confidentiality", "CONFIDENTIAL")

        cover = self._build_cover(title, report_type, generated_at, organization, confidentiality)
        toc = self._build_toc(sections, include_glossary=bool(glossary_html))
        body = self._build_body(sections, charts)
        glossary_section = (
            f'<div class="report-page" id="glossary"><h2>Glossary of Terms</h2>{glossary_html}</div>'
            if glossary_html else ""
        )
        footer = (
            f'<div class="report-footer">'
            f'<span>{organization} — {confidentiality}</span>'
            f'<span>REGIQ AI Compliance Platform | {generated_at}</span>'
            f'</div>'
        )

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{title}</title>
<style>{REGIQ_CSS}</style>
</head>
<body>
{cover}
{toc}
{body}
{glossary_section}
{footer}
</body>
</html>"""

    def _build_cover(
        self, title: str, report_type: str,
        generated_at: str, organization: str, confidentiality: str,
    ) -> str:
        return f"""
<div class="cover-page">
  <div class="cover-badge">REGIQ AI Compliance Platform</div>
  <h1>{title}</h1>
  <h2>{report_type}</h2>
  <div class="cover-meta">
    <div>Organization: {organization}</div>
    <div>Generated: {generated_at}</div>
    <div>Classification: {confidentiality}</div>
  </div>
</div>"""

    def _build_toc(self, sections: List[Dict[str, Any]], include_glossary: bool) -> str:
        entries = sorted(sections, key=lambda s: s.get("order", 0))
        rows = "".join(
            f'<div class="toc-entry"><a href="#{s["section_id"]}">{s.get("title","Section")}</a><span></span></div>'
            for s in entries
        )
        if include_glossary:
            rows += '<div class="toc-entry"><a href="#glossary">Glossary of Terms</a><span></span></div>'
        return f'<div class="toc"><h2>Table of Contents</h2>{rows}</div>'

    def _build_body(
        self,
        sections: List[Dict[str, Any]],
        charts: Optional[List[Dict[str, Any]]],
    ) -> str:
        chart_map: Dict[str, Dict] = {c["chart_id"]: c for c in (charts or [])}
        parts = []
        for section in sorted(sections, key=lambda s: s.get("order", 0)):
            sid = section.get("section_id", "section")
            title = section.get("title", "")
            content = section.get("content", "")

            # Embed any charts tagged for this section
            chart_html = ""
            for chart in chart_map.values():
                if chart.get("section_id") == sid and chart.get("image_data"):
                    caption = chart.get("caption", chart.get("title", ""))
                    chart_html += (
                        f'<div class="chart-container">'
                        f'<img src="data:image/png;base64,{chart["image_data"]}" alt="{caption}"/>'
                        f'<div class="chart-caption">{caption}</div>'
                        f'</div>'
                    )

            parts.append(
                f'<div class="report-page" id="{sid}">'
                f'<h2>{title}</h2>'
                f'{content}'
                f'{chart_html}'
                f'</div>'
            )
        return "\n".join(parts)

    def _save_html(self, html_doc: str, report_id: str) -> Dict[str, Any]:
        path = self.output_dir / f"{report_id}.html"
        path.write_text(html_doc, encoding="utf-8")
        self.logger.info(f"HTML report saved: {path}")
        return {"path": str(path), "size_bytes": path.stat().st_size, "content": html_doc}

    # ------------------------------------------------------------------ #
    # PDF                                                                  #
    # ------------------------------------------------------------------ #

    def _save_pdf(self, html_doc: str, report_id: str) -> Dict[str, Any]:
        path = self.output_dir / f"{report_id}.pdf"

        if WEASYPRINT_AVAILABLE:
            weasyprint.HTML(string=html_doc).write_pdf(str(path))
            self.logger.info(f"PDF generated via WeasyPrint: {path}")
        elif PDFKIT_AVAILABLE:
            pdfkit.from_string(html_doc, str(path))
            self.logger.info(f"PDF generated via pdfkit: {path}")
        else:
            # Fallback: save as HTML and warn
            path = self.output_dir / f"{report_id}_pdf_fallback.html"
            path.write_text(html_doc, encoding="utf-8")
            self.logger.warning(
                "Neither WeasyPrint nor pdfkit is installed. "
                "Saved HTML fallback instead. Install WeasyPrint: pip install weasyprint"
            )
            return {
                "path": str(path),
                "size_bytes": path.stat().st_size,
                "warning": "PDF library not available; HTML fallback saved.",
            }

        return {"path": str(path), "size_bytes": path.stat().st_size}

    # ------------------------------------------------------------------ #
    # JSON                                                                 #
    # ------------------------------------------------------------------ #

    def _save_json(
        self, sections: List[Dict[str, Any]], metadata: Dict[str, Any], report_id: str
    ) -> Dict[str, Any]:
        payload = {
            "report_id": report_id,
            "metadata": metadata,
            "sections": sections,
            "generated_at": datetime.utcnow().isoformat(),
        }
        path = self.output_dir / f"{report_id}.json"
        path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
        self.logger.info(f"JSON report saved: {path}")
        return {"path": str(path), "size_bytes": path.stat().st_size, "content": payload}

    # ------------------------------------------------------------------ #
    # Utilities                                                            #
    # ------------------------------------------------------------------ #

    def _make_report_id(self, metadata: Dict[str, Any]) -> str:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        report_type = metadata.get("report_type", "report").replace(" ", "_").lower()
        hash_suffix = hashlib.md5(json.dumps(metadata, default=str).encode()).hexdigest()[:6]
        return f"regiq_{report_type}_{timestamp}_{hash_suffix}"

    def embed_image_as_base64(self, image_path: Union[str, Path]) -> str:
        """Convert an image file to a base64 data URI string."""
        image_path = Path(image_path)
        with open(image_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
        suffix = image_path.suffix.lstrip(".")
        mime = "jpeg" if suffix in ("jpg", "jpeg") else suffix
        return f"data:image/{mime};base64,{encoded}"

    def get_supported_formats(self) -> List[str]:
        formats = ["html", "json"]
        if WEASYPRINT_AVAILABLE or PDFKIT_AVAILABLE:
            formats.append("pdf")
        return formats

    def __repr__(self) -> str:
        return f"ReportOutputGenerator(output_dir={self.output_dir})"
