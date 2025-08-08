from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl
from enum import Enum

class DocumentType(str, Enum):
    """Document type enumeration"""
    PDF = "pdf"
    DOCX = "docx"
    EMAIL = "email"
    UNKNOWN = "unknown"

class QuestionType(str, Enum):
    """Question type for scoring weights"""
    GRACE_PERIOD = "grace_period"
    WAITING_PERIOD = "waiting_period"
    COVERAGE = "coverage"
    MATERNITY = "maternity"
    SURGERY = "surgery"
    ORGAN_DONOR = "organ_donor"
    NCD = "ncd"
    HEALTH_CHECKUP = "health_checkup"
    HOSPITAL_DEFINITION = "hospital_definition"
    AYUSH = "ayush"
    ROOM_RENT = "room_rent"
    DEFAULT = "default"

class QueryRequest(BaseModel):
    """Request model for the query endpoint"""
    documents: List[HttpUrl] = Field(..., description="List of document URLs to process")
    questions: List[str] = Field(..., description="List of questions to answer")
    
    class Config:
        schema_extra = {
            "example": {
                "documents": [
                    "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24"
                ],
                "questions": [
                    "What is the grace period for premium payment?",
                    "What is the waiting period for pre-existing diseases (PED)?",
                    "Does the policy cover maternity expenses and what are the conditions?"
                ]
            }
        }

class QueryResponse(BaseModel):
    """Response model for the query endpoint"""
    answers: List[str] = Field(..., description="List of answers corresponding to questions")
    confidence_scores: Optional[List[float]] = Field(None, description="Confidence scores for each answer")
    source_clauses: Optional[List[str]] = Field(None, description="Source clauses for each answer")
    processing_time: Optional[float] = Field(None, description="Total processing time in seconds")
    
    class Config:
        schema_extra = {
            "example": {
                "answers": [
                    "A grace period of thirty days is provided for premium payment after the due date to renew or continue the policy.",
                    "There is a waiting period of thirty-six (36) months of continuous coverage from the first policy inception date.",
                    "Yes, the policy covers maternity expenses, including childbirth and lawful medical termination of pregnancy."
                ],
                "confidence_scores": [0.95, 0.92, 0.88],
                "source_clauses": ["Section 3.2 Grace Period", "Section 4.1 Waiting Period", "Section 5.3 Maternity Coverage"],
                "processing_time": 2.34
            }
        }

class DocumentChunk(BaseModel):
    """Model for document chunks"""
    id: str
    content: str
    page_number: Optional[int] = None
    chunk_index: int
    document_url: str
    embedding: Optional[List[float]] = None

class ProcessedQuestion(BaseModel):
    """Model for processed questions"""
    original_question: str
    question_type: QuestionType
    extracted_terms: List[str]
    structured_query: Dict[str, Any]
    weight: float

class SearchResult(BaseModel):
    """Model for search results"""
    chunk: DocumentChunk
    similarity_score: float
    relevance_score: float
    source_section: Optional[str] = None

class AnswerResult(BaseModel):
    """Model for answer results"""
    answer: str
    confidence_score: float
    source_clauses: List[str]
    reasoning: str
    question_weight: float
    document_weight: float
    score_contribution: float

class ScoringResult(BaseModel):
    """Model for scoring results"""
    total_score: float
    correct_answers: int
    total_questions: int
    score_breakdown: List[Dict[str, Any]]
    accuracy_percentage: float
