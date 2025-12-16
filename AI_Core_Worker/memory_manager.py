"""
Memory Manager for R3ÆLƎR AI
Advanced memory management with short-term and long-term memory capabilities
"""

import logging
import time
import json
import hashlib
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict, deque
import threading

logger = logging.getLogger(__name__)

class MemoryManager:
    """
    Advanced memory management system for AI context and learning
    """

    def __init__(self):
        self.short_term_memory = {}
        self.long_term_memory = {}
        self.conversation_history = defaultdict(list)
        self.user_profiles = {}
        self.memory_lock = threading.Lock()

        # Memory limits
        self.max_short_term_items = 1000
        self.max_long_term_items = 10000
        self.max_conversation_length = 50
        self.memory_decay_hours = 24

        logger.info("Memory manager initialized")

    def store_interaction(self, user_id: str, query: str, response: str):
        """Store user interaction in memory"""

        with self.memory_lock:
            timestamp = datetime.now()
            interaction = {
                'timestamp': timestamp.isoformat(),
                'query': query,
                'response': response,
                'user_id': user_id
            }

            # Store in conversation history
            if len(self.conversation_history[user_id]) >= self.max_conversation_length:
                self.conversation_history[user_id].pop(0)  # Remove oldest

            self.conversation_history[user_id].append(interaction)

            # Store in short-term memory
            self._store_short_term(user_id, interaction)

            # Check if should promote to long-term memory
            self._check_long_term_promotion(user_id, interaction)

    def get_context(self, user_id: str, current_query: str) -> str:
        """Get relevant context for current query"""

        with self.memory_lock:
            context_parts = []

            # Get recent conversation context
            recent_interactions = self.conversation_history.get(user_id, [])[-5:]  # Last 5 interactions

            if recent_interactions:
                context_parts.append("Recent conversation:")
                for interaction in recent_interactions:
                    context_parts.append(f"Q: {interaction['query'][:100]}...")
                    context_parts.append(f"A: {interaction['response'][:100]}...")
                context_parts.append("")

            # Get relevant short-term memories
            short_term_context = self._get_short_term_context(user_id, current_query)
            if short_term_context:
                context_parts.append("Relevant memories:")
                context_parts.extend(short_term_context)
                context_parts.append("")

            # Get user profile context
            profile_context = self._get_user_profile_context(user_id)
            if profile_context:
                context_parts.append("User preferences:")
                context_parts.append(profile_context)
                context_parts.append("")

            return '\n'.join(context_parts).strip()

    def _store_short_term(self, user_id: str, interaction: Dict):
        """Store interaction in short-term memory"""

        if user_id not in self.short_term_memory:
            self.short_term_memory[user_id] = deque(maxlen=self.max_short_term_items)

        self.short_term_memory[user_id].append(interaction)

        # Clean up if over limit
        while len(self.short_term_memory[user_id]) > self.max_short_term_items:
            self.short_term_memory[user_id].popleft()

    def _get_short_term_context(self, user_id: str, current_query: str) -> List[str]:
        """Get relevant short-term memories for current query"""

        if user_id not in self.short_term_memory:
            return []

        relevant_memories = []
        query_lower = current_query.lower()

        for memory in reversed(list(self.short_term_memory[user_id])):
            memory_query = memory.get('query', '').lower()
            memory_response = memory.get('response', '').lower()

            # Check relevance
            if self._calculate_relevance(query_lower, memory_query + " " + memory_response) > 0.3:
                relevant_memories.append(f"Previous: {memory['query'][:50]}... -> {memory['response'][:50]}...")

                if len(relevant_memories) >= 3:  # Limit to 3 relevant memories
                    break

        return relevant_memories

    def _calculate_relevance(self, query1: str, query2: str) -> float:
        """Calculate relevance between two queries/texts"""

        words1 = set(query1.split())
        words2 = set(query2.split())

        if not words1 or not words2:
            return 0.0

        intersection = words1 & words2
        union = words1 | words2

        return len(intersection) / len(union)

    def _check_long_term_promotion(self, user_id: str, interaction: Dict):
        """Check if interaction should be promoted to long-term memory"""

        # Simple heuristic: interactions that are referenced multiple times
        # or contain important keywords

        query = interaction.get('query', '').lower()

        # Check for important topics
        important_keywords = [
            'learn', 'remember', 'important', 'key', 'essential',
            'physics', 'quantum', 'cryptocurrency', 'space', 'medical'
        ]

        if any(keyword in query for keyword in important_keywords):
            self._promote_to_long_term(user_id, interaction)

        # Check frequency of similar queries
        similar_count = self._count_similar_queries(user_id, query)
        if similar_count >= 3:  # Asked similar question 3+ times
            self._promote_to_long_term(user_id, interaction)

    def _count_similar_queries(self, user_id: str, query: str) -> int:
        """Count how many similar queries user has made"""

        if user_id not in self.short_term_memory:
            return 0

        count = 0
        for memory in self.short_term_memory[user_id]:
            if self._calculate_relevance(query, memory.get('query', '')) > 0.7:
                count += 1

        return count

    def _promote_to_long_term(self, user_id: str, interaction: Dict):
        """Promote interaction to long-term memory"""

        if user_id not in self.long_term_memory:
            self.long_term_memory[user_id] = {}

        # Use query as key (simplified)
        key = hashlib.md5(interaction['query'].encode()).hexdigest()[:8]

        self.long_term_memory[user_id][key] = {
            **interaction,
            'promoted_at': datetime.now().isoformat(),
            'access_count': 0
        }

        # Clean up long-term memory if over limit
        if len(self.long_term_memory[user_id]) > self.max_long_term_items:
            # Remove least accessed items
            sorted_items = sorted(
                self.long_term_memory[user_id].items(),
                key=lambda x: x[1].get('access_count', 0)
            )
            items_to_remove = sorted_items[:100]  # Remove 100 least accessed

            for key, _ in items_to_remove:
                del self.long_term_memory[user_id][key]

    def update_user_profile(self, user_id: str, preferences: Dict):
        """Update user profile with preferences and behavior patterns"""

        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {
                'created': datetime.now().isoformat(),
                'preferences': {},
                'behavior_patterns': {}
            }

        # Update preferences
        self.user_profiles[user_id]['preferences'].update(preferences)
        self.user_profiles[user_id]['last_updated'] = datetime.now().isoformat()

    def _get_user_profile_context(self, user_id: str) -> str:
        """Get user profile context"""

        if user_id not in self.user_profiles:
            return ""

        profile = self.user_profiles[user_id]
        preferences = profile.get('preferences', {})

        context_parts = []
        if preferences:
            context_parts.append(f"User interests: {', '.join(preferences.keys())}")

        return ' '.join(context_parts)

    def get_memory_stats(self, user_id: str = None) -> Dict[str, Any]:
        """Get memory statistics"""

        stats = {
            'total_users': len(self.conversation_history),
            'total_short_term_memories': sum(len(mem) for mem in self.short_term_memory.values()),
            'total_long_term_memories': sum(len(mem) for mem in self.long_term_memory.values()),
            'total_user_profiles': len(self.user_profiles)
        }

        if user_id:
            stats['user_conversations'] = len(self.conversation_history.get(user_id, []))
            stats['user_short_term'] = len(self.short_term_memory.get(user_id, deque()))
            stats['user_long_term'] = len(self.long_term_memory.get(user_id, {}))
            stats['user_profile'] = user_id in self.user_profiles

        return stats

    def cleanup(self):
        """Clean up expired and irrelevant memories"""

        with self.memory_lock:
            logger.info("Starting memory cleanup...")

            current_time = datetime.now()
            cutoff_time = current_time - timedelta(hours=self.memory_decay_hours)

            # Clean short-term memory (remove very old entries)
            for user_id in list(self.short_term_memory.keys()):
                # Keep only recent entries, remove older ones beyond our maxlen
                # The deque automatically handles this, but we can be more aggressive
                pass

            # Clean long-term memory (remove least accessed)
            for user_id in list(self.long_term_memory.keys()):
                memories = self.long_term_memory[user_id]

                # Remove memories not accessed in decay period
                to_remove = []
                for key, memory in memories.items():
                    last_access = memory.get('last_access')
                    if last_access:
                        access_time = datetime.fromisoformat(last_access)
                        if current_time - access_time > timedelta(hours=self.memory_decay_hours):
                            to_remove.append(key)

                for key in to_remove:
                    del memories[key]

                # If user has no long-term memories left, remove user entry
                if not memories:
                    del self.long_term_memory[user_id]

            logger.info("Memory cleanup completed")

    def export_memory(self, user_id: str) -> Dict[str, Any]:
        """Export user's memory for backup/analysis"""

        return {
            'conversation_history': list(self.conversation_history.get(user_id, [])),
            'short_term_memory': list(self.short_term_memory.get(user_id, deque())),
            'long_term_memory': dict(self.long_term_memory.get(user_id, {})),
            'user_profile': self.user_profiles.get(user_id, {}),
            'export_timestamp': datetime.now().isoformat()
        }

    def import_memory(self, user_id: str, memory_data: Dict):
        """Import user's memory from backup"""

        with self.memory_lock:
            if 'conversation_history' in memory_data:
                self.conversation_history[user_id] = memory_data['conversation_history']

            if 'short_term_memory' in memory_data:
                self.short_term_memory[user_id] = deque(
                    memory_data['short_term_memory'],
                    maxlen=self.max_short_term_items
                )

            if 'long_term_memory' in memory_data:
                self.long_term_memory[user_id] = memory_data['long_term_memory']

            if 'user_profile' in memory_data:
                self.user_profiles[user_id] = memory_data['user_profile']

            logger.info(f"Imported memory for user: {user_id}")

    def optimize(self):
        """Optimize memory management"""

        logger.info("Optimizing memory management...")

        # Run cleanup
        self.cleanup()

        # Optimize data structures
        # This could include compressing old memories, rebuilding indexes, etc.

        logger.info("Memory optimization completed")

    def get_status(self) -> Dict[str, Any]:
        """Get memory manager status"""

        return {
            "component": "MemoryManager",
            **self.get_memory_stats(),
            "status": "active"
        }