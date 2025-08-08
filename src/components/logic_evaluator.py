import google.generativeai as genai
import logging
from typing import List, Dict, Any
import json
import asyncio

from ..models import ProcessedQuestion, AnswerResult
from ..config import Config

logger = logging.getLogger(__name__)

class LogicEvaluator:
    """Component 5: Logic Evaluation - Decision processing"""
    
    def __init__(self):
        if not Config.GEMINI_API_KEY:
            raise ValueError("Gemini API key is required")
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
    
    async def evaluate_question(self, processed_question: ProcessedQuestion, matched_clauses: List[Dict[str, Any]], document_weight: float) -> AnswerResult:
        """Evaluate a question and generate an answer with reasoning"""
        try:
            logger.info(f"Evaluating question: {processed_question.original_question}")
            
            # Prepare context for LLM
            context = self._prepare_context(processed_question, matched_clauses)
            
            # Generate answer using LLM
            answer, confidence_score, reasoning = await self._generate_answer_with_llm(
                processed_question, context
            )
            
            # Extract source clauses
            source_clauses = self._extract_source_clauses(matched_clauses)
            
            # Calculate score contribution
            score_contribution = self._calculate_score_contribution(
                processed_question.weight, document_weight, confidence_score
            )
            
            answer_result = AnswerResult(
                answer=answer,
                confidence_score=confidence_score,
                source_clauses=source_clauses,
                reasoning=reasoning,
                question_weight=processed_question.weight,
                document_weight=document_weight,
                score_contribution=score_contribution
            )
            
            logger.info(f"Generated answer with confidence: {confidence_score}")
            return answer_result
            
        except Exception as e:
            logger.error(f"Failed to evaluate question: {e}")
            # Return fallback answer
            return self._create_fallback_answer(processed_question, document_weight)
    
    def _prepare_context(self, processed_question: ProcessedQuestion, matched_clauses: List[Dict[str, Any]]) -> str:
        """Prepare context for LLM evaluation"""
        context_parts = []
        
        # Add question information
        context_parts.append(f"Question: {processed_question.original_question}")
        context_parts.append(f"Question Type: {processed_question.question_type.value}")
        context_parts.append(f"Extracted Terms: {', '.join(processed_question.extracted_terms)}")
        
        # Add structured query information
        structured_query = processed_question.structured_query
        context_parts.append(f"Query Type: {structured_query.get('query_type', 'general')}")
        context_parts.append(f"Entities: {', '.join(structured_query.get('entities', []))}")
        context_parts.append(f"Conditions: {', '.join(structured_query.get('conditions', []))}")
        
        # Add relevant clauses
        context_parts.append("\nRelevant Policy Clauses:")
        for i, clause_info in enumerate(matched_clauses[:3]):  # Top 3 clauses
            clause = clause_info["clause"]
            relevance = clause_info["relevance_score"]
            context_parts.append(f"{i+1}. {clause['text']} (Relevance: {relevance:.2f})")
        
        return "\n".join(context_parts)
    
    async def _generate_answer_with_llm(self, processed_question: ProcessedQuestion, context: str) -> tuple:
        """Generate answer using LLM"""
        try:
            prompt = f"""
            You are an expert insurance policy analyst. Based on the following context, provide a clear and accurate answer to the question.
            
            {context}
            
            Instructions:
            1. Answer the question directly and concisely
            2. Use information from the provided policy clauses
            3. If the information is not available in the clauses, state that clearly
            4. Provide specific details like numbers, percentages, or time periods when mentioned
            5. Be factual and avoid speculation
            
            Question: {processed_question.original_question}
            
            Provide your answer in the following JSON format:
            {{
                "answer": "Your direct answer here",
                "confidence": 0.95,
                "reasoning": "Explanation of how you arrived at this answer"
            }}
            """
            
            response = await self.model.generate_content_async(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=Config.GEMINI_MAX_TOKENS,
                    temperature=Config.GEMINI_TEMPERATURE
                )
            )
            
            content = response.text
            
            # Parse JSON response
            try:
                result = json.loads(content)
                answer = result.get("answer", "Unable to determine answer from available information.")
                confidence = result.get("confidence", 0.5)
                reasoning = result.get("reasoning", "Based on analysis of policy clauses.")
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                answer = content.strip()
                confidence = 0.7
                reasoning = "Generated from policy analysis."
            
            return answer, confidence, reasoning
            
        except Exception as e:
            logger.error(f"Failed to generate answer with LLM: {e}")
            return "Unable to determine answer from available information.", 0.3, "LLM processing failed."
    
    def _extract_source_clauses(self, matched_clauses: List[Dict[str, Any]]) -> List[str]:
        """Extract source clauses for attribution"""
        source_clauses = []
        
        for clause_info in matched_clauses[:3]:  # Top 3 clauses
            clause = clause_info["clause"]
            source_chunk = clause_info["source_chunk"]
            
            # Create source clause description
            source_desc = f"Clause: {clause['text'][:100]}..."
            if source_chunk.page_number:
                source_desc += f" (Page {source_chunk.page_number})"
            
            source_clauses.append(source_desc)
        
        return source_clauses
    
    def _calculate_score_contribution(self, question_weight: float, document_weight: float, confidence_score: float) -> float:
        """Calculate score contribution for this answer"""
        # Only contribute to score if confidence is high enough
        if confidence_score >= 0.7:
            return question_weight * document_weight
        else:
            return 0.0
    
    def _create_fallback_answer(self, processed_question: ProcessedQuestion, document_weight: float) -> AnswerResult:
        """Create a fallback answer when processing fails"""
        return AnswerResult(
            answer="Unable to determine answer from available information.",
            confidence_score=0.3,
            source_clauses=[],
            reasoning="Processing failed, using fallback response.",
            question_weight=processed_question.weight,
            document_weight=document_weight,
            score_contribution=0.0
        )
    
    async def evaluate_questions_batch(self, processed_questions: List[ProcessedQuestion], 
                                    all_matched_clauses: List[List[Dict[str, Any]]], 
                                    document_weights: List[float]) -> List[AnswerResult]:
        """Evaluate multiple questions in batch"""
        tasks = []
        
        for i, (question, clauses, weight) in enumerate(zip(processed_questions, all_matched_clauses, document_weights)):
            task = self.evaluate_question(question, clauses, weight)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        answer_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Failed to evaluate question {i}: {result}")
                # Create fallback answer
                fallback = self._create_fallback_answer(processed_questions[i], document_weights[i])
                answer_results.append(fallback)
            else:
                answer_results.append(result)
        
        return answer_results
    
    def calculate_total_score(self, answer_results: List[AnswerResult]) -> float:
        """Calculate total score from all answer results"""
        total_score = sum(result.score_contribution for result in answer_results)
        return total_score
    
    def generate_score_breakdown(self, answer_results: List[AnswerResult]) -> List[Dict[str, Any]]:
        """Generate detailed score breakdown"""
        breakdown = []
        
        for i, result in enumerate(answer_results):
            breakdown.append({
                "question_index": i,
                "question_weight": result.question_weight,
                "document_weight": result.document_weight,
                "confidence_score": result.confidence_score,
                "score_contribution": result.score_contribution,
                "is_correct": result.confidence_score >= 0.7
            })
        
        return breakdown
