import logging
from typing import List, Dict, Any
import re
from difflib import SequenceMatcher

from ..models import SearchResult, ProcessedQuestion
from ..config import Config

logger = logging.getLogger(__name__)

class ClauseMatcher:
    """Component 4: Clause Matching - Semantic similarity matching"""
    
    def __init__(self):
        self.clause_patterns = self._init_clause_patterns()
    
    def _init_clause_patterns(self) -> Dict[str, List[str]]:
        """Initialize patterns for different clause types"""
        return {
            "grace_period": [
                r"grace period.*\d+.*days",
                r"premium.*payment.*\d+.*days",
                r"due date.*\d+.*days"
            ],
            "waiting_period": [
                r"waiting period.*\d+.*months",
                r"pre-existing.*\d+.*months",
                r"ped.*\d+.*months"
            ],
            "coverage": [
                r"cover.*expenses",
                r"coverage.*include",
                r"policy.*cover"
            ],
            "maternity": [
                r"maternity.*expenses",
                r"pregnancy.*coverage",
                r"childbirth.*expenses"
            ],
            "surgery": [
                r"surgery.*coverage",
                r"operation.*expenses",
                r"knee.*surgery",
                r"cataract.*surgery"
            ],
            "organ_donor": [
                r"organ.*donor",
                r"donor.*medical",
                r"organ.*expenses"
            ],
            "ncd": [
                r"no claim discount",
                r"ncd.*\d+%",
                r"discount.*claim"
            ],
            "health_checkup": [
                r"health.*check",
                r"preventive.*health",
                r"checkup.*expenses"
            ],
            "hospital_definition": [
                r"hospital.*definition",
                r"institution.*\d+.*beds",
                r"define.*hospital"
            ],
            "ayush": [
                r"ayush.*treatment",
                r"ayurveda.*coverage",
                r"yoga.*naturopathy"
            ],
            "room_rent": [
                r"room.*rent.*\d+%",
                r"icu.*charges.*\d+%",
                r"daily.*rent.*limit"
            ]
        }
    
    def extract_clauses(self, text: str) -> List[Dict[str, Any]]:
        """Extract relevant clauses from text"""
        clauses = []
        
        # Split text into sentences
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 10:  # Skip very short sentences
                continue
            
            # Check for clause patterns
            clause_type = self._identify_clause_type(sentence)
            if clause_type:
                clauses.append({
                    "text": sentence,
                    "type": clause_type,
                    "confidence": self._calculate_clause_confidence(sentence, clause_type)
                })
        
        return clauses
    
    def _identify_clause_type(self, sentence: str) -> str:
        """Identify the type of clause in a sentence"""
        sentence_lower = sentence.lower()
        
        for clause_type, patterns in self.clause_patterns.items():
            for pattern in patterns:
                if re.search(pattern, sentence_lower):
                    return clause_type
        
        return None
    
    def _calculate_clause_confidence(self, sentence: str, clause_type: str) -> float:
        """Calculate confidence score for clause identification"""
        sentence_lower = sentence.lower()
        patterns = self.clause_patterns.get(clause_type, [])
        
        max_confidence = 0.0
        for pattern in patterns:
            # Calculate similarity with pattern
            similarity = SequenceMatcher(None, sentence_lower, pattern).ratio()
            max_confidence = max(max_confidence, similarity)
        
        return max_confidence
    
    def match_clauses_to_question(self, processed_question: ProcessedQuestion, search_results: List[SearchResult]) -> List[Dict[str, Any]]:
        """Match relevant clauses to a processed question"""
        matched_clauses = []
        
        for result in search_results:
            # Extract clauses from chunk
            clauses = self.extract_clauses(result.chunk.content)
            
            for clause in clauses:
                # Calculate relevance to question
                relevance_score = self._calculate_clause_relevance(clause, processed_question)
                
                if relevance_score > 0.5:  # Threshold for relevance
                    matched_clause = {
                        "clause": clause,
                        "search_result": result,
                        "relevance_score": relevance_score,
                        "source_chunk": result.chunk
                    }
                    matched_clauses.append(matched_clause)
        
        # Sort by relevance score
        matched_clauses.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        return matched_clauses
    
    def _calculate_clause_relevance(self, clause: Dict[str, Any], processed_question: ProcessedQuestion) -> float:
        """Calculate how relevant a clause is to a processed question"""
        clause_text = clause["text"].lower()
        question_terms = [term.lower() for term in processed_question.extracted_terms]
        
        # Check term overlap
        term_matches = sum(1 for term in question_terms if term in clause_text)
        term_score = term_matches / len(question_terms) if question_terms else 0
        
        # Check question type match
        type_match = 0.0
        if clause["type"] == processed_question.question_type.value:
            type_match = 1.0
        elif clause["type"] in processed_question.structured_query.get("entities", []):
            type_match = 0.8
        
        # Check structured query match
        query_score = 0.0
        structured_query = processed_question.structured_query
        for entity in structured_query.get("entities", []):
            if entity.lower() in clause_text:
                query_score += 0.3
        
        for condition in structured_query.get("conditions", []):
            if condition.lower() in clause_text:
                query_score += 0.3
        
        # Combine scores
        final_score = (term_score * 0.4 + type_match * 0.3 + query_score * 0.3)
        
        return min(final_score, 1.0)
    
    def extract_specific_information(self, clause: Dict[str, Any], question_type: str) -> Dict[str, Any]:
        """Extract specific information from a clause based on question type"""
        text = clause["text"]
        
        extracted_info = {
            "text": text,
            "type": question_type,
            "details": {}
        }
        
        if question_type == "grace_period":
            # Extract number of days
            days_match = re.search(r'(\d+)\s*days?', text.lower())
            if days_match:
                extracted_info["details"]["days"] = int(days_match.group(1))
        
        elif question_type == "waiting_period":
            # Extract number of months
            months_match = re.search(r'(\d+)\s*months?', text.lower())
            if months_match:
                extracted_info["details"]["months"] = int(months_match.group(1))
        
        elif question_type == "coverage":
            # Extract coverage details
            coverage_terms = ["cover", "coverage", "include", "provide"]
            for term in coverage_terms:
                if term in text.lower():
                    extracted_info["details"]["coverage_type"] = "included"
                    break
            else:
                extracted_info["details"]["coverage_type"] = "not_mentioned"
        
        elif question_type == "maternity":
            # Extract maternity coverage details
            if any(term in text.lower() for term in ["maternity", "pregnancy", "childbirth"]):
                extracted_info["details"]["maternity_coverage"] = "included"
            else:
                extracted_info["details"]["maternity_coverage"] = "not_mentioned"
        
        elif question_type == "surgery":
            # Extract surgery details
            surgery_types = ["knee", "cataract", "surgery", "operation"]
            for surgery_type in surgery_types:
                if surgery_type in text.lower():
                    extracted_info["details"]["surgery_type"] = surgery_type
                    break
        
        elif question_type == "ncd":
            # Extract NCD percentage
            percentage_match = re.search(r'(\d+)%', text)
            if percentage_match:
                extracted_info["details"]["percentage"] = int(percentage_match.group(1))
        
        elif question_type == "room_rent":
            # Extract room rent limits
            rent_match = re.search(r'(\d+)%', text)
            if rent_match:
                extracted_info["details"]["limit_percentage"] = int(rent_match.group(1))
        
        return extracted_info
    
    def find_best_matches(self, processed_question: ProcessedQuestion, search_results: List[SearchResult], top_k: int = 3) -> List[Dict[str, Any]]:
        """Find the best matching clauses for a question"""
        # Match clauses to question
        matched_clauses = self.match_clauses_to_question(processed_question, search_results)
        
        # Extract specific information
        detailed_matches = []
        for match in matched_clauses[:top_k]:
            detailed_match = self.extract_specific_information(
                match["clause"], 
                processed_question.question_type.value
            )
            detailed_match["relevance_score"] = match["relevance_score"]
            detailed_match["source_chunk"] = match["source_chunk"]
            detailed_matches.append(detailed_match)
        
        return detailed_matches
