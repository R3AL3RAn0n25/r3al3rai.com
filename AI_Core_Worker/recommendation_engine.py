#!/usr/bin/env python3
"""
R3ÆLƎR AI: Recommendation Engine
Smart suggestions based on user behavior patterns
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
from collections import Counter, defaultdict
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

class RecommendationEngine:
    """AI-powered recommendations for tools, topics, and learning paths"""
    
    @staticmethod
    def get_tool_recommendations(user_id, limit=5):
        """Recommend tools based on user's searches and interests"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            # Get user's recent search queries
            cursor.execute("""
                SELECT activity_data->>'query' as query
                FROM user_unit.activity_log
                WHERE user_id = %s
                AND activity_type IN ('knowledge_search', 'tool_search')
                AND timestamp > NOW() - INTERVAL '30 days'
                LIMIT 50
            """, (user_id,))
            
            queries = [row['query'].lower() for row in cursor.fetchall() if row['query']]
            
            # Get tools user hasn't used yet
            cursor.execute("""
                SELECT 
                    t.tool_id, t.name, t.category, t.description,
                    t.skill_level, t.usage_example
                FROM blackarch_unit.tools t
                LEFT JOIN user_unit.tool_preferences tp 
                    ON t.tool_id = tp.tool_id AND tp.user_id = %s
                WHERE tp.tool_id IS NULL
            """, (user_id,))
            
            available_tools = [dict(row) for row in cursor.fetchall()]
            
            # Score each tool based on user's search history
            scored_tools = []
            for tool in available_tools:
                score = RecommendationEngine._score_tool_relevance(
                    tool, queries
                )
                if score > 0:
                    tool['recommendation_score'] = score
                    tool['reason'] = RecommendationEngine._explain_recommendation(tool, queries)
                    scored_tools.append(tool)
            
            # Sort by score
            scored_tools.sort(key=lambda x: x['recommendation_score'], reverse=True)
            
            return scored_tools[:limit]
            
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def _score_tool_relevance(tool, user_queries):
        """Score how relevant a tool is to user's queries"""
        score = 0
        tool_text = (tool['name'] + ' ' + tool['description'] + ' ' + 
                     tool.get('category', '')).lower()
        
        for query in user_queries:
            query_words = query.split()
            matches = sum(1 for word in query_words if len(word) > 3 and word in tool_text)
            score += matches * 2
        
        return score
    
    @staticmethod
    def _explain_recommendation(tool, queries):
        """Generate explanation for why tool is recommended"""
        # Find matching queries
        tool_text = (tool['name'] + ' ' + tool['description']).lower()
        matching_queries = []
        
        for query in queries[:10]:  # Check recent queries
            if any(word in tool_text for word in query.split() if len(word) > 3):
                matching_queries.append(query)
        
        if matching_queries:
            return f"Matches your search for '{matching_queries[0]}'"
        
        return f"Popular in {tool['category']} category"
    
    @staticmethod
    def get_learning_path(user_id):
        """Suggest personalized learning path"""
        from personalization_engine import PersonalizationEngine
        
        profile = PersonalizationEngine.get_user_profile(user_id)
        if not profile or 'ai_profile' not in profile:
            return RecommendationEngine._default_learning_path()
        
        ai_profile = profile['ai_profile']
        interests = ai_profile.get('top_interests', [])
        skill_level = ai_profile.get('skill_level', 'beginner')
        
        # Build custom learning path
        path = {
            'user_skill_level': skill_level,
            'recommended_track': interests[0] if interests else 'general',
            'next_steps': []
        }
        
        if skill_level == 'beginner':
            path['next_steps'] = [
                {'step': 1, 'topic': 'Fundamentals', 'estimated_time': '2 weeks'},
                {'step': 2, 'topic': 'Basic Tools', 'estimated_time': '2 weeks'},
                {'step': 3, 'topic': 'Practice Labs', 'estimated_time': '4 weeks'}
            ]
        elif skill_level == 'intermediate':
            path['next_steps'] = [
                {'step': 1, 'topic': 'Advanced Techniques', 'estimated_time': '3 weeks'},
                {'step': 2, 'topic': 'Real-world Scenarios', 'estimated_time': '4 weeks'},
                {'step': 3, 'topic': 'Certification Prep', 'estimated_time': '6 weeks'}
            ]
        else:  # expert
            path['next_steps'] = [
                {'step': 1, 'topic': 'Research & Development', 'estimated_time': 'ongoing'},
                {'step': 2, 'topic': 'Exploit Development', 'estimated_time': 'ongoing'},
                {'step': 3, 'topic': 'Contribute to Community', 'estimated_time': 'ongoing'}
            ]
        
        return path
    
    @staticmethod
    def _default_learning_path():
        """Default learning path for new users"""
        return {
            'user_skill_level': 'beginner',
            'recommended_track': 'general',
            'next_steps': [
                {'step': 1, 'topic': 'Introduction to R3ÆLƎR AI', 'estimated_time': '1 week'},
                {'step': 2, 'topic': 'Knowledge Base Exploration', 'estimated_time': '1 week'},
                {'step': 3, 'topic': 'Tool Discovery', 'estimated_time': '2 weeks'}
            ]
        }
    
    @staticmethod
    def get_related_topics(user_id, current_topic, limit=5):
        """Suggest related topics based on user's history"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            # Find what other users with similar interests searched
            cursor.execute("""
                WITH similar_users AS (
                    SELECT DISTINCT user_id
                    FROM user_unit.activity_log
                    WHERE activity_data->>'query' ILIKE %s
                    AND user_id != %s
                    LIMIT 20
                )
                SELECT activity_data->>'query' as related_query, COUNT(*) as popularity
                FROM user_unit.activity_log
                WHERE user_id IN (SELECT user_id FROM similar_users)
                AND activity_type IN ('knowledge_search', 'tool_search')
                AND activity_data->>'query' IS NOT NULL
                AND activity_data->>'query' NOT ILIKE %s
                GROUP BY activity_data->>'query'
                ORDER BY popularity DESC
                LIMIT %s
            """, (f'%{current_topic}%', user_id, f'%{current_topic}%', limit))
            
            related = [
                {'topic': row['related_query'], 'popularity': row['popularity']}
                for row in cursor.fetchall()
            ]
            
            return related
            
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_trending_topics(days=7, limit=10):
        """Get trending search topics across all users"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cursor.execute("""
                SELECT 
                    activity_data->>'query' as topic,
                    COUNT(*) as search_count,
                    COUNT(DISTINCT user_id) as unique_users
                FROM user_unit.activity_log
                WHERE activity_type IN ('knowledge_search', 'tool_search')
                AND timestamp > NOW() - INTERVAL '%s days'
                AND activity_data->>'query' IS NOT NULL
                GROUP BY activity_data->>'query'
                ORDER BY search_count DESC, unique_users DESC
                LIMIT %s
            """, (days, limit))
            
            trending = [
                {
                    'topic': row['topic'],
                    'search_count': row['search_count'],
                    'unique_users': row['unique_users']
                }
                for row in cursor.fetchall()
            ]
            
            return trending
            
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_personalized_dashboard(user_id):
        """Build complete personalized dashboard"""
        from personalization_engine import PersonalizationEngine
        
        profile = PersonalizationEngine.get_user_profile(user_id)
        
        dashboard = {
            'greeting': PersonalizationEngine.get_personalized_greeting(user_id),
            'profile_summary': profile.get('ai_profile', {}) if profile else {},
            'recommended_tools': RecommendationEngine.get_tool_recommendations(user_id, 5),
            'learning_path': RecommendationEngine.get_learning_path(user_id),
            'suggested_topics': PersonalizationEngine.suggest_next_topics(user_id, 5),
            'trending_now': RecommendationEngine.get_trending_topics(7, 5)
        }
        
        return dashboard

# Convenience functions
get_tool_recommendations = RecommendationEngine.get_tool_recommendations
get_learning_path = RecommendationEngine.get_learning_path
get_related_topics = RecommendationEngine.get_related_topics
get_trending_topics = RecommendationEngine.get_trending_topics
get_personalized_dashboard = RecommendationEngine.get_personalized_dashboard
