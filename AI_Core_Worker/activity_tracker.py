#!/usr/bin/env python3
"""
R3ÆLƎR AI: Activity Tracking Module
Logs all user interactions for AI learning and personalization
"""

import psycopg2
from psycopg2.extras import Json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# PostgreSQL Configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'r3aler_ai',
    'user': 'r3aler_user_2025',
    'password': 'password123'
}

def get_connection():
    """Get database connection"""
    return psycopg2.connect(**DB_CONFIG)

class ActivityTracker:
    """Track user activities for AI learning"""
    
    @staticmethod
    def log_activity(user_id, activity_type, activity_data):
        """
        Log user activity to database
        
        Args:
            user_id: User ID (or None for anonymous)
            activity_type: Type of activity (search, tool_query, knowledge_click, etc.)
            activity_data: Dict containing activity details
        """
        if not user_id:
            return  # Skip logging for anonymous users (for now)
        
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO user_unit.activity_log (
                    user_id, activity_type, activity_data, timestamp
                ) VALUES (%s, %s, %s, NOW())
            """, (user_id, activity_type, Json(activity_data)))
            
            conn.commit()
            
            logger.debug(f"Logged activity: user={user_id}, type={activity_type}")
            
        except Exception as e:
            logger.error(f"Failed to log activity: {e}")
            conn.rollback()
        
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def log_knowledge_search(user_id, query, results_count, unit=None, time_taken_ms=None):
        """Log knowledge base search"""
        ActivityTracker.log_activity(user_id, 'knowledge_search', {
            'query': query,
            'results_count': results_count,
            'unit': unit,
            'time_taken_ms': time_taken_ms,
            'timestamp': datetime.now().isoformat()
        })
    
    @staticmethod
    def log_knowledge_click(user_id, entry_id, topic, relevance_score, position_in_results):
        """Log when user clicks/views a knowledge entry"""
        ActivityTracker.log_activity(user_id, 'knowledge_click', {
            'entry_id': entry_id,
            'topic': topic,
            'relevance_score': relevance_score,
            'position': position_in_results,
            'timestamp': datetime.now().isoformat()
        })
    
    @staticmethod
    def log_tool_search(user_id, query, results_count, category=None):
        """Log BlackArch tool search"""
        ActivityTracker.log_activity(user_id, 'tool_search', {
            'query': query,
            'results_count': results_count,
            'category': category,
            'timestamp': datetime.now().isoformat()
        })
    
    @staticmethod
    def log_tool_view(user_id, tool_id, tool_name, category):
        """Log when user views tool details"""
        ActivityTracker.log_activity(user_id, 'tool_view', {
            'tool_id': tool_id,
            'tool_name': tool_name,
            'category': category,
            'timestamp': datetime.now().isoformat()
        })
    
    @staticmethod
    def log_tool_download(user_id, tool_id, tool_name):
        """Log when user downloads a tool"""
        ActivityTracker.log_activity(user_id, 'tool_download', {
            'tool_id': tool_id,
            'tool_name': tool_name,
            'timestamp': datetime.now().isoformat()
        })
        
        # Also update tool_preferences
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO user_unit.tool_preferences (
                    user_id, tool_id, is_downloaded, last_used, usage_count
                ) VALUES (%s, %s, TRUE, NOW(), 1)
                ON CONFLICT (user_id, tool_id) DO UPDATE SET
                    is_downloaded = TRUE,
                    last_used = NOW(),
                    usage_count = user_unit.tool_preferences.usage_count + 1
            """, (user_id, tool_id))
            
            conn.commit()
            
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def log_session_duration(user_id, session_start, session_end, pages_viewed):
        """Log session information"""
        duration_seconds = (session_end - session_start).total_seconds()
        
        ActivityTracker.log_activity(user_id, 'session', {
            'duration_seconds': duration_seconds,
            'pages_viewed': pages_viewed,
            'start_time': session_start.isoformat(),
            'end_time': session_end.isoformat()
        })
    
    @staticmethod
    def log_error(user_id, error_type, error_message, context=None):
        """Log errors for improvement"""
        ActivityTracker.log_activity(user_id, 'error', {
            'error_type': error_type,
            'error_message': error_message,
            'context': context,
            'timestamp': datetime.now().isoformat()
        })
    
    @staticmethod
    def log_feedback(user_id, feedback_type, rating, comment=None, related_to=None):
        """Log user feedback"""
        ActivityTracker.log_activity(user_id, 'feedback', {
            'feedback_type': feedback_type,  # positive, negative, suggestion
            'rating': rating,  # 1-5
            'comment': comment,
            'related_to': related_to,  # entry_id, tool_id, etc.
            'timestamp': datetime.now().isoformat()
        })
    
    @staticmethod
    def get_user_activity_summary(user_id, days=30):
        """Get summary of user's recent activity"""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT 
                    activity_type,
                    COUNT(*) as count,
                    MAX(timestamp) as last_occurrence
                FROM user_unit.activity_log
                WHERE user_id = %s
                AND timestamp > NOW() - INTERVAL '%s days'
                GROUP BY activity_type
                ORDER BY count DESC
            """, (user_id, days))
            
            activities = cursor.fetchall()
            
            return {
                'user_id': user_id,
                'period_days': days,
                'activities': [
                    {
                        'type': row[0],
                        'count': row[1],
                        'last_occurrence': row[2].isoformat() if row[2] else None
                    }
                    for row in activities
                ]
            }
            
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_most_searched_topics(user_id, limit=10):
        """Get user's most searched topics"""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT 
                    activity_data->>'query' as query,
                    COUNT(*) as search_count
                FROM user_unit.activity_log
                WHERE user_id = %s
                AND activity_type IN ('knowledge_search', 'tool_search')
                AND activity_data->>'query' IS NOT NULL
                GROUP BY activity_data->>'query'
                ORDER BY search_count DESC
                LIMIT %s
            """, (user_id, limit))
            
            return [
                {'query': row[0], 'count': row[1]}
                for row in cursor.fetchall()
            ]
            
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_favorite_tools(user_id, limit=10):
        """Get user's most used tools"""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT 
                    tool_id,
                    usage_count,
                    is_pinned,
                    is_downloaded,
                    last_used
                FROM user_unit.tool_preferences
                WHERE user_id = %s
                ORDER BY usage_count DESC, last_used DESC
                LIMIT %s
            """, (user_id, limit))
            
            return [
                {
                    'tool_id': row[0],
                    'usage_count': row[1],
                    'is_pinned': row[2],
                    'is_downloaded': row[3],
                    'last_used': row[4].isoformat() if row[4] else None
                }
                for row in cursor.fetchall()
            ]
            
        finally:
            cursor.close()
            conn.close()

# Convenience functions for easy import
log_activity = ActivityTracker.log_activity
log_knowledge_search = ActivityTracker.log_knowledge_search
log_knowledge_click = ActivityTracker.log_knowledge_click
log_tool_search = ActivityTracker.log_tool_search
log_tool_view = ActivityTracker.log_tool_view
log_tool_download = ActivityTracker.log_tool_download
log_session_duration = ActivityTracker.log_session_duration
log_error = ActivityTracker.log_error
log_feedback = ActivityTracker.log_feedback
