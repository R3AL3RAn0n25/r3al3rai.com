"""
R3ÆLƎR AI - Mathematical Reasoning Enhancement Module
Enhances AI mathematical capabilities by integrating knowledge base with symbolic processing
"""

import re
import sympy as sp
from typing import Dict, List, Optional, Tuple
import logging
from AI_Core_Worker.math_processor import SymbolicMathProcessor

class MathReasoningEnhancer:
    """Enhances mathematical reasoning by combining knowledge base with symbolic processing"""

    def __init__(self, storage_facility=None):
        self.storage = storage_facility
        self.math_processor = SymbolicMathProcessor()
        self.logger = logging.getLogger(__name__)

        # Math patterns for problem recognition
        self.math_patterns = {
            'algebra': re.compile(r'\b(?:solve|find|calculate)\s+.*\b(?:x|y|z|variable)\b', re.IGNORECASE),
            'arithmetic': re.compile(r'\b\d+\s*[\+\-\*\/]\s*\d+\b'),
            'word_problems': re.compile(r'\b(?:how many|what is|find the|calculate)\b.*\d+', re.IGNORECASE),
            'equations': re.compile(r'\b\w+\s*=\s*[\d\w\+\-\*\/\(\)]+\b'),
        }

    def enhance_mathematical_reasoning(self, query: str) -> Dict:
        """
        Enhance mathematical reasoning for a given query

        Args:
            query: The mathematical query to process

        Returns:
            Dict containing enhanced reasoning and solution
        """
        try:
            # Detect math problem type
            problem_type = self._classify_math_problem(query)

            # Retrieve relevant knowledge from storage
            knowledge_results = self._retrieve_math_knowledge(query, problem_type)

            # Apply symbolic processing
            symbolic_result = self._apply_symbolic_processing(query, problem_type)

            # Combine knowledge and symbolic processing
            enhanced_reasoning = self._combine_reasoning(
                query, knowledge_results, symbolic_result, problem_type
            )

            return {
                'query': query,
                'problem_type': problem_type,
                'knowledge_used': len(knowledge_results),
                'symbolic_processing': symbolic_result,
                'enhanced_reasoning': enhanced_reasoning,
                'confidence': self._calculate_confidence(knowledge_results, symbolic_result)
            }

        except Exception as e:
            self.logger.error(f"Error in mathematical reasoning enhancement: {e}")
            return {
                'query': query,
                'error': str(e),
                'fallback_reasoning': self._fallback_reasoning(query)
            }

    def _classify_math_problem(self, query: str) -> str:
        """Classify the type of mathematical problem"""
        query_lower = query.lower()

        if self.math_patterns['algebra'].search(query):
            return 'algebra'
        elif self.math_patterns['arithmetic'].search(query):
            return 'arithmetic'
        elif self.math_patterns['word_problems'].search(query):
            return 'word_problem'
        elif self.math_patterns['equations'].search(query):
            return 'equation'
        elif any(word in query_lower for word in ['geometry', 'triangle', 'circle', 'area', 'volume']):
            return 'geometry'
        elif any(word in query_lower for word in ['probability', 'chance', 'odds']):
            return 'probability'
        elif any(word in query_lower for word in ['statistics', 'average', 'mean', 'median']):
            return 'statistics'
        else:
            return 'general_math'

    def _retrieve_math_knowledge(self, query: str, problem_type: str) -> List[Dict]:
        """Retrieve relevant mathematical knowledge from storage facility"""
        if not self.storage:
            return []

        try:
            # Search physics unit for math knowledge
            results = self.storage.search_knowledge('physics', query, limit=10)

            # Filter for math-related content
            math_results = []
            for result in results:
                content = result.get('content', '').lower()
                topic = result.get('topic', '').lower()

                # Check if content is math-related
                math_keywords = ['math', 'algebra', 'equation', 'solve', 'calculate',
                               'arithmetic', 'geometry', 'probability', 'statistics']

                if any(keyword in content or keyword in topic for keyword in math_keywords):
                    math_results.append(result)

            return math_results[:5]  # Return top 5 relevant results

        except Exception as e:
            self.logger.error(f"Error retrieving math knowledge: {e}")
            return []

    def _apply_symbolic_processing(self, query: str, problem_type: str) -> Dict:
        """Apply symbolic mathematics processing"""
        try:
            if problem_type == 'algebra':
                return self._process_algebra(query)
            elif problem_type == 'arithmetic':
                return self._process_arithmetic(query)
            elif problem_type == 'equation':
                return self._process_equation(query)
            else:
                return self.math_processor.process_math_query(query)
        except Exception as e:
            self.logger.error(f"Error in symbolic processing: {e}")
            return {'error': str(e)}

    def _process_algebra(self, query: str) -> Dict:
        """Process algebraic problems"""
        try:
            # Extract equation from query
            equation_match = re.search(r'(\w+)\s*=\s*([^=\n]+)', query)
            if equation_match:
                var, expr = equation_match.groups()
                # Use sympy to solve
                x = sp.Symbol(var)
                equation = sp.Eq(x, sp.sympify(expr))
                solution = sp.solve(equation, x)

                return {
                    'type': 'algebra',
                    'equation': f"{var} = {expr}",
                    'solution': str(solution[0]) if solution else 'No solution found',
                    'method': 'symbolic_algebra'
                }
            else:
                return {'type': 'algebra', 'error': 'Could not parse equation'}
        except Exception as e:
            return {'type': 'algebra', 'error': str(e)}

    def _process_arithmetic(self, query: str) -> Dict:
        """Process arithmetic problems"""
        try:
            # Extract arithmetic expression
            expr_match = re.search(r'(\d+\s*[\+\-\*\/]\s*\d+)', query)
            if expr_match:
                expr = expr_match.group(1)
                result = eval(expr)  # Safe for simple arithmetic

                return {
                    'type': 'arithmetic',
                    'expression': expr,
                    'result': result,
                    'method': 'direct_calculation'
                }
            else:
                return {'type': 'arithmetic', 'error': 'Could not parse expression'}
        except Exception as e:
            return {'type': 'arithmetic', 'error': str(e)}

    def _process_equation(self, query: str) -> Dict:
        """Process general equations"""
        try:
            return self.math_processor.process_math_query(query)
        except Exception as e:
            return {'type': 'equation', 'error': str(e)}

    def _combine_reasoning(self, query: str, knowledge: List[Dict],
                          symbolic: Dict, problem_type: str) -> str:
        """Combine knowledge base and symbolic processing results"""
        reasoning_parts = []

        # Add knowledge-based insights
        if knowledge:
            reasoning_parts.append("Based on stored mathematical knowledge:")
            for item in knowledge[:2]:  # Use top 2 knowledge items
                content = item.get('content', '')[:100]
                if content:
                    reasoning_parts.append(f"• {content}...")

        # Add symbolic processing results
        if 'result' in symbolic:
            reasoning_parts.append(f"Symbolic processing result: {symbolic['result']}")
        elif 'solution' in symbolic:
            reasoning_parts.append(f"Algebraic solution: {symbolic['solution']}")

        # Add problem type analysis
        reasoning_parts.append(f"Problem type identified: {problem_type}")

        return "\n".join(reasoning_parts)

    def _calculate_confidence(self, knowledge: List[Dict], symbolic: Dict) -> float:
        """Calculate confidence score for the reasoning"""
        confidence = 0.0

        # Knowledge base contribution
        if knowledge:
            confidence += min(len(knowledge) * 0.2, 0.4)

        # Symbolic processing contribution
        if 'result' in symbolic or 'solution' in symbolic:
            confidence += 0.6

        return min(confidence, 1.0)

    def _fallback_reasoning(self, query: str) -> str:
        """Provide fallback reasoning when enhancement fails"""
        return f"Query: {query}\nThis appears to be a mathematical problem. Consider breaking it down into smaller steps and using basic arithmetic or algebraic principles."

def integrate_math_enhancement(ai_core, storage_facility):
    """
    Integrate mathematical reasoning enhancement into AI core

    Args:
        ai_core: The main AI core system
        storage_facility: The storage facility instance
    """
    enhancer = MathReasoningEnhancer(storage_facility)

    # Add enhancement method to AI core
    ai_core.math_enhancer = enhancer

    # Override or extend the response generation to include math enhancement
    original_generate = ai_core.generate_response

    def enhanced_generate_response(query, **kwargs):
        # Check if query is mathematical
        if any(keyword in query.lower() for keyword in
               ['solve', 'calculate', 'math', 'equation', 'algebra', 'arithmetic']):
            # Apply mathematical enhancement
            math_result = enhancer.enhance_mathematical_reasoning(query)

            # Combine with original response
            enhanced_response = original_generate(query, **kwargs)

            if 'enhanced_reasoning' in math_result:
                enhanced_response += f"\n\nMathematical Analysis:\n{math_result['enhanced_reasoning']}"

            return enhanced_response
        else:
            return original_generate(query, **kwargs)

    ai_core.generate_response = enhanced_generate_response
    print("✅ Mathematical reasoning enhancement integrated into AI core")

if __name__ == "__main__":
    # Test the math reasoning enhancer
    enhancer = MathReasoningEnhancer()

    test_queries = [
        "Solve 2x + 5 = 17",
        "What is 15 + 27?",
        "Calculate the area of a rectangle 8 by 5",
        "Find x in the equation x^2 = 16"
    ]

    print("🧮 Testing Mathematical Reasoning Enhancement")
    print("=" * 50)

    for query in test_queries:
        print(f"\nQuery: {query}")
        result = enhancer.enhance_mathematical_reasoning(query)
        print(f"Problem Type: {result.get('problem_type', 'unknown')}")
        print(f"Confidence: {result.get('confidence', 0):.2f}")
        if 'enhanced_reasoning' in result:
            print(f"Reasoning: {result['enhanced_reasoning'][:200]}...")
        print("-" * 30)