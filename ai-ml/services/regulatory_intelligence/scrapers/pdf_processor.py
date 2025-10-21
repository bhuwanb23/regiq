#!/usr/bin/env python3
"""
REGIQ AI/ML - PDF Processing Module
Advanced PDF text extraction and processing for regulatory documents.
Integrates with Gemini 2.5-flash for intelligent document analysis.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime

# PDF Processing Libraries
try:
    import PyPDF2
    import pdfplumber
    import fitz  # PyMuPDF
    import tabula
    PDF_LIBRARIES_AVAILABLE = True
except ImportError as e:
    PDF_LIBRARIES_AVAILABLE = False
    print(f"⚠️  PDF libraries not installed: {e}")
    print("   Install with: pip install PyPDF2 pdfplumber pymupdf tabula-py")

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from config.env_config import get_env_config
from config.gemini_config import GeminiAPIManager


@dataclass
class PDFMetadata:
    """PDF document metadata."""
    filename: str
    file_size: int
    page_count: int
    title: Optional[str] = None
    author: Optional[str] = None
    subject: Optional[str] = None
    creator: Optional[str] = None
    producer: Optional[str] = None
    creation_date: Optional[datetime] = None
    modification_date: Optional[datetime] = None


@dataclass
class ExtractedContent:
    """Extracted content from PDF."""
    text: str
    tables: List[Dict] = None
    images: List[Dict] = None
    metadata: PDFMetadata = None
    page_texts: List[str] = None
    structured_data: Dict = None


class PDFProcessor:
    """
    Advanced PDF processing for regulatory documents.
    Uses multiple libraries for robust extraction and Gemini for analysis.
    """
    
    def __init__(self):
        """Initialize PDF processor."""
        self.env_config = get_env_config()
        self.gemini_manager = GeminiAPIManager()
        self.logger = self._setup_logging()
        
        if not PDF_LIBRARIES_AVAILABLE:
            raise ImportError("PDF processing libraries not available. Please install required packages.")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for PDF processor."""
        logger = logging.getLogger('pdf_processor')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def extract_text_pypdf2(self, pdf_path: str) -> Tuple[str, List[str]]:
        """Extract text using PyPDF2 (good for simple PDFs)."""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                full_text = ""
                page_texts = []
                
                for page_num, page in enumerate(reader.pages):
                    try:
                        page_text = page.extract_text()
                        page_texts.append(page_text)
                        full_text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
                    except Exception as e:
                        self.logger.warning(f"Error extracting page {page_num + 1}: {e}")
                        page_texts.append("")
                
                return full_text, page_texts
                
        except Exception as e:
            self.logger.error(f"PyPDF2 extraction failed: {e}")
            return "", []
    
    def extract_text_pdfplumber(self, pdf_path: str) -> Tuple[str, List[str], List[Dict]]:
        """Extract text and tables using pdfplumber (good for complex layouts)."""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                full_text = ""
                page_texts = []
                tables = []
                
                for page_num, page in enumerate(pdf.pages):
                    try:
                        # Extract text
                        page_text = page.extract_text() or ""
                        page_texts.append(page_text)
                        full_text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
                        
                        # Extract tables
                        page_tables = page.extract_tables()
                        if page_tables:
                            for table_num, table in enumerate(page_tables):
                                tables.append({
                                    'page': page_num + 1,
                                    'table_num': table_num + 1,
                                    'data': table,
                                    'bbox': page.within_bbox(page.bbox).extract_tables()[table_num] if hasattr(page, 'bbox') else None
                                })
                    
                    except Exception as e:
                        self.logger.warning(f"Error processing page {page_num + 1}: {e}")
                        page_texts.append("")
                
                return full_text, page_texts, tables
                
        except Exception as e:
            self.logger.error(f"pdfplumber extraction failed: {e}")
            return "", [], []
    
    def extract_text_pymupdf(self, pdf_path: str) -> Tuple[str, List[str], List[Dict]]:
        """Extract text and images using PyMuPDF (good for complex documents)."""
        try:
            doc = fitz.open(pdf_path)
            full_text = ""
            page_texts = []
            images = []
            
            for page_num in range(doc.page_count):
                try:
                    page = doc[page_num]
                    
                    # Extract text
                    page_text = page.get_text()
                    page_texts.append(page_text)
                    full_text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
                    
                    # Extract images
                    image_list = page.get_images()
                    for img_index, img in enumerate(image_list):
                        images.append({
                            'page': page_num + 1,
                            'image_num': img_index + 1,
                            'xref': img[0],
                            'bbox': page.get_image_bbox(img)
                        })
                
                except Exception as e:
                    self.logger.warning(f"Error processing page {page_num + 1}: {e}")
                    page_texts.append("")
            
            doc.close()
            return full_text, page_texts, images
            
        except Exception as e:
            self.logger.error(f"PyMuPDF extraction failed: {e}")
            return "", [], []
    
    def extract_tables_tabula(self, pdf_path: str) -> List[Dict]:
        """Extract tables using tabula-py (specialized for tables)."""
        try:
            # Extract all tables from all pages
            tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
            
            structured_tables = []
            for i, table in enumerate(tables):
                structured_tables.append({
                    'table_num': i + 1,
                    'data': table.to_dict('records') if hasattr(table, 'to_dict') else table,
                    'shape': table.shape if hasattr(table, 'shape') else None,
                    'columns': list(table.columns) if hasattr(table, 'columns') else None
                })
            
            return structured_tables
            
        except Exception as e:
            self.logger.error(f"Tabula table extraction failed: {e}")
            return []
    
    def get_pdf_metadata(self, pdf_path: str) -> PDFMetadata:
        """Extract PDF metadata."""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                metadata = reader.metadata or {}
                
                file_stats = os.stat(pdf_path)
                
                return PDFMetadata(
                    filename=os.path.basename(pdf_path),
                    file_size=file_stats.st_size,
                    page_count=len(reader.pages),
                    title=metadata.get('/Title'),
                    author=metadata.get('/Author'),
                    subject=metadata.get('/Subject'),
                    creator=metadata.get('/Creator'),
                    producer=metadata.get('/Producer'),
                    creation_date=metadata.get('/CreationDate'),
                    modification_date=metadata.get('/ModDate')
                )
                
        except Exception as e:
            self.logger.error(f"Metadata extraction failed: {e}")
            return PDFMetadata(
                filename=os.path.basename(pdf_path),
                file_size=0,
                page_count=0
            )
    
    def process_pdf_comprehensive(self, pdf_path: str) -> ExtractedContent:
        """
        Comprehensive PDF processing using multiple methods.
        Combines results from different libraries for best extraction.
        """
        self.logger.info(f"🔍 Processing PDF: {pdf_path}")
        
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        # Get metadata
        metadata = self.get_pdf_metadata(pdf_path)
        self.logger.info(f"📄 PDF Info: {metadata.page_count} pages, {metadata.file_size} bytes")
        
        # Try multiple extraction methods
        best_text = ""
        best_page_texts = []
        tables = []
        images = []
        
        # Method 1: pdfplumber (best for complex layouts)
        try:
            text1, page_texts1, tables1 = self.extract_text_pdfplumber(pdf_path)
            if len(text1) > len(best_text):
                best_text = text1
                best_page_texts = page_texts1
            tables.extend(tables1)
            self.logger.info("✅ pdfplumber extraction successful")
        except Exception as e:
            self.logger.warning(f"pdfplumber failed: {e}")
        
        # Method 2: PyMuPDF (good for images and complex docs)
        try:
            text2, page_texts2, images2 = self.extract_text_pymupdf(pdf_path)
            if len(text2) > len(best_text):
                best_text = text2
                best_page_texts = page_texts2
            images.extend(images2)
            self.logger.info("✅ PyMuPDF extraction successful")
        except Exception as e:
            self.logger.warning(f"PyMuPDF failed: {e}")
        
        # Method 3: PyPDF2 (fallback)
        if not best_text:
            try:
                text3, page_texts3 = self.extract_text_pypdf2(pdf_path)
                best_text = text3
                best_page_texts = page_texts3
                self.logger.info("✅ PyPDF2 extraction successful (fallback)")
            except Exception as e:
                self.logger.error(f"All extraction methods failed: {e}")
        
        # Method 4: Specialized table extraction
        try:
            tabula_tables = self.extract_tables_tabula(pdf_path)
            tables.extend(tabula_tables)
            self.logger.info(f"✅ Extracted {len(tabula_tables)} tables with tabula")
        except Exception as e:
            self.logger.warning(f"Tabula table extraction failed: {e}")
        
        return ExtractedContent(
            text=best_text,
            tables=tables,
            images=images,
            metadata=metadata,
            page_texts=best_page_texts,
            structured_data={}
        )
    
    def analyze_with_gemini(self, content: ExtractedContent) -> Dict[str, Any]:
        """
        Analyze extracted content using Gemini 2.5-flash.
        Provides intelligent analysis of regulatory documents.
        """
        self.logger.info("🤖 Analyzing content with Gemini 2.5-flash")
        
        if not content.text.strip():
            return {"error": "No text content to analyze"}
        
        # Prepare analysis prompt
        analysis_prompt = f"""
Analyze this regulatory document and provide a structured analysis:

DOCUMENT METADATA:
- Filename: {content.metadata.filename if content.metadata else 'Unknown'}
- Pages: {content.metadata.page_count if content.metadata else 'Unknown'}
- Tables found: {len(content.tables) if content.tables else 0}

DOCUMENT TEXT (first 3000 characters):
{content.text[:3000]}...

Please provide:
1. DOCUMENT TYPE: What type of regulatory document is this?
2. KEY TOPICS: Main regulatory topics covered
3. IMPORTANT DATES: Any deadlines, effective dates, or compliance dates
4. REQUIREMENTS: Key compliance requirements mentioned
5. PENALTIES: Any penalties or enforcement actions mentioned
6. ENTITIES: Organizations, agencies, or companies mentioned
7. SUMMARY: Brief 2-3 sentence summary of the document

Format your response as JSON with these keys: document_type, key_topics, important_dates, requirements, penalties, entities, summary
"""
        
        try:
            # Use Gemini 2.5-flash for analysis
            response = self.gemini_manager.generate_content(
                analysis_prompt,
                model="gemini-2.5-flash"
            )
            
            if response:
                self.logger.info("✅ Gemini analysis completed")
                return {
                    "gemini_analysis": response,
                    "analysis_timestamp": datetime.now().isoformat(),
                    "model_used": "gemini-2.5-flash"
                }
            else:
                return {"error": "Gemini analysis failed"}
                
        except Exception as e:
            self.logger.error(f"Gemini analysis error: {e}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def process_regulatory_pdf(self, pdf_path: str, analyze_with_ai: bool = True) -> Dict[str, Any]:
        """
        Complete regulatory PDF processing pipeline.
        
        Args:
            pdf_path: Path to PDF file
            analyze_with_ai: Whether to analyze with Gemini
            
        Returns:
            Complete processing results
        """
        try:
            # Extract content
            content = self.process_pdf_comprehensive(pdf_path)
            
            # Prepare results
            results = {
                "pdf_path": pdf_path,
                "extraction_timestamp": datetime.now().isoformat(),
                "metadata": content.metadata.__dict__ if content.metadata else {},
                "text_length": len(content.text),
                "page_count": len(content.page_texts) if content.page_texts else 0,
                "tables_found": len(content.tables) if content.tables else 0,
                "images_found": len(content.images) if content.images else 0,
                "extracted_text": content.text,
                "page_texts": content.page_texts,
                "tables": content.tables,
                "images": content.images
            }
            
            # AI Analysis
            if analyze_with_ai:
                ai_analysis = self.analyze_with_gemini(content)
                results["ai_analysis"] = ai_analysis
            
            self.logger.info(f"✅ PDF processing completed: {pdf_path}")
            return results
            
        except Exception as e:
            self.logger.error(f"PDF processing failed: {e}")
            return {
                "error": str(e),
                "pdf_path": pdf_path,
                "processing_timestamp": datetime.now().isoformat()
            }
    
    def batch_process_pdfs(self, pdf_directory: str, output_directory: str = None) -> List[Dict]:
        """
        Batch process multiple PDFs in a directory.
        
        Args:
            pdf_directory: Directory containing PDF files
            output_directory: Directory to save results (optional)
            
        Returns:
            List of processing results
        """
        pdf_dir = Path(pdf_directory)
        if not pdf_dir.exists():
            raise FileNotFoundError(f"Directory not found: {pdf_directory}")
        
        pdf_files = list(pdf_dir.glob("*.pdf"))
        if not pdf_files:
            self.logger.warning(f"No PDF files found in {pdf_directory}")
            return []
        
        self.logger.info(f"📚 Processing {len(pdf_files)} PDF files")
        
        results = []
        for pdf_file in pdf_files:
            try:
                result = self.process_regulatory_pdf(str(pdf_file))
                results.append(result)
                
                # Save individual result if output directory specified
                if output_directory:
                    output_dir = Path(output_directory)
                    output_dir.mkdir(parents=True, exist_ok=True)
                    
                    output_file = output_dir / f"{pdf_file.stem}_analysis.json"
                    import json
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(result, f, indent=2, default=str)
                
            except Exception as e:
                self.logger.error(f"Failed to process {pdf_file}: {e}")
                results.append({
                    "error": str(e),
                    "pdf_path": str(pdf_file),
                    "processing_timestamp": datetime.now().isoformat()
                })
        
        self.logger.info(f"✅ Batch processing completed: {len(results)} files processed")
        return results


def main():
    """Test the PDF processor."""
    print("🧪 Testing PDF Processor")
    print("="*50)
    
    processor = PDFProcessor()
    
    # Test with a sample PDF (you would need to provide a real PDF file)
    test_pdf = "data/sample_regulatory_document.pdf"
    
    if os.path.exists(test_pdf):
        print(f"📄 Processing: {test_pdf}")
        result = processor.process_regulatory_pdf(test_pdf)
        
        print(f"✅ Processing completed!")
        print(f"📊 Text length: {result.get('text_length', 0)} characters")
        print(f"📄 Pages: {result.get('page_count', 0)}")
        print(f"📋 Tables: {result.get('tables_found', 0)}")
        print(f"🖼️  Images: {result.get('images_found', 0)}")
        
        if 'ai_analysis' in result:
            print(f"🤖 AI Analysis: Available")
    else:
        print(f"⚠️  Test PDF not found: {test_pdf}")
        print("   Place a sample regulatory PDF in data/ directory to test")


if __name__ == "__main__":
    main()
