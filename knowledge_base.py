"""
Knowledge Base for R3ÆLƎR AI
Enhanced wrapper around the storage facility with advanced indexing and search
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import requests
import time

logger = logging.getLogger(__name__)

class KnowledgeBase:
    """
    Enhanced knowledge base with advanced search and indexing capabilities
    """

    def __init__(self):
        self.storage_url = "http://localhost:3003"  # Storage facility URL
        self.index_cache = {}
        self.search_cache = {}
        self.cache_timeout = 300  # 5 minutes

        # Initialize connection
        self._test_connection()

        logger.info("Knowledge base initialized")

    def _test_connection(self):
        """Test connection to storage facility"""
        try:
            response = requests.get(f"{self.storage_url}/health", timeout=5)
            if response.status_code == 200:
                logger.info("Storage facility connection established")
            else:
                logger.warning(f"Storage facility returned status {response.status_code}")
        except Exception as e:
            logger.error(f"Failed to connect to storage facility: {e}")

    def search(self, query: str, user_id: str = 'anonymous', max_results: int = 5) -> List[Dict]:
        """Enhanced search with caching and advanced filtering"""

        # Check cache first
        cache_key = f"{query}_{user_id}_{max_results}"
        if cache_key in self.search_cache:
            cached_result, timestamp = self.search_cache[cache_key]
            if time.time() - timestamp < self.cache_timeout:
                return cached_result

        try:
            # Perform search against storage facility
            search_payload = {
                'query': query,
                'user_id': user_id,
                'max_results': max_results
            }

            response = requests.post(
                f"{self.storage_url}/api/facility/search",
                json=search_payload,
                timeout=10
            )

            if response.status_code == 200:
                results = response.json()

                # Enhance results with metadata
                enhanced_results = self._enhance_results(results, query)

                # Cache results
                self.search_cache[cache_key] = (enhanced_results, time.time())

                return enhanced_results
            else:
                logger.error(f"Search failed with status {response.status_code}")
                return []

        except Exception as e:
            logger.error(f"Search error: {e}")
            return []

    def _enhance_results(self, results: List[Dict], query: str) -> List[Dict]:
        """Enhance search results with additional metadata"""
        enhanced = []

        for result in results:
            if isinstance(result, dict):
                enhanced_result = result.copy()

                # Add relevance score
                enhanced_result['relevance_score'] = self._calculate_relevance(
                    result, query
                )

                # Add domain classification
                enhanced_result['domain'] = self._classify_domain(result)

                # Add freshness indicator
                enhanced_result['freshness'] = self._calculate_freshness(result)

                enhanced.append(enhanced_result)

        # Sort by relevance
        enhanced.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)

        return enhanced

    def _calculate_relevance(self, result: Dict, query: str) -> float:
        """Calculate relevance score for result"""
        score = 0.0

        content = result.get('content', '').lower()
        query_lower = query.lower()

        # Exact matches get highest score
        if query_lower in content:
            score += 1.0

        # Partial matches
        query_words = query_lower.split()
        content_words = content.split()

        matching_words = sum(1 for word in query_words if word in content_words)
        if query_words:
            score += matching_words / len(query_words) * 0.5

        # Domain relevance bonus
        domain = self._classify_domain(result)
        if domain in query_lower:
            score += 0.3

        return min(score, 1.0)  # Cap at 1.0

    def _classify_domain(self, result: Dict) -> str:
        """Classify the domain of a knowledge result"""
        content = result.get('content', '').lower()

        domains = {
            'physics': ['physics', 'quantum', 'mechanics', 'thermodynamics'],
            'cryptocurrency': ['bitcoin', 'crypto', 'blockchain', 'wallet'],
            'space': ['space', 'astronomy', 'nasa', 'satellite', 'exoplanet'],
            'medical': ['medical', 'health', 'disease', 'treatment'],
            'programming': ['code', 'programming', 'algorithm', 'function']
        }

        for domain, keywords in domains.items():
            if any(keyword in content for keyword in keywords):
                return domain

        return 'general'

    def _calculate_freshness(self, result: Dict) -> str:
        """Calculate how fresh the knowledge is"""
        # This would use timestamps in a real implementation
        # For now, return a simple indicator
        return "current"

    def store_knowledge(self, content: str, domain: str, metadata: Dict = None) -> bool:
        """Store new knowledge in the knowledge base"""

        try:
            store_payload = {
                'content': content,
                'domain': domain,
                'metadata': metadata or {},
                'timestamp': datetime.now().isoformat()
            }

            response = requests.post(
                f"{self.storage_url}/api/kb/store",
                json=store_payload,
                timeout=10
            )

            if response.status_code == 200:
                # Clear relevant caches
                self._clear_caches()
                logger.info(f"Knowledge stored successfully in domain: {domain}")
                return True
            else:
                logger.error(f"Failed to store knowledge: {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"Knowledge storage error: {e}")
            return False

    def get_domain_stats(self) -> Dict[str, Any]:
        """Get statistics about knowledge domains"""
        try:
            response = requests.get(f"{self.storage_url}/api/kb/stats", timeout=5)

            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Failed to get stats: {response.status_code}"}

        except Exception as e:
            logger.error(f"Stats retrieval error: {e}")
            return {"error": str(e)}

    def _clear_caches(self):
        """Clear search and index caches"""
        self.search_cache.clear()
        self.index_cache.clear()

    def optimize(self):
        """Optimize knowledge base performance"""
        logger.info("Optimizing knowledge base...")

        # Clear old cache entries
        current_time = time.time()
        self.search_cache = {
            k: v for k, v in self.search_cache.items()
            if current_time - v[1] < self.cache_timeout
        }

        # Rebuild indexes if needed
        self._rebuild_indexes()

        logger.info("Knowledge base optimization completed")

    def _rebuild_indexes(self):
        """Rebuild search indexes for better performance"""
        # This would implement actual index rebuilding
        # For now, just clear and rebuild cache
        self.index_cache.clear()

    def get_status(self) -> Dict[str, Any]:
        """Get knowledge base status"""
        try:
            response = requests.get(f"{self.storage_url}/health", timeout=5)
            connected = response.status_code == 200
        except:
            connected = False

        return {
            "component": "KnowledgeBase",
            "storage_connected": connected,
            "cache_size": len(self.search_cache),
            "index_size": len(self.index_cache),
            "status": "active" if connected else "disconnected"
        }