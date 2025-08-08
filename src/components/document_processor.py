import asyncio
import aiohttp
import PyPDF2
import io
import logging
from typing import List, Optional
from urllib.parse import urlparse
import re

from ..models import DocumentChunk, DocumentType
from ..config import Config

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Component 1: Input Documents - Process PDFs, DOCX, and email documents"""
    
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        if not self.session:
            self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            self.session = None
    
    async def _ensure_session(self):
        """Ensure session is initialized"""
        if not self.session:
            self.session = aiohttp.ClientSession()
    
    async def download_document(self, url: str) -> bytes:
        """Download document from URL"""
        try:
            await self._ensure_session()
            # Ensure URL is a string
            url_str = str(url)
            logger.info(f"Downloading document from: {url_str}")
            async with self.session.get(url_str) as response:
                response.raise_for_status()
                content = await response.read()
                logger.info(f"Downloaded {len(content)} bytes from {url_str}")
                return content
        except Exception as e:
            logger.error(f"Failed to download document from {url}: {e}")
            raise
    
    def detect_document_type(self, url: str, content: bytes) -> DocumentType:
        """Detect document type from URL and content"""
        # Convert Pydantic URL to string if needed
        url_str = str(url)
        url_lower = url_str.lower()
        
        if url_lower.endswith('.pdf'):
            return DocumentType.PDF
        elif url_lower.endswith('.docx'):
            return DocumentType.DOCX
        elif 'email' in url_lower or 'mail' in url_lower:
            return DocumentType.EMAIL
        else:
            return DocumentType.UNKNOWN
    
    def extract_text_from_pdf(self, content: bytes) -> str:
        """Extract text from PDF content"""
        try:
            pdf_file = io.BytesIO(content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text.strip():
                    text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
            
            return text.strip()
        except Exception as e:
            logger.error(f"Failed to extract text from PDF: {e}")
            raise
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep important ones
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)\[\]\{\}]', '', text)
        
        # Normalize line breaks
        text = text.replace('\n', ' ').replace('\r', ' ')
        
        return text.strip()
    
    def chunk_text(self, text: str, document_url: str) -> List[DocumentChunk]:
        """Split text into chunks for processing"""
        chunks = []
        words = text.split()
        
        chunk_size = Config.MAX_CHUNK_SIZE
        overlap = Config.CHUNK_OVERLAP
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk_words = words[i:i + chunk_size]
            chunk_text = ' '.join(chunk_words)
            
            if chunk_text.strip():
                chunk = DocumentChunk(
                    id=f"{str(document_url)}_{i//chunk_size}",
                    content=chunk_text,
                    chunk_index=i // chunk_size,
                    document_url=str(document_url)
                )
                chunks.append(chunk)
        
        return chunks
    
    async def process_document(self, url: str) -> List[DocumentChunk]:
        """Process a single document and return chunks"""
        try:
            logger.info(f"Processing document: {url}")
            
            # Download document
            content = await self.download_document(url)
            
            # Detect document type
            doc_type = self.detect_document_type(url, content)
            logger.info(f"Detected document type: {doc_type}")
            
            # Extract text based on document type
            if doc_type == DocumentType.PDF:
                text = self.extract_text_from_pdf(content)
            else:
                # For now, handle other types as text
                text = content.decode('utf-8', errors='ignore')
            
            # Clean text
            text = self.clean_text(text)
            
            # Chunk text
            chunks = self.chunk_text(text, url)
            
            logger.info(f"Created {len(chunks)} chunks from document: {url}")
            return chunks
            
        except Exception as e:
            logger.error(f"Failed to process document {url}: {e}")
            import traceback
            logger.error(f"Document processing traceback: {traceback.format_exc()}")
            raise
    
    async def process_documents(self, urls: List[str]) -> List[DocumentChunk]:
        """Process multiple documents concurrently"""
        tasks = [self.process_document(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        all_chunks = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Failed to process document {urls[i]}: {result}")
                continue
            all_chunks.extend(result)
        
        logger.info(f"Total chunks processed: {len(all_chunks)}")
        return all_chunks
