#!/usr/bin/env python3
"""
R3ÆLƎR AI: Self-Learning Engine
Analyzes aggregate user data to automatically improve the knowledge base
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
from collections import Counter, defaultdict
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

class SelfLearningEngine:
    """AI system that learns from user interactions and improves automatically"""

@staticmethod
def real_search_results(query):
    conn = get_connection()
    cur = conn.cursor()
    # Search physics_unit + crypto_unit with simple keyword match
    cur.execute("""
        SELECT COUNT(*) FROM physics_unit.knowledge 
        WHERE to_tsvector('english', topic || ' ' || content) @@ plainto_tsquery(%s)
        UNION ALL
        SELECT COUNT(*) FROM crypto_unit.knowledge 
        WHERE to_tsvector('english', topic || ' ' || content) @@ plainto_tsquery(%s)
    """, (query, query))
    total = sum(row[0] for row in cur.fetchall())
    cur.close()
    conn.close()
    return total if total > 0 else 0

    @staticmethod
    def identify_knowledge_gaps(days=1, min_searches=3):
        """Find searches that yield poor results - indicating missing knowledge"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            # Searches with 0 or very few results
            cursor.execute("""
                SELECT 
                    activity_data->>'query' as query,
                    COUNT(*) as search_count,
                    AVG((activity_data->>'results_count')::int) as avg_results,
                    COUNT(DISTINCT user_id) as unique_users
                FROM user_unit.activity_log
                WHERE activity_type = 'knowledge_search'
                AND timestamp > NOW() - INTERVAL '%s days'
                AND (activity_data->>'results_count')::int < 3
                GROUP BY activity_data->>'query'
                HAVING COUNT(*) >= %s
                ORDER BY search_count DESC, unique_users DESC
                LIMIT 50
            """, (days, min_searches))
            
            gaps = [
                {
                    'query': row['query'],
                    'search_count': row['search_count'],
                    'avg_results': float(row['avg_results']) if row['avg_results'] else 0,
                    'unique_users': row['unique_users'],
                    'priority': 'high' if row['search_count'] >= 10 else 'medium'
                }
                for row in cursor.fetchall()
            ]
            
            return gaps
            
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def analyze_click_patterns(days=30):
        """Identify which knowledge entries are most valuable based on clicks"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cursor.execute("""
                SELECT 
                    activity_data->>'entry_id' as entry_id,
                    activity_data->>'topic' as topic,
                    COUNT(*) as click_count,
                    COUNT(DISTINCT user_id) as unique_users,
                    AVG((activity_data->>'position')::int) as avg_position,
                    AVG((activity_data->>'relevance_score')::float) as avg_relevance
                FROM user_unit.activity_log
                WHERE activity_type = 'knowledge_click'
                AND timestamp > NOW() - INTERVAL '%s days'
                AND activity_data->>'entry_id' IS NOT NULL
                GROUP BY activity_data->>'entry_id', activity_data->>'topic'
                ORDER BY click_count DESC
                LIMIT 100
            """, (days,))
            
            popular_entries = [
                {
                    'entry_id': row['entry_id'],
                    'topic': row['topic'],
                    'click_count': row['click_count'],
                    'unique_users': row['unique_users'],
                    'avg_position': float(row['avg_position']) if row['avg_position'] else 0,
                    'avg_relevance': float(row['avg_relevance']) if row['avg_relevance'] else 0,
                    'quality_score': SelfLearningEngine._calculate_quality_score(
                        row['click_count'], 
                        row['unique_users'],
                        float(row['avg_position']) if row['avg_position'] else 10
                    )
                }
                for row in cursor.fetchall()
            ]
            
            return popular_entries
            
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def _calculate_quality_score(clicks, unique_users, avg_position):
        """Calculate quality score for knowledge entry"""
        # Higher clicks, more unique users, lower position (clicked even when not at top)
        position_factor = max(0.1, 1.0 / (avg_position + 1))
        uniqueness_factor = unique_users / max(1, clicks)  # Diversity of users
        
        return clicks * position_factor * (1 + uniqueness_factor)
    
    @staticmethod
    def discover_topic_correlations(min_support=5):
        """Find which topics are commonly searched together"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            # Get user search sequences
            cursor.execute("""
                SELECT 
                    user_id,
                    activity_data->>'query' as query,
                    timestamp
                FROM user_unit.activity_log
                WHERE activity_type IN ('knowledge_search', 'tool_search')
                AND activity_data->>'query' IS NOT NULL
                ORDER BY user_id, timestamp
            """)
            
            # Build search sequences per user
            user_sequences = defaultdict(list)
            for row in cursor.fetchall():
                user_sequences[row['user_id']].append(row['query'])
            
            # Find co-occurrences
            topic_pairs = Counter()
            for user_id, queries in user_sequences.items():
                # Look at consecutive searches
                for i in range(len(queries) - 1):
                    topic1 = queries[i].lower()
                    topic2 = queries[i + 1].lower()
                    if topic1 != topic2:
                        pair = tuple(sorted([topic1, topic2]))
                        topic_pairs[pair] += 1
            
            # Filter by minimum support
            correlations = [
                {
                    'topic_a': pair[0],
                    'topic_b': pair[1],
                    'co_occurrence_count': count,
                    'strength': 'strong' if count >= min_support * 2 else 'moderate'
                }
                for pair, count in topic_pairs.items()
                if count >= min_support
            ]
            
            correlations.sort(key=lambda x: x['co_occurrence_count'], reverse=True)
            return correlations[:50]
            
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def auto_tag_knowledge_entries(unit_name, min_mentions=3):
        """Automatically tag knowledge entries based on user search patterns"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            # Get search queries that led to clicks on entries from this unit
            cursor.execute("""
                SELECT 
                    activity_data->>'entry_id' as entry_id,
                    activity_data->>'topic' as original_topic,
                    ARRAY_AGG(DISTINCT query_data.query) as related_queries
                FROM user_unit.activity_log clicks
                JOIN LATERAL (
                    SELECT activity_data->>'query' as query
                    FROM user_unit.activity_log searches
                    WHERE searches.user_id = clicks.user_id
                    AND searches.activity_type = 'knowledge_search'
                    AND searches.timestamp <= clicks.timestamp
                    AND searches.timestamp > clicks.timestamp - INTERVAL '5 minutes'
                    AND activity_data->>'query' IS NOT NULL
                ) query_data ON TRUE
                WHERE clicks.activity_type = 'knowledge_click'
                AND clicks.activity_data->>'entry_id' IS NOT NULL
                GROUP BY activity_data->>'entry_id', activity_data->>'topic'
                HAVING COUNT(DISTINCT query_data.query) >= %s
            """, (min_mentions,))
            
            auto_tags = []
            for row in cursor.fetchall():
                entry_id = row['entry_id']
                queries = row['related_queries']
                
                # Extract potential tags from queries
                tags = SelfLearningEngine._extract_tags_from_queries(queries)
                
                auto_tags.append({
                    'entry_id': entry_id,
                    'original_topic': row['original_topic'],
                    'suggested_tags': tags,
                    'unit_name': unit_name
                })
            
            return auto_tags
            
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def _extract_tags_from_queries(queries):
        """Extract meaningful tags from search queries"""
        if not queries:
            return []
        
        # Common words to ignore
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'was', 'were',
                     'what', 'how', 'why', 'when', 'where', 'who', 'which'}
        
        word_freq = Counter()
        for query in queries:
            words = query.lower().split()
            for word in words:
                if len(word) > 3 and word not in stop_words:
                    word_freq[word] += 1
        
        # Return top 5 most common words as tags
        return [word for word, count in word_freq.most_common(5)]
    
    @staticmethod
    def analyze_search_performance(unit_name, days=30):
        """Analyze how well searches perform in a specific unit"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cursor.execute("""
                SELECT 
                    activity_data->>'query' as query,
                    AVG((activity_data->>'results_count')::int) as avg_results,
                    AVG((activity_data->>'time_taken_ms')::float) as avg_time_ms,
                    COUNT(*) as search_count
                FROM user_unit.activity_log
                WHERE activity_type = 'knowledge_search'
                AND activity_data->>'unit' = %s
                AND timestamp > NOW() - INTERVAL '%s days'
                GROUP BY activity_data->>'query'
                ORDER BY search_count DESC
                LIMIT 100
            """, (unit_name, days))
            
            performance = []
            for row in cursor.fetchall():
                avg_results = float(row['avg_results']) if row['avg_results'] else 0
                avg_time = float(row['avg_time_ms']) if row['avg_time_ms'] else 0
                
                # Performance rating
                rating = 'good'
                if avg_results < 1:
                    rating = 'poor'
                elif avg_results < 3:
                    rating = 'needs_improvement'
                
                performance.append({
                    'query': row['query'],
                    'avg_results': avg_results,
                    'avg_time_ms': avg_time,
                    'search_count': row['search_count'],
                    'performance_rating': rating
                })
            
            return performance
            
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_improvement_suggestions(days=30):
        """Generate actionable improvement suggestions"""
        suggestions = []
        
        # Knowledge gaps
        gaps = SelfLearningEngine.identify_knowledge_gaps(days)
        if gaps:
            suggestions.append({
                'category': 'knowledge_gaps',
                'priority': 'high',
                'issue': f'Found {len(gaps)} search queries with insufficient results',
                'action': 'Add new knowledge entries for these topics',
                'details': gaps[:10]  # Top 10
            })
        
        # Topic correlations
        correlations = SelfLearningEngine.discover_topic_correlations()
        if correlations:
            suggestions.append({
                'category': 'topic_relationships',
                'priority': 'medium',
                'issue': f'Discovered {len(correlations)} topic correlations',
                'action': 'Create cross-references between related knowledge entries',
                'details': correlations[:10]
            })
        
        # Popular content
        popular = SelfLearningEngine.analyze_click_patterns(days)
        if popular:
            high_quality = [p for p in popular if p['quality_score'] > 50]
            suggestions.append({
                'category': 'content_quality',
                'priority': 'low',
                'issue': f'Identified {len(high_quality)} high-quality knowledge entries',
                'action': 'Use these as templates for new content',
                'details': high_quality[:5]
            })
        
        return suggestions
    
    @staticmethod
    def generate_learning_report(days=30):
        """Generate comprehensive learning report"""
        report = {
            'report_period': f'{days} days',
            'generated_at': datetime.now().isoformat(),
            'knowledge_gaps': SelfLearningEngine.identify_knowledge_gaps(days),
            'popular_content': SelfLearningEngine.analyze_click_patterns(days)[:20],
            'topic_correlations': SelfLearningEngine.discover_topic_correlations(),
            'improvement_suggestions': SelfLearningEngine.get_improvement_suggestions(days),
            'summary': {
                'total_gaps': 0,
                'total_correlations': 0,
                'high_priority_actions': 0
            }
        }
        
        # Calculate summary
        report['summary']['total_gaps'] = len(report['knowledge_gaps'])
        report['summary']['total_correlations'] = len(report['topic_correlations'])
        report['summary']['high_priority_actions'] = len([
            s for s in report['improvement_suggestions'] if s['priority'] == 'high'
        ])
        
        return report

# Convenience functions
if __name__ == "__main__":
    # Call the class method correctly
    report = SelfLearningEngine.generate_learning_report(30)
    print(json.dumps(report, indent=2))
