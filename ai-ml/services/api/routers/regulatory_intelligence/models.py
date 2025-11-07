"""Pydantic models for Regulatory Intelligence API"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class DocumentAnalysisRequest(BaseModel):
    """Request model for document analysis"""
    document_text: str = Field(..., description="Text content of the regulatory document")
    document_type: str = Field(default="regulation", description="Type of document (regulation, guideline, policy)")
    analysis_depth: str = Field(default="standard", description="Depth of analysis (quick, standard, deep)")


class DocumentAnalysisResponse(BaseModel):
    """Response model for document analysis"""
    document_id: str = Field(..., description="Unique identifier for the document")
    compliance_score: float = Field(..., description="Overall compliance score (0-100)")
    key_findings: List[str] = Field(..., description="Key findings from the analysis")
    risk_factors: List[str] = Field(..., description="Identified risk factors")
    recommended_actions: List[str] = Field(..., description="Recommended compliance actions")
    processing_time: float = Field(..., description="Time taken to process the document (seconds)")


class SummarizationRequest(BaseModel):
    """Request model for document summarization"""
    text: str = Field(..., description="Text to summarize")
    summary_type: str = Field(default="executive", description="Type of summary (executive, technical, bullet)")
    max_length: int = Field(default=500, description="Maximum length of summary")


class SummarizationResponse(BaseModel):
    """Response model for document summarization"""
    summary: str = Field(..., description="Generated summary")
    key_points: List[str] = Field(..., description="Key points extracted from the text")
    word_count: int = Field(..., description="Word count of the summary")


class QARequest(BaseModel):
    """Request model for Q&A endpoint"""
    question: str = Field(..., description="Question to answer")
    context: str = Field(..., description="Context for answering the question")
    model_preference: str = Field(default="gemini", description="Preferred LLM model")


class QAResponse(BaseModel):
    """Response model for Q&A endpoint"""
    answer: str = Field(..., description="Answer to the question")
    confidence: float = Field(..., description="Confidence score (0-1)")
    citations: List[str] = Field(..., description="Relevant text snippets supporting the answer")
    processing_time: float = Field(..., description="Time taken to generate the answer (seconds)")


class SearchRequest(BaseModel):
    """Request model for search functionality"""
    query: str = Field(..., description="Search query")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="Search filters")
    page: int = Field(default=1, description="Page number")
    page_size: int = Field(default=10, description="Number of results per page")


class SearchResult(BaseModel):
    """Model for individual search results"""
    document_id: str = Field(..., description="Document identifier")
    title: str = Field(..., description="Document title")
    snippet: str = Field(..., description="Relevant text snippet")
    relevance_score: float = Field(..., description="Relevance score (0-1)")
    document_type: str = Field(..., description="Type of document")


class SearchResponse(BaseModel):
    """Response model for search functionality"""
    results: List[SearchResult] = Field(..., description="Search results")
    total_results: int = Field(..., description="Total number of matching documents")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of results per page")
    total_pages: int = Field(..., description="Total number of pages")