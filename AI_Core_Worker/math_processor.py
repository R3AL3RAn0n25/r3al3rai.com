"""
math_processor.py - Symbolic Mathematics Processing for R3ÆLƎR AI
Enhances mathematical reasoning capabilities for benchmark improvement
"""

import re
import sympy as sp
from typing import Optional, Dict, Any
import logging
import traceback

class SymbolicMathProcessor:
    """
    Handles symbolic mathematics, equation solving, and numerical computations
    Integrates with R3ÆLƎR AI to improve GSM8K benchmark performance
    """

    def __init__(self):
        # Initialize SymPy
        sp.init_printing()

        # Mathematical patterns for recognition
        self.math_patterns = {
            # Basic arithmetic
            r'(\d+(?:\.\d+)?)\s*([\+\-\*\/])\s*(\d+(?:\.\d+)?)': self.solve_arithmetic,

            # Equation solving
            r'solve\s+(.+?)\s*(?:for\s+(.+?))?\s*$': self.solve_equation,

            # Derivatives
            r'(?:differentiate|derivative|d/dx)\s+(.+?)(?:\s+with\s+respect\s+to\s+(.+?))?$': self.differentiate,

            # Integrals
            r'(?:integrate|integral)\s+(.+?)\s+d(.+?)(?:\s+from\s+(.+?)\s+to\s+(.+?))?$': self.integrate,

            # Factorials
            r'(\d+)!': lambda num: sp.factorial(int(num)),

            # Powers and roots
            r'(\d+(?:\.\d+)?)\s*\^\s*(\d+(?:\.\d+)?)': lambda base, exp: float(base) ** float(exp),
            r'sqrt\s*\(\s*(\d+(?:\.\d+)?)\s*\)': lambda x: sp.sqrt(float(x)),

            # Trigonometric functions
            r'sin\s*\(\s*(\d+(?:\.\d+)?)\s*\)': lambda x: sp.sin(float(x)),
            r'cos\s*\(\s*(\d+(?:\.\d+)?)\s*\)': lambda x: sp.cos(float(x)),
            r'tan\s*\(\s*(\d+(?:\.\d+)?)\s*\)': lambda x: sp.tan(float(x)),
        }

        # Common mathematical keywords
        self.math_keywords = {
            'calculate', 'compute', 'solve', 'evaluate', 'simplify',
            'factor', 'expand', 'math', 'mathematics', 'algebra',
            'calculus', 'geometry', 'trigonometry', 'equation'
        }

        logging.info("SymbolicMathProcessor initialized")

    def is_math_query(self, query: str) -> bool:
        """Check if query contains mathematical content"""
        query_lower = query.lower()

        # Check for mathematical keywords
        if any(keyword in query_lower for keyword in self.math_keywords):
            return True

        # Check for mathematical symbols
        math_symbols = ['=', '+', '-', '*', '/', '^', 'sqrt', 'sin', 'cos', 'tan', '∫', '∂']
        if any(symbol in query for symbol in math_symbols):
            return True

        # Check for numbers and operators
        if re.search(r'\d', query) and re.search(r'[\+\-\*\/\^\=]', query):
            return True

        return False

    def process_query(self, query: str) -> Optional[str]:
        """
        Process mathematical query and return solution
        Returns None if not a mathematical query or unable to solve
        """
        if not self.is_math_query(query):
            return None

        try:
            # Try each pattern
            for pattern, handler in self.math_patterns.items():
                match = re.search(pattern, query, re.IGNORECASE)
                if match:
                    result = handler(*match.groups())
                    if result is not None:
                        return self.format_result(result, query)

            # If no pattern matches, try general symbolic evaluation
            return self.evaluate_expression(query)

        except Exception as e:
            logging.error(f"Math processing failed for query '{query}': {e}")
            return None

    def solve_arithmetic(self, num1: str, op: str, num2: str) -> Optional[float]:
        """Solve basic arithmetic operations"""
        try:
            n1, n2 = float(num1), float(num2)

            if op == '+':
                return n1 + n2
            elif op == '-':
                return n1 - n2
            elif op == '*':
                return n1 * n2
            elif op == '/':
                if n2 != 0:
                    return n1 / n2
                else:
                    return None
        except ValueError:
            return None
        return None

    def solve_equation(self, equation: str, variable: str = 'x') -> Optional[str]:
        """Solve algebraic equations"""
        try:
            # Clean up the equation
            equation = equation.replace(' ', '').replace('=', '-(') + ')'

            # Parse with SymPy
            if variable:
                x = sp.Symbol(variable)
            else:
                x = sp.Symbol('x')

            # Try to solve
            solutions = sp.solve(sp.sympify(equation), x)

            if solutions:
                return f"Solutions: {solutions}"
            else:
                return "No solutions found"

        except Exception as e:
            logging.error(f"Equation solving failed: {e}")
            return None

    def differentiate(self, expression: str, variable: str = 'x') -> Optional[str]:
        """Compute derivatives"""
        try:
            x = sp.Symbol(variable)
            expr = sp.sympify(expression)
            derivative = sp.diff(expr, x)

            return f"d/d{variable}({expression}) = {derivative}"

        except Exception as e:
            logging.error(f"Differentiation failed: {e}")
            return None

    def integrate(self, expression: str, variable: str, lower: str = None, upper: str = None) -> Optional[str]:
        """Compute integrals"""
        try:
            x = sp.Symbol(variable)
            expr = sp.sympify(expression)

            if lower and upper:
                # Definite integral
                result = sp.integrate(expr, (x, sp.sympify(lower), sp.sympify(upper)))
                return f"∫({expression}) d{variable} from {lower} to {upper} = {result}"
            else:
                # Indefinite integral
                result = sp.integrate(expr, x)
                return f"∫({expression}) d{variable} = {result} + C"

        except Exception as e:
            logging.error(f"Integration failed: {e}")
            return None

    def factorial(self, n: str) -> Optional[int]:
        """Compute factorial"""
        try:
            n = int(n)
            if n >= 0 and n <= 100:  # Reasonable limit
                return sp.factorial(n)
            return None
        except ValueError:
            return None

    def power(self, base: str, exponent: str) -> Optional[float]:
        """Compute power"""
        try:
            base, exp = float(base), float(exponent)
            return base ** exp
        except ValueError:
            return None

    def square_root(self, n: str) -> Optional[float]:
        """Compute square root"""
        try:
            n = float(n)
            if n >= 0:
                return sp.sqrt(n)
            return None
        except ValueError:
            return None

    def evaluate_expression(self, expression: str) -> Optional[str]:
        """Evaluate general mathematical expressions"""
        try:
            # Remove common text and keep only mathematical expression
            expr = re.sub(r'[^\d\w\+\-\*\/\^\(\)\.\s]', '', expression)
            expr = expr.strip()

            if not expr:
                return None

            # Try to evaluate with SymPy
            result = sp.sympify(expr)
            return f"Result: {result}"

        except Exception as e:
            logging.error(f"Expression evaluation failed: {e}")
            return None

    def format_result(self, result: Any, original_query: str) -> str:
        """Format mathematical result for response"""
        if isinstance(result, (int, float, sp.Basic)):
            return f"**Mathematical Solution**\n\nFor: {original_query}\n\n**Result:** {result}"
        elif isinstance(result, str):
            return f"**Mathematical Solution**\n\nFor: {original_query}\n\n{result}"
        else:
            return f"**Mathematical Solution**\n\nFor: {original_query}\n\n**Result:** {str(result)}"


# Integration function for R3ÆLƎR AI
def integrate_math_processor(realer_ai_instance):
    """
    Integrate mathematical processor into R3ÆLƎR AI response chain
    Add as Priority 1.5 (between prompts and DeepAnalyze)
    """
    math_processor = SymbolicMathProcessor()
    realer_ai_instance.math_processor = math_processor

    # Monkey patch the process_chat method to include math processing
    original_process_chat = realer_ai_instance.process_chat

    def enhanced_process_chat(user_message, user_id=None, conversation_history=None):
        # Try math processing first
        math_result = math_processor.process_query(user_message)
        if math_result:
            logging.info("Math processor handled query")
            return math_result

        # Fall back to original processing
        return original_process_chat(user_message, user_id, conversation_history)

    realer_ai_instance.process_chat = enhanced_process_chat
    logging.info("Mathematical processor integrated into R3ÆLƎR AI")


if __name__ == "__main__":
    # Test the math processor
    processor = SymbolicMathProcessor()

    test_queries = [
        "What is 15 + 27?",
        "Solve x^2 - 4 = 0",
        "Differentiate x^2 + 3x + 1",
        "Integrate 2x dx",
        "What is 5!",
        "Calculate 2^8",
        "What is the square root of 144?"
    ]

    print("Testing Mathematical Processor:")
    print("=" * 50)

    for query in test_queries:
        result = processor.process_query(query)
        print(f"Query: {query}")
        print(f"Result: {result}")
        print("-" * 30)