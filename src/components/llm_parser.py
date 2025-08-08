import google.generativeai as genai
import logging
from typing import List, Dict, Any
import json
import re
import asyncio

from ..models import ProcessedQuestion, QuestionType
from ..config import Config

logger = logging.getLogger(__name__)

class LLMParser:
    """Component 2: LLM Parser - Extract structured query from natural language"""
    
    def __init__(self):
        if not Config.GEMINI_API_KEY:
            raise ValueError("Gemini API key is required")
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
    
    def classify_question_type(self, question: str) -> QuestionType:
        """Classify question type for scoring weights"""
        question_lower = question.lower()
        
        # Define patterns for each question type
        patterns = {
            QuestionType.GRACE_PERIOD: [
                r'grace period', r'premium payment', r'due date'
            ],
            QuestionType.WAITING_PERIOD: [
                r'waiting period', r'pre-existing', r'ped', r'coverage.*wait'
            ],
            QuestionType.COVERAGE: [
                r'cover', r'coverage', r'what.*cover', r'does.*cover'
            ],
            QuestionType.MATERNITY: [
                r'maternity', r'pregnancy', r'childbirth', r'prenatal'
            ],
            QuestionType.SURGERY: [
                r'surgery', r'operation', r'knee surgery', r'cataract'
            ],
            QuestionType.ORGAN_DONOR: [
                r'organ donor', r'donor.*medical', r'organ.*expense'
            ],
            QuestionType.NCD: [
                r'ncd', r'no claim discount', r'discount.*claim'
            ],
            QuestionType.HEALTH_CHECKUP: [
                r'health check', r'preventive', r'checkup', r'health.*check'
            ],
            QuestionType.HOSPITAL_DEFINITION: [
                r'hospital.*definition', r'what.*hospital', r'define.*hospital'
            ],
            QuestionType.AYUSH: [
                r'ayush', r'ayurveda', r'yoga', r'naturopathy', r'unani'
            ],
            QuestionType.ROOM_RENT: [
                r'room rent', r'icu.*charge', r'daily.*rent', r'room.*limit'
            ]
        }
        
        for question_type, pattern_list in patterns.items():
            for pattern in pattern_list:
                if re.search(pattern, question_lower):
                    return question_type
        
        return QuestionType.DEFAULT
    
    def extract_key_terms(self, question: str) -> List[str]:
        """Extract key terms from the question"""
        # Remove common question words
        stop_words = {
            'what', 'is', 'the', 'does', 'do', 'are', 'and', 'or', 'for', 'in', 'on', 'at', 'to', 'of', 'with', 'by'
        }
        
        # Extract words and filter
        words = re.findall(r'\b\w+\b', question.lower())
        key_terms = [word for word in words if word not in stop_words and len(word) > 2]
        
        return key_terms
    
    async def parse_question_with_llm(self, question: str) -> Dict[str, Any]:
        """Use LLM to parse question into structured format"""
        try:
            prompt = f"""
            Parse the following insurance policy question into a structured format.
            
            Question: "{question}"
            
            Extract the following information:
            1. Query type (coverage_check, waiting_period, grace_period, maternity, surgery, etc.)
            2. Key entities (body parts, procedures, conditions, etc.)
            3. Specific conditions or requirements being asked about
            4. Whether it's asking about coverage, conditions, or definitions
            
            Return as JSON with these fields:
            {{
                "query_type": "string",
                "entities": ["list", "of", "entities"],
                "conditions": ["list", "of", "conditions"],
                "focus": "coverage|conditions|definition",
                "specific_terms": ["list", "of", "specific", "terms"]
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
            logger.info(f"LLM response: {content[:200]}...")
            
            if not content or content.strip() == "":
                logger.error("Empty response from LLM")
                raise ValueError("Empty response from LLM")
            
            try:
                # Remove markdown formatting if present
                cleaned_content = content.strip()
                if cleaned_content.startswith('```json'):
                    cleaned_content = cleaned_content[7:]
                if cleaned_content.endswith('```'):
                    cleaned_content = cleaned_content[:-3]
                cleaned_content = cleaned_content.strip()
                
                structured_query = json.loads(cleaned_content)
                return structured_query
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse LLM response as JSON: {e}")
                logger.error(f"Raw response: {content}")
                raise
            
        except Exception as e:
            logger.error(f"Failed to parse question with LLM: {e}")
            # Fallback to basic parsing
            return {
                "query_type": "general",
                "entities": self.extract_key_terms(question),
                "conditions": [],
                "focus": "coverage",
                "specific_terms": self.extract_key_terms(question)
            }
    
    def get_question_weight(self, question_type: QuestionType) -> float:
        """Get scoring weight for question type"""
        weights = Config.get_scoring_weights()
        return weights.get(question_type.value, Config.DEFAULT_QUESTION_WEIGHT)
    
    async def process_question(self, question: str) -> ProcessedQuestion:
        """Process a single question"""
        try:
            logger.info(f"Processing question: {question}")
            
            # Classify question type
            question_type = self.classify_question_type(question)
            
            # Extract key terms
            extracted_terms = self.extract_key_terms(question)
            
            # Parse with LLM
            structured_query = await self.parse_question_with_llm(question)
            
            # Get question weight
            weight = self.get_question_weight(question_type)
            
            processed_question = ProcessedQuestion(
                original_question=question,
                question_type=question_type,
                extracted_terms=extracted_terms,
                structured_query=structured_query,
                weight=weight
            )
            
            logger.info(f"Processed question type: {question_type}, weight: {weight}")
            return processed_question
            
        except Exception as e:
            logger.error(f"Failed to process question: {e}")
            raise
    
    async def process_questions(self, questions: List[str]) -> List[ProcessedQuestion]:
        """Process multiple questions"""
        tasks = [self.process_question(question) for question in questions]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        processed_questions = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Failed to process question {questions[i]}: {result}")
                # Create a default processed question
                default_question = ProcessedQuestion(
                    original_question=questions[i],
                    question_type=QuestionType.DEFAULT,
                    extracted_terms=self.extract_key_terms(questions[i]),
                    structured_query={"query_type": "general", "entities": [], "conditions": [], "focus": "coverage", "specific_terms": []},
                    weight=Config.DEFAULT_QUESTION_WEIGHT
                )
                processed_questions.append(default_question)
            else:
                processed_questions.append(result)
        
        return processed_questions
