import chromadb
from chromadb.config import Settings
import os
from typing import List, Dict, Any

class VectorDatabase:
    def __init__(self):
        # Create a persistent client with the new configuration
        self.client = chromadb.PersistentClient(
            path="data/chroma_db"
        )
        
        # Get or create collections
        self.candidates_collection = self.client.get_or_create_collection(
            name="candidates"
        )
        self.jobs_collection = self.client.get_or_create_collection(
            name="jobs"
        )

    def add_candidate(self, candidate_id: str, resume_text: str, metadata: Dict[str, Any]):
        """Add a candidate's resume to the vector database"""
        self.candidates_collection.add(
            documents=[resume_text],
            metadatas=[metadata],
            ids=[candidate_id]
        )

    def add_job(self, job_id: str, job_description: str, metadata: Dict[str, Any]):
        """Add a job description to the vector database"""
        self.jobs_collection.add(
            documents=[job_description],
            metadatas=[metadata],
            ids=[job_id]
        )

    def search_candidates(self, query: str, n_results: int = 5) -> Dict[str, Any]:
        """Search for candidates matching a query"""
        try:
            results = self.candidates_collection.query(
                query_texts=[query],
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )
            return results
        except Exception as e:
            print(f"Error searching candidates: {e}")
            return {
                "ids": [],
                "documents": [],
                "metadatas": [],
                "distances": []
            }

    def search_jobs(self, query: str, n_results: int = 5) -> Dict[str, Any]:
        """Search for jobs matching a query"""
        try:
            results = self.jobs_collection.query(
                query_texts=[query],
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )
            return results
        except Exception as e:
            print(f"Error searching jobs: {e}")
            return {
                "ids": [],
                "documents": [],
                "metadatas": [],
                "distances": []
            }

    def get_candidate(self, candidate_id: str) -> Dict[str, Any]:
        """Get a specific candidate's information"""
        try:
            result = self.candidates_collection.get(
                ids=[candidate_id],
                include=["documents", "metadatas"]
            )
            return result
        except Exception as e:
            print(f"Error getting candidate: {e}")
            return {
                "ids": [],
                "documents": [],
                "metadatas": []
            }

    def get_job(self, job_id: str) -> Dict[str, Any]:
        """Get a specific job's information"""
        try:
            result = self.jobs_collection.get(
                ids=[job_id],
                include=["documents", "metadatas"]
            )
            return result
        except Exception as e:
            print(f"Error getting job: {e}")
            return {
                "ids": [],
                "documents": [],
                "metadatas": []
            } 