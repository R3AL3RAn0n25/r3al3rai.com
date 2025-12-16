#!/usr/bin/env python3
"""
R3ÆLƎR AI: Evolution Engine
Automatic system optimization and continuous improvement
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
from collections import defaultdict
import json
import logging
import statistics

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

class EvolutionEngine:
    """System that evolves and optimizes itself based on performance metrics"""
    
    @staticmethod
    def measure_search_quality(days=1):
        """Measure overall search quality metrics"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            # Get search metrics
            cursor.execute("""
                WITH search_metrics AS (
                    SELECT 
                        (activity_data->>'results_count')::int as results_count,
                        (activity_data->>'time_taken_ms')::float as time_ms
                    FROM user_unit.activity_log
                    WHERE activity_type = 'knowledge_search'
                    AND timestamp > NOW() - INTERVAL '%s days'
                    AND activity_data->>'results_count' IS NOT NULL
                    AND activity_data->>'time_taken_ms' IS NOT NULL
                )
                SELECT 
                    COUNT(*) as total_searches,
                    AVG(results_count) as avg_results,
                    AVG(time_ms) as avg_time_ms,
                    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY results_count) as median_results,
                    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY time_ms) as p95_time_ms,
                    COUNT(CASE WHEN results_count = 0 THEN 1 END) as zero_result_searches,
                    COUNT(CASE WHEN results_count >= 5 THEN 1 END) as good_searches
                FROM search_metrics
            """, (days,))
            
            metrics = cursor.fetchone()
            if not metrics or metrics['total_searches'] == 0:
                return {
                    'status': 'insufficient_data',
                    'message': 'Not enough search data to measure quality'
                }
            
            total = metrics['total_searches']
            zero_rate = (metrics['zero_result_searches'] / total) * 100
            good_rate = (metrics['good_searches'] / total) * 100
            
            quality = {
                'period_days': days,
                'total_searches': total,
                'avg_results_per_search': float(metrics['avg_results']) if metrics['avg_results'] else 0,
                'median_results': float(metrics['median_results']) if metrics['median_results'] else 0,
                'avg_response_time_ms': float(metrics['avg_time_ms']) if metrics['avg_time_ms'] else 0,
                'p95_response_time_ms': float(metrics['p95_time_ms']) if metrics['p95_time_ms'] else 0,
                'zero_result_rate': round(zero_rate, 2),
                'good_search_rate': round(good_rate, 2),
                'quality_score': EvolutionEngine._calculate_overall_quality(
                    zero_rate, good_rate, float(metrics['avg_time_ms']) if metrics['avg_time_ms'] else 0
                )
            }
            
            return quality
            
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def _calculate_overall_quality(zero_rate, good_rate, avg_time_ms):
        """Calculate overall quality score (0-100)"""
        # Lower zero_rate is better, higher good_rate is better, lower time is better
        score = 100
        score -= zero_rate * 2  # Penalize zero results heavily
        score += (good_rate - 50) * 0.5  # Reward good searches
        
        # Penalize slow searches (>500ms is bad)
        if avg_time_ms > 500:
            score -= (avg_time_ms - 500) / 100
        
        return max(0, min(100, round(score, 2)))
    
    @staticmethod
    def detect_trending_patterns(days=7):
        """Detect emerging trends in user behavior"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            # Compare recent activity to historical average
            cursor.execute("""
                WITH recent_topics AS (
                    SELECT 
                        activity_data->>'query' as topic,
                        COUNT(*) as recent_count
                    FROM user_unit.activity_log
                    WHERE activity_type IN ('knowledge_search', 'tool_search')
                    AND timestamp > NOW() - INTERVAL '%s days'
                    AND activity_data->>'query' IS NOT NULL
                    GROUP BY activity_data->>'query'
                ),
                historical_topics AS (
                    SELECT 
                        activity_data->>'query' as topic,
                        COUNT(*) as historical_count
                    FROM user_unit.activity_log
                    WHERE activity_type IN ('knowledge_search', 'tool_search')
                    AND timestamp <= NOW() - INTERVAL '%s days'
                    AND timestamp > NOW() - INTERVAL '%s days'
                    AND activity_data->>'query' IS NOT NULL
                    GROUP BY activity_data->>'query'
                )
                SELECT 
                    r.topic,
                    r.recent_count,
                    COALESCE(h.historical_count, 0) as historical_count,
                    CASE 
                        WHEN COALESCE(h.historical_count, 0) = 0 THEN 999
                        ELSE ROUND((r.recent_count::float / h.historical_count::float), 2)
                    END as growth_factor
                FROM recent_topics r
                LEFT JOIN historical_topics h ON r.topic = h.topic
                ORDER BY growth_factor DESC
                LIMIT 20
            """, (days, days, days * 2))
            
            trends = []
            for row in cursor.fetchall():
                growth = float(row['growth_factor'])
                
                if growth >= 999:
                    trend_type = 'new_emerging'
                elif growth >= 3:
                    trend_type = 'rapidly_growing'
                elif growth >= 1.5:
                    trend_type = 'growing'
                else:
                    trend_type = 'stable'
                
                trends.append({
                    'topic': row['topic'],
                    'recent_searches': row['recent_count'],
                    'historical_searches': row['historical_count'],
                    'growth_factor': growth,
                    'trend_type': trend_type
                })
            
            return trends
            
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def optimize_personalization_weights():
        """Analyze and suggest optimal personalization boost factors"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            # Analyze click-through rates at different positions
            cursor.execute("""
                SELECT 
                    (activity_data->>'position')::int as position,
                    COUNT(*) as click_count,
                    AVG((activity_data->>'relevance_score')::float) as avg_relevance
                FROM user_unit.activity_log
                WHERE activity_type = 'knowledge_click'
                AND activity_data->>'position' IS NOT NULL
                AND (activity_data->>'position')::int <= 20
                GROUP BY (activity_data->>'position')::int
                ORDER BY position
            """)
            
            position_data = [dict(row) for row in cursor.fetchall()]
            
            if not position_data:
                return {
                    'status': 'insufficient_data',
                    'message': 'Not enough click data for optimization'
                }
            
            # Calculate optimal boost factors
            # If users click lower positions frequently, boost factors may be too aggressive
            total_clicks = sum(row['click_count'] for row in position_data)
            top_3_clicks = sum(row['click_count'] for row in position_data[:3])
            top_3_rate = (top_3_clicks / total_clicks) * 100 if total_clicks > 0 else 0
            
            suggestions = {
                'current_analysis': {
                    'total_clicks': total_clicks,
                    'top_3_click_rate': round(top_3_rate, 2),
                    'position_distribution': position_data[:10]
                },
                'recommendations': []
            }
            
            if top_3_rate < 50:
                suggestions['recommendations'].append({
                    'parameter': 'interest_boost_factor',
                    'current_value': 1.5,
                    'suggested_value': 1.8,
                    'reason': 'Top 3 click rate is low, increase personalization boost'
                })
            elif top_3_rate > 80:
                suggestions['recommendations'].append({
                    'parameter': 'interest_boost_factor',
                    'current_value': 1.5,
                    'suggested_value': 1.3,
                    'reason': 'Top 3 click rate is very high, decrease boost to improve diversity'
                })
            else:
                suggestions['recommendations'].append({
                    'parameter': 'interest_boost_factor',
                    'current_value': 1.5,
                    'suggested_value': 1.5,
                    'reason': 'Current boost factor is performing well'
                })
            
            return suggestions
            
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def analyze_user_retention(days=30):
        """Analyze user retention and engagement patterns"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cursor.execute("""
                WITH user_activity AS (
                    SELECT 
                        user_id,
                        DATE(timestamp) as activity_date,
                        COUNT(*) as daily_actions
                    FROM user_unit.activity_log
                    WHERE timestamp > NOW() - INTERVAL '%s days'
                    GROUP BY user_id, DATE(timestamp)
                ),
                user_metrics AS (
                    SELECT 
                        user_id,
                        COUNT(DISTINCT activity_date) as active_days,
                        AVG(daily_actions) as avg_daily_actions
                    FROM user_activity
                    GROUP BY user_id
                )
                SELECT 
                    COUNT(*) as total_users,
                    AVG(active_days) as avg_active_days,
                    AVG(avg_daily_actions) as avg_actions_per_day,
                    COUNT(CASE WHEN active_days >= %s * 0.5 THEN 1 END) as highly_engaged_users,
                    COUNT(CASE WHEN active_days <= 2 THEN 1 END) as at_risk_users
                FROM user_metrics
            """, (days, days))
            
            metrics = cursor.fetchone()
            if not metrics or metrics['total_users'] == 0:
                return {
                    'status': 'no_users',
                    'message': 'No user activity data available'
                }
            
            total = metrics['total_users']
            
            return {
                'period_days': days,
                'total_users': total,
                'avg_active_days': round(float(metrics['avg_active_days']), 2) if metrics['avg_active_days'] else 0,
                'avg_actions_per_day': round(float(metrics['avg_actions_per_day']), 2) if metrics['avg_actions_per_day'] else 0,
                'highly_engaged_users': metrics['highly_engaged_users'],
                'highly_engaged_rate': round((metrics['highly_engaged_users'] / total) * 100, 2),
                'at_risk_users': metrics['at_risk_users'],
                'at_risk_rate': round((metrics['at_risk_users'] / total) * 100, 2)
            }
            
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def generate_evolution_report(days=7):
        """Generate comprehensive system evolution report"""
        report = {
            'report_period': f'{days} days',
            'generated_at': datetime.now().isoformat(),
            'search_quality': EvolutionEngine.measure_search_quality(days),
            'trending_patterns': EvolutionEngine.detect_trending_patterns(days),
            'personalization_optimization': EvolutionEngine.optimize_personalization_weights(),
            'user_retention': EvolutionEngine.analyze_user_retention(days * 4),
            'recommendations': []
        }
        
        # Generate actionable recommendations
        quality = report['search_quality']
        if isinstance(quality, dict) and 'quality_score' in quality:
            if quality['quality_score'] < 60:
                report['recommendations'].append({
                    'priority': 'high',
                    'area': 'search_quality',
                    'issue': f'Quality score is {quality["quality_score"]}/100',
                    'action': 'Review and improve search algorithm'
                })
            
            if quality['zero_result_rate'] > 20:
                report['recommendations'].append({
                    'priority': 'high',
                    'area': 'knowledge_coverage',
                    'issue': f'{quality["zero_result_rate"]}% of searches return no results',
                    'action': 'Add knowledge entries for underserved topics'
                })
        
        # Check trending patterns
        trends = report['trending_patterns']
        new_topics = [t for t in trends if t['trend_type'] == 'new_emerging']
        if new_topics:
            report['recommendations'].append({
                'priority': 'medium',
                'area': 'content_strategy',
                'issue': f'Detected {len(new_topics)} emerging topics',
                'action': f'Create content for: {", ".join([t["topic"] for t in new_topics[:3]])}'
            })
        
        return report
    
    @staticmethod
    def auto_adjust_system_parameters():
        """Automatically adjust system parameters based on performance"""
        adjustments = []
        
        # Get current performance metrics
        quality = EvolutionEngine.measure_search_quality(7)
        if isinstance(quality, dict) and 'quality_score' in quality:
            
            # Auto-adjust based on quality score
            if quality['zero_result_rate'] > 25:
                adjustments.append({
                    'parameter': 'search_similarity_threshold',
                    'action': 'decrease',
                    'reason': 'Too many zero-result searches, lower threshold for broader results'
                })
            
            if quality['p95_response_time_ms'] > 1000:
                adjustments.append({
                    'parameter': 'max_search_results',
                    'action': 'decrease',
                    'reason': 'Response time is slow, reduce result set size'
                })
        
        # Get personalization optimization
        personalization = EvolutionEngine.optimize_personalization_weights()
        if isinstance(personalization, dict) and 'recommendations' in personalization:
            for rec in personalization['recommendations']:
                if rec['current_value'] != rec['suggested_value']:
                    adjustments.append({
                        'parameter': rec['parameter'],
                        'action': f'change to {rec["suggested_value"]}',
                        'reason': rec['reason']
                    })
        
        return {
            'timestamp': datetime.now().isoformat(),
            'adjustments_recommended': len(adjustments),
            'adjustments': adjustments
        }

# Convenience functions
measure_search_quality = EvolutionEngine.measure_search_quality
detect_trending_patterns = EvolutionEngine.detect_trending_patterns
optimize_personalization_weights = EvolutionEngine.optimize_personalization_weights
analyze_user_retention = EvolutionEngine.analyze_user_retention
generate_evolution_report = EvolutionEngine.generate_evolution_report
auto_adjust_system_parameters = EvolutionEngine.auto_adjust_system_parameters
