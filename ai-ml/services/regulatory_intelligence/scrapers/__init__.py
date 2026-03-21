#!/usr/bin/env python3
"""
REGIQ AI/ML - Regulatory Document Scrapers
Document ingestion pipeline for SEC EDGAR, EU regulatory sources,
PDF documents, and regulatory APIs.

Provides:
    - DocumentProcessingPipeline: Main orchestrator for all ingestion
    - PDFProcessor: PDF text extraction (PyPDF2, pdfplumber, PyMuPDF)
    - SECEdgarScraper: SEC EDGAR filings scraper
    - EURegulatoryScaper: EU regulatory documents scraper
    - RegulatoryAPIConnector: External regulatory API connector

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

from .document_pipeline import DocumentProcessingPipeline
from .pdf_processor import PDFProcessor, PDFMetadata, ExtractedContent
from .sec_edgar_scraper import SECEdgarScraper, SECFiling, ScrapingConfig
from .eu_regulatory_scraper import EURegulatoryScaper, EURegulatoryDocument
from .regulatory_api_connector import RegulatoryAPIConnector, APIConfig, RegulatoryAPIData

__version__ = "1.0.0"
__author__ = "REGIQ AI/ML Team"

__all__ = [
    # Pipeline
    "DocumentProcessingPipeline",
    # PDF
    "PDFProcessor",
    "PDFMetadata",
    "ExtractedContent",
    # SEC EDGAR
    "SECEdgarScraper",
    "SECFiling",
    "ScrapingConfig",
    # EU Regulatory
    "EURegulatoryScaper",
    "EURegulatoryDocument",
    # API Connector
    "RegulatoryAPIConnector",
    "APIConfig",
    "RegulatoryAPIData",
]
