import numpy as np
import logging
from typing import List, Optional
from sentence_transformers import SentenceTransformer
import faiss
import pinecone
from urllib.parse import urlparse

from ..models import DocumentChunk, SearchResult
from ..config import Config

logger = logging.getLogger(__name__)

class EmbeddingSearch:
    """Component 3: Embedding Search - FAISS/Pinecone retrieval"""
    
    def __init__(self):
        # Initialize sentence transformer
        self.model = SentenceTransformer(Config.EMBEDDING_MODEL)
        
        # Initialize vector database
        self.use_pinecone = bool(Config.PINECONE_API_KEY)
        if self.use_pinecone:
            self._init_pinecone()
        else:
            self._init_faiss()
    
    def _init_pinecone(self):
        """Initialize Pinecone vector database"""
        try:
            pinecone.init(
                api_key=Config.PINECONE_API_KEY,
                environment=Config.PINECONE_ENVIRONMENT
            )
            
            # Get or create index
            if Config.PINECONE_INDEX_NAME not in pinecone.list_indexes():
                pinecone.create_index(
                    name=Config.PINECONE_INDEX_NAME,
                    dimension=Config.EMBEDDING_DIMENSION,
                    metric="cosine"
                )
            
            self.index = pinecone.Index(Config.PINECONE_INDEX_NAME)
            logger.info("Pinecone initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Pinecone: {e}")
            logger.info("Falling back to FAISS for local vector storage")
            self.use_pinecone = False
            self._init_faiss()
    
    def _init_faiss(self):
        """Initialize FAISS vector database"""
        try:
            self.index = faiss.IndexFlatIP(Config.EMBEDDING_DIMENSION)
            self.chunks = []
            logger.info("FAISS initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize FAISS: {e}")
            raise
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for text"""
        try:
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            raise
    
    def is_known_document(self, url: str) -> bool:
        """Determine if document is known (public) or unknown (private)"""
        # Simple heuristic: check if URL contains known domains
        known_domains = [
            'hackrx.blob.core.windows.net',
            'public.policy.com',
            'insurance.gov',
            'localhost'  # Local development
        ]
        
        # Convert Pydantic URL to string if needed
        url_str = str(url)
        parsed_url = urlparse(url_str)
        domain = parsed_url.netloc.lower()
        
        return any(known_domain in domain for known_domain in known_domains)
    
    def get_document_weight(self, url: str) -> float:
        """Get document weight for scoring"""
        if self.is_known_document(url):
            return Config.KNOWN_DOCUMENT_WEIGHT
        else:
            return Config.UNKNOWN_DOCUMENT_WEIGHT
    
    async def index_chunks(self, chunks: List[DocumentChunk]) -> None:
        """Index document chunks in vector database"""
        try:
            logger.info(f"Indexing {len(chunks)} chunks")
            
            if not chunks:
                logger.warning("No chunks to index - skipping indexing")
                return
            
            # Generate embeddings
            texts = [chunk.content for chunk in chunks]
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            
            # Store embeddings in chunks
            for i, chunk in enumerate(chunks):
                chunk.embedding = embeddings[i].tolist()
            
            if self.use_pinecone:
                await self._index_pinecone(chunks, embeddings)
            else:
                await self._index_faiss(chunks, embeddings)
            
            logger.info("Chunks indexed successfully")
            
        except Exception as e:
            logger.error(f"Failed to index chunks: {e}")
            raise
    
    async def _index_pinecone(self, chunks: List[DocumentChunk], embeddings: np.ndarray):
        """Index chunks in Pinecone"""
        vectors = []
        for i, chunk in enumerate(chunks):
            vectors.append({
                'id': chunk.id,
                'values': embeddings[i].tolist(),
                'metadata': {
                    'content': chunk.content,
                    'document_url': chunk.document_url,
                    'chunk_index': chunk.chunk_index,
                    'page_number': chunk.page_number
                }
            })
        
        # Upsert in batches
        batch_size = 100
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i + batch_size]
            self.index.upsert(vectors=batch)
    
    async def _index_faiss(self, chunks: List[DocumentChunk], embeddings: np.ndarray):
        """Index chunks in FAISS"""
        # Add to FAISS index
        self.index.add(embeddings)
        
        # Store chunks for retrieval
        self.chunks.extend(chunks)
    
    async def search_similar(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """Search for similar chunks"""
        try:
            # Generate query embedding
            query_embedding = self.generate_embedding(query)
            
            if self.use_pinecone:
                results = await self._search_pinecone(query_embedding, top_k)
            else:
                results = await self._search_faiss(query_embedding, top_k)
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to search: {e}")
            raise
    
    async def _search_pinecone(self, query_embedding: np.ndarray, top_k: int) -> List[SearchResult]:
        """Search in Pinecone"""
        results = self.index.query(
            vector=query_embedding.tolist(),
            top_k=top_k,
            include_metadata=True
        )
        
        search_results = []
        for match in results.matches:
            chunk = DocumentChunk(
                id=match.id,
                content=match.metadata['content'],
                document_url=match.metadata['document_url'],
                chunk_index=match.metadata['chunk_index'],
                page_number=match.metadata.get('page_number')
            )
            
            search_result = SearchResult(
                chunk=chunk,
                similarity_score=match.score,
                relevance_score=match.score,
                source_section=None
            )
            search_results.append(search_result)
        
        return search_results
    
    async def _search_faiss(self, query_embedding: np.ndarray, top_k: int) -> List[SearchResult]:
        """Search in FAISS"""
        # Reshape for FAISS
        query_embedding = query_embedding.reshape(1, -1)
        
        # Search
        scores, indices = self.index.search(query_embedding, top_k)
        
        search_results = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx < len(self.chunks):
                chunk = self.chunks[idx]
                search_result = SearchResult(
                    chunk=chunk,
                    similarity_score=float(score),
                    relevance_score=float(score),
                    source_section=None
                )
                search_results.append(search_result)
        
        return search_results
    
    async def search_by_question(self, processed_question, chunks: List[DocumentChunk]) -> List[SearchResult]:
        """Search for chunks relevant to a processed question"""
        try:
            # Create search query from processed question
            query_parts = [
                processed_question.original_question,
                " ".join(processed_question.extracted_terms),
                " ".join(processed_question.structured_query.get("entities", [])),
                " ".join(processed_question.structured_query.get("specific_terms", []))
            ]
            
            search_query = " ".join(filter(None, query_parts))
            
            # Search for similar chunks
            results = await self.search_similar(search_query, top_k=10)
            
            # Filter results by relevance
            relevant_results = []
            for result in results:
                # Check if chunk contains relevant terms
                chunk_text = result.chunk.content.lower()
                relevant_terms = processed_question.extracted_terms
                
                term_matches = sum(1 for term in relevant_terms if term.lower() in chunk_text)
                relevance_score = term_matches / len(relevant_terms) if relevant_terms else 0
                
                # Combine similarity and relevance scores
                combined_score = (result.similarity_score + relevance_score) / 2
                result.relevance_score = combined_score
                
                if combined_score > 0.3:  # Threshold for relevance
                    relevant_results.append(result)
            
            # Sort by combined score
            relevant_results.sort(key=lambda x: x.relevance_score, reverse=True)
            
            return relevant_results[:5]  # Return top 5
            
        except Exception as e:
            logger.error(f"Failed to search by question: {e}")
            return []
