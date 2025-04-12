from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from utils.prompts import SOURCING_PROMPT
from utils.database import VectorDatabase
import os
from typing import Dict, List, Any
from dotenv import load_dotenv
load_dotenv()




class SourcingAgent:
    def __init__(self):
        self.llm = ChatGroq(
            model_name="gemma2-9b-it",
            temperature=0.7,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
        self.chain = SOURCING_PROMPT | self.llm
        self.db = VectorDatabase()

    def source_candidates(self, job_description: str, requirements: str) -> Dict[str, Any]:
        """Generate search queries and find potential candidates"""
        response = self.chain.invoke({
            "job_description": job_description,
            "requirements": requirements
        })
        
        search_queries = response.content if hasattr(response, 'content') else str(response)

        candidates = []
        for query in search_queries.split('\n'):
            if query.strip():
                results = self.db.search_candidates(query)
                if results and 'ids' in results:
                    # Ensure we have lists for all required fields
                    ids = results.get('ids', [])
                    documents = results.get('documents', [])
                    metadatas = results.get('metadatas', [])
                    distances = results.get('distances', [])
                    
                    # Process each result
                    for i in range(len(ids)):
                        # Convert ID to string if it's a list
                        doc_id = str(ids[i]) if isinstance(ids[i], list) else str(ids[i])
                        
                        candidate = {
                            'id': doc_id,
                            'document': documents[i] if i < len(documents) else '',
                            'metadata': metadatas[i] if i < len(metadatas) else {},
                            'distance': distances[i] if i < len(distances) else 0
                        }
                        candidates.append(candidate)

        # Remove duplicates using string IDs
        unique_candidates = {}
        for candidate in candidates:
            candidate_id = str(candidate['id'])
            if candidate_id not in unique_candidates:
                unique_candidates[candidate_id] = candidate

        return {
            "search_queries": search_queries,
            "candidates": list(unique_candidates.values())
        }

    def add_candidate_to_database(self, candidate_id: str, resume_text: str, metadata: Dict[str, Any]):
        """Add a new candidate to the database"""
        self.db.add_candidate(candidate_id, resume_text, metadata) 