import asyncio
import logging
from typing import List, Dict, Any
from urllib.parse import urlparse

from .components.document_processor import DocumentProcessor
from .components.llm_parser import LLMParser
from .components.embedding_search import EmbeddingSearch
from .components.clause_matcher import ClauseMatcher
from .components.logic_evaluator import LogicEvaluator
from .components.response_generator import ResponseGenerator
from .models import QueryRequest, QueryResponse, AnswerResult
from .config import Config

logger = logging.getLogger(__name__)

class QueryRetrievalOrchestrator:
    """Main orchestrator for the LLM-Powered Query Retrieval System"""
    
    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.llm_parser = LLMParser()
        self.embedding_search = EmbeddingSearch()
        self.clause_matcher = ClauseMatcher()
        self.logic_evaluator = LogicEvaluator()
        self.response_generator = ResponseGenerator()
    
    async def process_query(self, request: QueryRequest) -> QueryResponse:
        """Process a query request through all 6 components"""
        try:
            logger.info("Starting query processing")
            self.response_generator.start_timing()
            
            # Component 1: Input Documents - Process PDFs, DOCX, and email documents
            logger.info("Component 1: Processing documents")
            document_chunks = await self._process_documents(request.documents)
            
            # Component 2: LLM Parser - Extract structured query
            logger.info("Component 2: Parsing questions")
            processed_questions = await self._parse_questions(request.questions)
            
            # Component 3: Embedding Search - FAISS/Pinecone retrieval
            logger.info("Component 3: Indexing and searching")
            await self._index_documents(document_chunks)
            search_results = await self._search_documents(processed_questions, document_chunks)
            
            # Component 4: Clause Matching - Semantic similarity
            logger.info("Component 4: Matching clauses")
            matched_clauses = await self._match_clauses(processed_questions, search_results)
            
            # Component 5: Logic Evaluation - Decision processing
            logger.info("Component 5: Evaluating logic")
            answer_results = await self._evaluate_logic(processed_questions, matched_clauses, request.documents)
            
            # Component 6: JSON Output - Structured response
            logger.info("Component 6: Generating response")
            response = self.response_generator.generate_response(answer_results)
            
            logger.info("Query processing completed successfully")
            return response
            
        except Exception as e:
            logger.error(f"Failed to process query: {e}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            return self._create_error_response(len(request.questions))
    
    async def _process_documents(self, document_urls: List[str]) -> List:
        """Component 1: Process documents"""
        async with self.document_processor:
            return await self.document_processor.process_documents(document_urls)
    
    async def _parse_questions(self, questions: List[str]) -> List:
        """Component 2: Parse questions"""
        return await self.llm_parser.process_questions(questions)
    
    async def _index_documents(self, document_chunks: List) -> None:
        """Component 3: Index documents"""
        await self.embedding_search.index_chunks(document_chunks)
    
    async def _search_documents(self, processed_questions: List, document_chunks: List) -> List[List]:
        """Component 3: Search documents"""
        search_results = []
        for question in processed_questions:
            results = await self.embedding_search.search_by_question(question, document_chunks)
            search_results.append(results)
        return search_results
    
    async def _match_clauses(self, processed_questions: List, search_results: List[List]) -> List[List]:
        """Component 4: Match clauses"""
        matched_clauses = []
        for question, results in zip(processed_questions, search_results):
            clauses = self.clause_matcher.find_best_matches(question, results)
            matched_clauses.append(clauses)
        return matched_clauses
    
    async def _evaluate_logic(self, processed_questions: List, matched_clauses: List[List], document_urls: List[str]) -> List[AnswerResult]:
        """Component 5: Evaluate logic"""
        # Get document weights
        document_weights = []
        for url in document_urls:
            weight = self.embedding_search.get_document_weight(url)
            document_weights.append(weight)
        
        # Use the first document weight for now (assuming single document processing)
        # In a multi-document scenario, you'd need more sophisticated weight assignment
        document_weight = document_weights[0] if document_weights else Config.KNOWN_DOCUMENT_WEIGHT
        
        # Create list of document weights for each question
        question_document_weights = [document_weight] * len(processed_questions)
        
        return await self.logic_evaluator.evaluate_questions_batch(
            processed_questions, matched_clauses, question_document_weights
        )
    
    def _create_error_response(self, num_questions: int) -> QueryResponse:
        """Create error response"""
        error_answers = ["Unable to process request due to system error."] * num_questions
        error_confidence = [0.0] * num_questions
        error_sources = ["Error occurred during processing"] * num_questions
        
        return QueryResponse(
            answers=error_answers,
            confidence_scores=error_confidence,
            source_clauses=error_sources,
            processing_time=self.response_generator.get_processing_time()
        )
    
    async def process_query_with_details(self, request: QueryRequest) -> Dict[str, Any]:
        """Process query with detailed response including scoring"""
        try:
            logger.info("Starting detailed query processing")
            self.response_generator.start_timing()
            
            # Process through all components
            document_chunks = await self._process_documents(request.documents)
            processed_questions = await self._parse_questions(request.questions)
            await self._index_documents(document_chunks)
            search_results = await self._search_documents(processed_questions, document_chunks)
            matched_clauses = await self._match_clauses(processed_questions, search_results)
            
            # Get document weights
            document_weights = []
            for url in request.documents:
                weight = self.embedding_search.get_document_weight(url)
                document_weights.append(weight)
            
            document_weight = document_weights[0] if document_weights else Config.KNOWN_DOCUMENT_WEIGHT
            question_document_weights = [document_weight] * len(processed_questions)
            
            answer_results = await self.logic_evaluator.evaluate_questions_batch(
                processed_questions, matched_clauses, question_document_weights
            )
            
            # Generate detailed response
            detailed_response = self.response_generator.generate_detailed_response(
                answer_results, request.questions
            )
            
            # Add explanation summary
            explanation = self.response_generator.generate_explanation_summary(answer_results)
            detailed_response["explanation_summary"] = explanation
            
            return detailed_response
            
        except Exception as e:
            logger.error(f"Failed to process query with details: {e}")
            return self.response_generator._create_fallback_detailed_response(len(request.questions))
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status and configuration"""
        return {
            "status": "operational",
            "components": {
                "document_processor": "initialized",
                "llm_parser": "initialized",
                "embedding_search": "initialized",
                "clause_matcher": "initialized",
                "logic_evaluator": "initialized",
                "response_generator": "initialized"
            },
            "configuration": {
                "llm_model": Config.GEMINI_MODEL,
                "embedding_model": Config.EMBEDDING_MODEL,
                "vector_db": "Pinecone" if Config.PINECONE_API_KEY else "FAISS",
                "max_chunk_size": Config.MAX_CHUNK_SIZE,
                "known_document_weight": Config.KNOWN_DOCUMENT_WEIGHT,
                "unknown_document_weight": Config.UNKNOWN_DOCUMENT_WEIGHT
            }
        }
