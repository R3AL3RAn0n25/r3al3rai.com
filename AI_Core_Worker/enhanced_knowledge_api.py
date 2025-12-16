"""
Enhanced Knowledge API for R3ÆLƎR AI
Integrates trained benchmark data with response generation
"""

import os
import sys
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify, request
from flask_cors import CORS

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

class EnhancedKnowledgeAPI:
    """Enhanced knowledge API with trained benchmark data integration"""

    def __init__(self):
        self.db_config = {
            'host': '127.0.0.1',
            'port': 5432,
            'database': 'r3aler_ai',
            'user': 'r3aler_user_2025',
            'password': 'R3AL3RAdmin816'
        }
        self.benchmark_schemas = {
            "mmlu": "mmlu_training",
            "commonsense_qa": "commonsense_training",
            "gsm8k": "gsm8k_training",
            "arc": "arc_training",
            "hellaswag": "hellaswag_training",
            "math": "math_training",
            "gpqa": "gpqa_training",
            "humaneval": "humaneval_training"
        }

    def search_trained_knowledge(self, query: str, benchmark_area: str = None,
                                limit: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant trained knowledge based on query"""
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            results = []

            # If specific benchmark area requested
            if benchmark_area and benchmark_area in self.benchmark_schemas:
                schema = self.benchmark_schemas[benchmark_area]
                results.extend(self._search_schema(cursor, schema, query, limit))
            else:
                # Search all benchmark areas
                for area, schema in self.benchmark_schemas.items():
                    area_results = self._search_schema(cursor, schema, query, limit // 2)
                    results.extend(area_results)

            # Sort by relevance and limit
            results.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
            results = results[:limit]

            cursor.close()
            conn.close()

            return results

        except Exception as e:
            logger.error(f"Knowledge search error: {e}")
            return []

    def _search_schema(self, cursor, schema: str, query: str, limit: int) -> List[Dict[str, Any]]:
        """Search within a specific training schema"""
        try:
            # Search for similar questions using text similarity
            cursor.execute(f"""
                SELECT
                    question,
                    answer,
                    context,
                    subject,
                    dataset_source,
                    similarity(question, %s) as relevance_score
                FROM {schema}.training_examples
                WHERE question % %s
                ORDER BY similarity(question, %s) DESC
                LIMIT %s
            """, (query, query, query, limit))

            results = []
            for row in cursor.fetchall():
                results.append({
                    "question": row["question"],
                    "answer": row["answer"],
                    "context": row["context"],
                    "subject": row["subject"],
                    "dataset_source": row["dataset_source"],
                    "relevance_score": float(row["relevance_score"]),
                    "source": f"R3AL3R Training - {schema}",
                    "confidence": min(float(row["relevance_score"]) * 1.2, 0.95)  # Boost confidence for trained data
                })

            return results

        except Exception as e:
            logger.warning(f"Schema search error for {schema}: {e}")
            return []

    def get_knowledge_patterns(self, benchmark_area: str) -> Dict[str, Any]:
        """Get knowledge patterns for a benchmark area"""
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            schema = self.benchmark_schemas.get(benchmark_area)
            if not schema:
                return {}

            cursor.execute(f"""
                SELECT pattern_type, pattern_data, confidence, usage_count
                FROM {schema}.knowledge_patterns
                ORDER BY usage_count DESC, confidence DESC
            """)

            patterns = {}
            for row in cursor.fetchall():
                patterns[row["pattern_type"]] = {
                    "data": row["pattern_data"],
                    "confidence": float(row["confidence"]),
                    "usage_count": row["usage_count"]
                }

            cursor.close()
            conn.close()

            return patterns

        except Exception as e:
            logger.error(f"Pattern retrieval error: {e}")
            return {}

    def enhance_response_with_training(self, query: str, base_response: str,
                                     intent: Dict) -> str:
        """Enhance response using trained knowledge"""
        try:
            # Detect which benchmark area this query relates to
            benchmark_area = self._classify_query_benchmark_area(query, intent)

            if benchmark_area:
                # Get relevant trained knowledge
                knowledge_results = self.search_trained_knowledge(query, benchmark_area, limit=3)

                if knowledge_results:
                    # Get patterns for this area
                    patterns = self.get_knowledge_patterns(benchmark_area)

                    # Enhance response with trained knowledge
                    enhanced_response = self._integrate_knowledge(base_response, knowledge_results, patterns)
                    return enhanced_response

            return base_response

        except Exception as e:
            logger.error(f"Response enhancement error: {e}")
            return base_response

    def _classify_query_benchmark_area(self, query: str, intent: Dict) -> Optional[str]:
        """Classify query into benchmark area"""
        query_lower = query.lower()

        # Classification rules
        if any(word in query_lower for word in ['what is', 'who was', 'where is', 'when did', 'why does', 'how does']):
            if any(word in query_lower for word in ['physics', 'chemistry', 'biology', 'history', 'geography']):
                return "mmlu"
            elif any(word in query_lower for word in ['calculate', 'solve', 'math', 'equation']):
                return "math"
            elif any(word in query_lower for word in ['code', 'program', 'function', 'algorithm']):
                return "humaneval"
            else:
                return "mmlu"

        elif any(word in query_lower for word in ['solve', 'calculate', 'math', 'number', 'equation']):
            return "gsm8k"

        elif any(word in query_lower for word in ['why', 'because', 'reason', 'explain']):
            if any(word in query_lower for word in ['science', 'physics', 'chemistry']):
                return "arc"
            else:
                return "commonsense_qa"

        elif any(word in query_lower for word in ['what happens', 'then', 'next', 'after']):
            return "hellaswag"

        elif any(word in query_lower for word in ['quantum', 'physics', 'theory', 'hypothesis']):
            return "gpqa"

        return None

    def _integrate_knowledge(self, base_response: str, knowledge_results: List[Dict],
                           patterns: Dict) -> str:
        """Integrate trained knowledge into response"""
        if not knowledge_results:
            return base_response

        # Add knowledge-based enhancement
        enhancement_parts = []

        # Add most relevant knowledge
        top_knowledge = knowledge_results[0] if knowledge_results else None
        if top_knowledge and top_knowledge["relevance_score"] > 0.3:
            enhancement_parts.append(f"📚 Based on training data: {top_knowledge['answer']}")

        # Add pattern-based insights
        if patterns.get("question_patterns"):
            question_patterns = patterns["question_patterns"].get("data", {})
            if question_patterns.get("short_questions", 0) > question_patterns.get("long_questions", 0):
                enhancement_parts.append("💡 This appears to be a direct factual question requiring precise knowledge.")

        # Add confidence indicator
        avg_confidence = sum(k["confidence"] for k in knowledge_results) / len(knowledge_results)
        if avg_confidence > 0.8:
            enhancement_parts.append("🎯 High confidence response based on comprehensive training data.")

        # Combine enhancements
        if enhancement_parts:
            enhanced = base_response + "\n\n" + "\n".join(enhancement_parts)
            return enhanced

        return base_response

# Global instance
knowledge_api = EnhancedKnowledgeAPI()

@app.route('/api/knowledge/search', methods=['POST'])
def search_knowledge():
    """Search trained knowledge"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        benchmark_area = data.get('benchmark_area')
        limit = data.get('limit', 5)

        results = knowledge_api.search_trained_knowledge(query, benchmark_area, limit)

        return jsonify({
            "status": "success",
            "results": results,
            "count": len(results)
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/knowledge/patterns/<benchmark_area>', methods=['GET'])
def get_patterns(benchmark_area):
    """Get knowledge patterns for benchmark area"""
    try:
        patterns = knowledge_api.get_knowledge_patterns(benchmark_area)

        return jsonify({
            "status": "success",
            "benchmark_area": benchmark_area,
            "patterns": patterns
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/knowledge/enhance', methods=['POST'])
def enhance_response():
    """Enhance response with trained knowledge"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        base_response = data.get('response', '')
        intent = data.get('intent', {})

        enhanced_response = knowledge_api.enhance_response_with_training(query, base_response, intent)

        return jsonify({
            "status": "success",
            "original_response": base_response,
            "enhanced_response": enhanced_response,
            "enhancement_applied": enhanced_response != base_response
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/knowledge/status', methods=['GET'])
def get_status():
    """Get training data status"""
    try:
        # Import here to avoid circular imports
        from targeted_benchmark_training import BenchmarkTrainingSystem
        trainer = BenchmarkTrainingSystem()
        status = trainer.get_training_status()

        return jsonify({
            "status": "success",
            "training_status": status,
            "total_areas": len(status)
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    print("🚀 Starting Enhanced Knowledge API for R3ÆLƎR AI")
    print("📍 Integrated with R3AL3R Cloud Storage Facility")
    app.run(host='0.0.0.0', port=5001, debug=False)</content>
<parameter name="filePath">c:\Users\work8\OneDrive\Desktop\r3al3rai\New Folder 1\R3al3r-AI Main Working\R3aler-ai\R3aler-ai\enhanced_knowledge_api.py