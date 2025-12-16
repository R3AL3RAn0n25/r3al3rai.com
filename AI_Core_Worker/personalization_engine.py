#!/usr/bin/env python3
"""
R3ÆLƎR AI: Personalization Engine
Analyzes user behavior and personalizes responses
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
from collections import Counter
import json
import logging

logger = logging.getLogger(__name__)

# PostgreSQL Configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'r3aler_ai',
    'user': 'r3aler_user_2025',
    'password': 'R3AL3RAdmin816'
}

def get_connection():
    """Get database connection"""
    return psycopg2.connect(**DB_CONFIG)

class PersonalizationEngine:
    """AI-powered personalization based on user behavior"""
    
    @staticmethod
    def get_user_profile(user_id):
        """
        Build comprehensive user profile from activity history
        Returns dict with user preferences, interests, skill level, etc.
        """
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            # Get user info
            cursor.execute("""
                SELECT user_id, username, subscription_tier, preferences, created_at
                FROM user_unit.profiles
                WHERE user_id = %s
            """, (user_id,))
            
            user_info = cursor.fetchone()
            if not user_info:
                return None
            
            profile = dict(user_info)
            
            # Analyze search history
            cursor.execute("""
                SELECT activity_data
                FROM user_unit.activity_log
                WHERE user_id = %s
                AND activity_type IN ('knowledge_search', 'tool_search')
                AND timestamp > NOW() - INTERVAL '90 days'
                ORDER BY timestamp DESC
                LIMIT 200
            """, (user_id,))
            
            searches = [row['activity_data'] for row in cursor.fetchall()]
            
            # Extract search queries
            queries = [s.get('query', '').lower() for s in searches if s.get('query')]
            
            # Analyze clicked/viewed items
            cursor.execute("""
                SELECT activity_data
                FROM user_unit.activity_log
                WHERE user_id = %s
                AND activity_type IN ('knowledge_click', 'tool_view')
                AND timestamp > NOW() - INTERVAL '90 days'
                LIMIT 200
            """, (user_id,))
            
            clicks = [row['activity_data'] for row in cursor.fetchall()]
            
            # Get tool preferences
            cursor.execute("""
                SELECT tool_id, usage_count, is_pinned
                FROM user_unit.tool_preferences
                WHERE user_id = %s
                ORDER BY usage_count DESC
                LIMIT 50
            """, (user_id,))
            
            tools = [dict(row) for row in cursor.fetchall()]
            
            # Build preference profile
            profile['ai_profile'] = PersonalizationEngine._analyze_behavior(
                queries, clicks, tools
            )
            
            return profile
            
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def _analyze_behavior(queries, clicks, tools):
        """Analyze user behavior to extract preferences"""
        
        # Topic extraction from queries
        topic_keywords = {
            'crypto': ['bitcoin', 'cryptocurrency', 'blockchain', 'wallet', 'crypto', 'ethereum', 'mining'],
            'network': ['network', 'nmap', 'scan', 'port', 'tcp', 'ip', 'packet', 'wifi', 'wireless'],
            'security': ['security', 'vulnerability', 'exploit', 'hack', 'penetration', 'test'],
            'web': ['web', 'http', 'sql', 'injection', 'xss', 'burp', 'webapp'],
            'forensics': ['forensic', 'investigation', 'evidence', 'recovery', 'analysis'],
            'password': ['password', 'crack', 'hash', 'brute', 'wordlist'],
            'physics': ['physics', 'quantum', 'energy', 'force', 'mechanics'],
            'space': ['space', 'astronomy', 'planet', 'star', 'galaxy', 'exoplanet']
        }
        
        # Count topic occurrences
        topic_counts = Counter()
        for query in queries:
            for topic, keywords in topic_keywords.items():
                if any(kw in query for kw in keywords):
                    topic_counts[topic] += 1
        
        # Get top interests
        top_interests = [topic for topic, count in topic_counts.most_common(5)]
        
        # Infer skill level based on query complexity and tool usage
        skill_level = PersonalizationEngine._infer_skill_level(queries, tools)
        
        # Detect learning patterns
        learning_style = PersonalizationEngine._detect_learning_style(clicks)
        
        # Calculate activity frequency
        activity_frequency = 'active' if len(queries) > 20 else 'moderate' if len(queries) > 5 else 'new'
        
        return {
            'top_interests': top_interests,
            'skill_level': skill_level,
            'learning_style': learning_style,
            'activity_frequency': activity_frequency,
            'total_searches': len(queries),
            'total_clicks': len(clicks),
            'favorite_tools_count': len([t for t in tools if t.get('usage_count', 0) > 2]),
            'last_analysis': datetime.now().isoformat()
        }
    
    @staticmethod
    def _infer_skill_level(queries, tools):
        """Infer user skill level from behavior"""
        
        beginner_keywords = ['tutorial', 'how to', 'basics', 'introduction', 'guide', 'simple']
        intermediate_keywords = ['advanced', 'technique', 'method', 'custom', 'configure']
        expert_keywords = ['exploit', 'bypass', 'reverse', 'assembly', 'kernel', 'zero-day']
        
        beginner_count = sum(1 for q in queries if any(kw in q.lower() for kw in beginner_keywords))
        intermediate_count = sum(1 for q in queries if any(kw in q.lower() for kw in intermediate_keywords))
        expert_count = sum(1 for q in queries if any(kw in q.lower() for kw in expert_keywords))
        
        # Tool complexity indicator
        advanced_tools = sum(1 for t in tools if t.get('usage_count', 0) > 5)
        
        total = beginner_count + intermediate_count + expert_count + advanced_tools
        if total == 0:
            return 'beginner'
        
        if expert_count > intermediate_count or advanced_tools > 10:
            return 'expert'
        elif intermediate_count > beginner_count or advanced_tools > 5:
            return 'intermediate'
        else:
            return 'beginner'
    
    @staticmethod
    def _detect_learning_style(clicks):
        """Detect how user prefers to learn"""
        
        if len(clicks) < 5:
            return 'explorer'  # New user, still exploring
        
        # Check if user clicks top results or browses deep
        top_clicks = sum(1 for c in clicks if c.get('position', 99) <= 3)
        deep_clicks = sum(1 for c in clicks if c.get('position', 0) > 5)
        
        if deep_clicks > top_clicks:
            return 'thorough'  # Reads many results
        elif top_clicks > deep_clicks * 2:
            return 'focused'  # Clicks top results only
        else:
            return 'balanced'  # Mix of both
    
    @staticmethod
    def personalize_search_results(results, user_id):
        """
        Adjust search results based on user profile
        Boosts relevant results, filters by skill level
        """
        if not user_id:
            return results  # No personalization for anonymous users
        
        profile = PersonalizationEngine.get_user_profile(user_id)
        if not profile or 'ai_profile' not in profile:
            return results
        
        ai_profile = profile['ai_profile']
        top_interests = ai_profile.get('top_interests', [])
        skill_level = ai_profile.get('skill_level', 'beginner')
        
        # Apply personalization to each result
        for result in results:
            original_score = result.get('relevance_score', 0)
            boost = 1.0
            
            # Boost based on user interests
            result_category = result.get('category', '').lower()
            result_content = (result.get('content', '') + ' ' + result.get('description', '')).lower()
            
            for interest in top_interests:
                if interest in result_category or interest in result_content:
                    boost *= 1.5
                    break
            
            # Adjust for skill level match
            result_skill = result.get('skill_level', 'intermediate')
            if result_skill == skill_level:
                boost *= 1.3
            elif result_skill == 'expert' and skill_level == 'beginner':
                boost *= 0.5  # Penalize too advanced content for beginners
            
            # Apply boost
            result['relevance_score'] = original_score * boost
            result['personalized'] = boost != 1.0
            result['boost_factor'] = boost
        
        # Re-sort by adjusted relevance
        results.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        return results
    
    @staticmethod
    def get_personalized_greeting(user_id):
        """Generate personalized greeting message"""
        profile = PersonalizationEngine.get_user_profile(user_id)
        if not profile:
            return "Welcome to R3ÆLƎR AI!"
        
        username = profile.get('username', 'User')
        ai_profile = profile.get('ai_profile', {})
        
        top_interests = ai_profile.get('top_interests', [])
        activity_freq = ai_profile.get('activity_frequency', 'new')
        
        if activity_freq == 'new':
            return f"Welcome, {username}! Let's explore R3ÆLƎR AI together."
        
        if top_interests:
            interest_str = ', '.join(top_interests[:2])
            return f"Welcome back, {username}! Ready to explore {interest_str}?"
        
        return f"Welcome back, {username}!"
    
    @staticmethod
    def suggest_next_topics(user_id, limit=5):
        """Suggest topics user might be interested in"""
        profile = PersonalizationEngine.get_user_profile(user_id)
        if not profile or 'ai_profile' not in profile:
            return []
        
        ai_profile = profile['ai_profile']
        top_interests = ai_profile.get('top_interests', [])
        skill_level = ai_profile.get('skill_level', 'beginner')
        
        # Topic progression map
        topic_progression = {
            'network': {
                'beginner': ['Network basics', 'TCP/IP fundamentals', 'Nmap basics'],
                'intermediate': ['Advanced port scanning', 'Network traffic analysis', 'Wireshark mastery'],
                'expert': ['Custom packet crafting', 'Network exploit development', 'IDS/IPS evasion']
            },
            'crypto': {
                'beginner': ['Cryptocurrency basics', 'Wallet security', 'Bitcoin fundamentals'],
                'intermediate': ['Blockchain analysis', 'Smart contract security', 'Privacy coins'],
                'expert': ['Cryptanalysis', 'Zero-knowledge proofs', 'DeFi exploit research']
            },
            'web': {
                'beginner': ['Web security basics', 'SQL injection intro', 'XSS fundamentals'],
                'intermediate': ['Advanced SQL injection', 'CSRF attacks', 'Authentication bypass'],
                'expert': ['Prototype pollution', 'Server-side template injection', 'Deserialization attacks']
            }
        }
        
        suggestions = []
        for interest in top_interests[:3]:
            if interest in topic_progression:
                suggestions.extend(topic_progression[interest].get(skill_level, []))
        
        return suggestions[:limit]
    
    @staticmethod
    def get_adaptive_explanation_level(user_id):
        """Determine how technical explanations should be"""
        profile = PersonalizationEngine.get_user_profile(user_id)
        if not profile or 'ai_profile' not in profile:
            return 'intermediate'
        
        return profile['ai_profile'].get('skill_level', 'intermediate')

# Convenience functions
get_user_profile = PersonalizationEngine.get_user_profile
personalize_search_results = PersonalizationEngine.personalize_search_results
get_personalized_greeting = PersonalizationEngine.get_personalized_greeting
suggest_next_topics = PersonalizationEngine.suggest_next_topics
get_adaptive_explanation_level = PersonalizationEngine.get_adaptive_explanation_level
