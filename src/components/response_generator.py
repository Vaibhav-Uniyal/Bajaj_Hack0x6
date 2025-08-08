import logging
from typing import List, Dict, Any
import time
from datetime import datetime

from ..models import QueryResponse, AnswerResult, ScoringResult
from ..config import Config

logger = logging.getLogger(__name__)

class ResponseGenerator:
    """Component 6: JSON Output - Structured response generation"""
    
    def __init__(self):
        self.start_time = None
    
    def start_timing(self):
        """Start timing the processing"""
        self.start_time = time.time()
    
    def get_processing_time(self) -> float:
        """Get total processing time"""
        if self.start_time:
            return time.time() - self.start_time
        return 0.0
    
    def generate_response(self, answer_results: List[AnswerResult]) -> QueryResponse:
        """Generate structured JSON response"""
        try:
            logger.info("Generating structured response")
            
            # Extract answers
            answers = [result.answer for result in answer_results]
            
            # Extract confidence scores
            confidence_scores = [result.confidence_score for result in answer_results]
            
            # Extract source clauses
            source_clauses = []
            for result in answer_results:
                if result.source_clauses:
                    source_clauses.append(result.source_clauses[0])  # Take first source
                else:
                    source_clauses.append("No specific source clause identified")
            
            # Calculate processing time
            processing_time = self.get_processing_time()
            
            response = QueryResponse(
                answers=answers,
                confidence_scores=confidence_scores,
                source_clauses=source_clauses,
                processing_time=processing_time
            )
            
            logger.info(f"Generated response with {len(answers)} answers")
            return response
            
        except Exception as e:
            logger.error(f"Failed to generate response: {e}")
            # Return fallback response
            return self._create_fallback_response(len(answer_results))
    
    def generate_detailed_response(self, answer_results: List[AnswerResult], 
                                 questions: List[str]) -> Dict[str, Any]:
        """Generate detailed response with additional information"""
        try:
            # Basic response
            basic_response = self.generate_response(answer_results)
            
            # Calculate scoring information
            total_score = sum(result.score_contribution for result in answer_results)
            correct_answers = sum(1 for result in answer_results if result.confidence_score >= 0.7)
            accuracy_percentage = (correct_answers / len(answer_results)) * 100 if answer_results else 0
            
            # Generate score breakdown
            score_breakdown = []
            for i, result in enumerate(answer_results):
                breakdown_item = {
                    "question": questions[i] if i < len(questions) else f"Question {i+1}",
                    "answer": result.answer,
                    "confidence_score": result.confidence_score,
                    "question_weight": result.question_weight,
                    "document_weight": result.document_weight,
                    "score_contribution": result.score_contribution,
                    "is_correct": result.confidence_score >= 0.7,
                    "source_clauses": result.source_clauses,
                    "reasoning": result.reasoning
                }
                score_breakdown.append(breakdown_item)
            
            # Create detailed response
            detailed_response = {
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "processing_time": basic_response.processing_time,
                "total_score": total_score,
                "correct_answers": correct_answers,
                "total_questions": len(answer_results),
                "accuracy_percentage": accuracy_percentage,
                "answers": basic_response.answers,
                "confidence_scores": basic_response.confidence_scores,
                "source_clauses": basic_response.source_clauses,
                "score_breakdown": score_breakdown,
                "metadata": {
                    "model_used": Config.GEMINI_MODEL,
                    "embedding_model": Config.EMBEDDING_MODEL,
                    "vector_db": "Pinecone" if Config.PINECONE_API_KEY else "FAISS"
                }
            }
            
            return detailed_response
            
        except Exception as e:
            logger.error(f"Failed to generate detailed response: {e}")
            return self._create_fallback_detailed_response(len(answer_results))
    
    def generate_scoring_result(self, answer_results: List[AnswerResult]) -> ScoringResult:
        """Generate scoring result for evaluation"""
        try:
            total_score = sum(result.score_contribution for result in answer_results)
            correct_answers = sum(1 for result in answer_results if result.confidence_score >= 0.7)
            total_questions = len(answer_results)
            accuracy_percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
            
            # Generate score breakdown
            score_breakdown = []
            for i, result in enumerate(answer_results):
                breakdown_item = {
                    "question_index": i,
                    "question_weight": result.question_weight,
                    "document_weight": result.document_weight,
                    "confidence_score": result.confidence_score,
                    "score_contribution": result.score_contribution,
                    "is_correct": result.confidence_score >= 0.7
                }
                score_breakdown.append(breakdown_item)
            
            scoring_result = ScoringResult(
                total_score=total_score,
                correct_answers=correct_answers,
                total_questions=total_questions,
                score_breakdown=score_breakdown,
                accuracy_percentage=accuracy_percentage
            )
            
            return scoring_result
            
        except Exception as e:
            logger.error(f"Failed to generate scoring result: {e}")
            return ScoringResult(
                total_score=0.0,
                correct_answers=0,
                total_questions=len(answer_results),
                score_breakdown=[],
                accuracy_percentage=0.0
            )
    
    def _create_fallback_response(self, num_questions: int) -> QueryResponse:
        """Create fallback response when processing fails"""
        fallback_answers = ["Unable to determine answer from available information."] * num_questions
        fallback_confidence = [0.3] * num_questions
        fallback_sources = ["No source clause identified"] * num_questions
        
        return QueryResponse(
            answers=fallback_answers,
            confidence_scores=fallback_confidence,
            source_clauses=fallback_sources,
            processing_time=self.get_processing_time()
        )
    
    def _create_fallback_detailed_response(self, num_questions: int) -> Dict[str, Any]:
        """Create fallback detailed response"""
        return {
            "status": "error",
            "timestamp": datetime.now().isoformat(),
            "processing_time": self.get_processing_time(),
            "total_score": 0.0,
            "correct_answers": 0,
            "total_questions": num_questions,
            "accuracy_percentage": 0.0,
            "answers": ["Unable to determine answer from available information."] * num_questions,
            "confidence_scores": [0.3] * num_questions,
            "source_clauses": ["No source clause identified"] * num_questions,
            "score_breakdown": [],
            "metadata": {
                "model_used": "fallback",
                "embedding_model": "fallback",
                "vector_db": "fallback"
            }
        }
    
    def format_for_api(self, response: QueryResponse) -> Dict[str, Any]:
        """Format response for API output"""
        return {
            "answers": response.answers,
            "confidence_scores": response.confidence_scores,
            "source_clauses": response.source_clauses,
            "processing_time": response.processing_time
        }
    
    def generate_explanation_summary(self, answer_results: List[AnswerResult]) -> str:
        """Generate a summary explanation of the results"""
        try:
            total_questions = len(answer_results)
            high_confidence = sum(1 for result in answer_results if result.confidence_score >= 0.8)
            medium_confidence = sum(1 for result in answer_results if 0.5 <= result.confidence_score < 0.8)
            low_confidence = sum(1 for result in answer_results if result.confidence_score < 0.5)
            
            total_score = sum(result.score_contribution for result in answer_results)
            
            summary = f"""
            Processing Summary:
            - Total Questions: {total_questions}
            - High Confidence Answers: {high_confidence}
            - Medium Confidence Answers: {medium_confidence}
            - Low Confidence Answers: {low_confidence}
            - Total Score: {total_score:.2f}
            - Average Confidence: {sum(result.confidence_score for result in answer_results) / total_questions:.2f}
            """
            
            return summary.strip()
            
        except Exception as e:
            logger.error(f"Failed to generate explanation summary: {e}")
            return "Unable to generate explanation summary."
