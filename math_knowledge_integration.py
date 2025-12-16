#!/usr/bin/env python3
"""
math_knowledge_integration.py - Integrate math datasets into R3ÆLƎR storage facility
"""

import json
import sys
import os
from typing import List, Dict, Any

# Add the AI_Core_Worker directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'AI_Core_Worker'))

try:
    from self_hosted_storage_facility import StorageFacility
    STORAGE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import storage facility: {e}")
    STORAGE_AVAILABLE = False

class MathKnowledgeIntegrator:
    """Integrate math datasets into the storage facility"""

    def __init__(self):
        self.facility = None
        if STORAGE_AVAILABLE:
            try:
                self.facility = StorageFacility()
                print("✅ Storage facility initialized")
            except Exception as e:
                print(f"❌ Failed to initialize storage facility: {e}")

    def load_math_datasets(self) -> List[Dict]:
        """Load math datasets from JSON file"""
        try:
            with open('math_datasets_integrated.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"✅ Loaded {len(data)} math entries from file")
            return data
        except FileNotFoundError:
            print("❌ Math datasets file not found")
            return []
        except Exception as e:
            print(f"❌ Error loading math datasets: {e}")
            return []

    def create_additional_math_entries(self) -> List[Dict]:
        """Create additional math entries manually"""
        math_entries = [
            # Basic arithmetic
            {
                'id': 'math_basic_001',
                'topic': 'Basic Arithmetic',
                'content': 'What is 15 + 27?',
                'answer': '42',
                'explanation': '15 + 27 = 42',
                'category': 'arithmetic',
                'subcategory': 'addition',
                'level': 'elementary',
                'source': 'R3AL3R_Manual'
            },
            {
                'id': 'math_basic_002',
                'topic': 'Basic Arithmetic',
                'content': 'What is 63 - 28?',
                'answer': '35',
                'explanation': '63 - 28 = 35',
                'category': 'arithmetic',
                'subcategory': 'subtraction',
                'level': 'elementary',
                'source': 'R3AL3R_Manual'
            },
            {
                'id': 'math_basic_003',
                'topic': 'Basic Arithmetic',
                'content': 'What is 12 × 8?',
                'answer': '96',
                'explanation': '12 × 8 = 96',
                'category': 'arithmetic',
                'subcategory': 'multiplication',
                'level': 'elementary',
                'source': 'R3AL3R_Manual'
            },
            {
                'id': 'math_basic_004',
                'topic': 'Basic Arithmetic',
                'content': 'What is 144 ÷ 12?',
                'answer': '12',
                'explanation': '144 ÷ 12 = 12',
                'category': 'arithmetic',
                'subcategory': 'division',
                'level': 'elementary',
                'source': 'R3AL3R_Manual'
            },
            # Word problems
            {
                'id': 'math_word_001',
                'topic': 'Word Problems',
                'content': 'Sarah has 24 apples. She gives 8 apples to each of her 3 friends. How many apples does she have left?',
                'answer': '0',
                'explanation': 'Sarah gives 8 × 3 = 24 apples to her friends. She started with 24 apples, so 24 - 24 = 0 apples left.',
                'category': 'arithmetic',
                'subcategory': 'word_problems',
                'level': 'elementary',
                'source': 'R3AL3R_Manual'
            },
            {
                'id': 'math_word_002',
                'topic': 'Word Problems',
                'content': 'A train travels at 60 miles per hour. How far will it travel in 3.5 hours?',
                'answer': '210 miles',
                'explanation': 'Distance = speed × time = 60 × 3.5 = 210 miles',
                'category': 'arithmetic',
                'subcategory': 'word_problems',
                'level': 'elementary',
                'source': 'R3AL3R_Manual'
            },
            # Algebra
            {
                'id': 'math_algebra_001',
                'topic': 'Algebra',
                'content': 'Solve for x: 2x + 5 = 17',
                'answer': 'x = 6',
                'explanation': 'Subtract 5 from both sides: 2x = 12. Divide both sides by 2: x = 6.',
                'category': 'algebra',
                'subcategory': 'equation_solving',
                'level': 'intermediate',
                'source': 'R3AL3R_Manual'
            },
            {
                'id': 'math_algebra_002',
                'topic': 'Algebra',
                'content': 'Solve for y: 3y - 7 = 11',
                'answer': 'y = 6',
                'explanation': 'Add 7 to both sides: 3y = 18. Divide both sides by 3: y = 6.',
                'category': 'algebra',
                'subcategory': 'equation_solving',
                'level': 'intermediate',
                'source': 'R3AL3R_Manual'
            },
            # Geometry
            {
                'id': 'math_geometry_001',
                'topic': 'Geometry',
                'content': 'What is the area of a rectangle with length 8 cm and width 5 cm?',
                'answer': '40 square cm',
                'explanation': 'Area of rectangle = length × width = 8 × 5 = 40 square cm',
                'category': 'geometry',
                'subcategory': 'area_calculation',
                'level': 'elementary',
                'source': 'R3AL3R_Manual'
            },
            {
                'id': 'math_geometry_002',
                'topic': 'Geometry',
                'content': 'What is the circumference of a circle with radius 7 cm? (Use π ≈ 3.14)',
                'answer': '43.96 cm',
                'explanation': 'Circumference = 2 × π × radius = 2 × 3.14 × 7 = 43.96 cm',
                'category': 'geometry',
                'subcategory': 'circumference',
                'level': 'intermediate',
                'source': 'R3AL3R_Manual'
            }
        ]

        print(f"✅ Created {len(math_entries)} additional math entries manually")
        return math_entries

    def integrate_math_knowledge(self):
        """Integrate all math knowledge into the storage facility"""
        if not self.facility:
            print("❌ Storage facility not available")
            return

        print("🧮 Integrating Math Knowledge into Storage Facility")
        print("=" * 60)

        # Load datasets
        math_data = []
        math_data.extend(self.load_math_datasets())
        math_data.extend(self.create_additional_math_entries())

        if not math_data:
            print("❌ No math data to integrate")
            return

        print(f"📊 Total math entries to integrate: {len(math_data)}")

        # Store in the physics unit (since it handles mathematical physics too)
        # Actually, let's create a dedicated math unit or use an existing one
        # For now, we'll use the physics unit since it already exists

        result = self.facility.store_knowledge('physics', math_data)

        print("📈 Integration Results:")
        print(f"  • Stored: {result.get('stored', 0)}")
        print(f"  • Updated: {result.get('updated', 0)}")
        print(f"  • Errors: {result.get('errors', 0)}")
        print(f"  • Total processed: {result.get('total', 0)}")

        if result.get('errors', 0) == 0:
            print("✅ Math knowledge integration completed successfully!")
        else:
            print("⚠️ Math knowledge integration completed with some errors")

    def test_math_integration(self):
        """Test that math knowledge was integrated properly"""
        if not self.facility:
            print("❌ Storage facility not available for testing")
            return

        print("\n🧪 Testing Math Knowledge Integration")
        print("-" * 40)

        test_queries = [
            "solve 2x + 5 = 17",
            "area of rectangle 8 by 5",
            "15 + 27",
            "144 ÷ 12"
        ]

        for query in test_queries:
            print(f"Query: '{query}'")
            results = self.facility.search_unit('physics', query, limit=2)
            if results:
                print(f"  ✅ Found {len(results)} results")
                for result in results[:1]:  # Show first result
                    print(f"    Topic: {result.get('topic', 'N/A')}")
                    print(f"    Answer: {result.get('answer', 'N/A')[:50]}...")
            else:
                print("  ❌ No results found")
            print()

def main():
    """Main integration function"""
    print("🧮 R3ÆLƎR AI - Math Knowledge Integration")
    print("=" * 50)

    integrator = MathKnowledgeIntegrator()

    # Integrate math knowledge
    integrator.integrate_math_knowledge()

    # Test integration
    integrator.test_math_integration()

    print("\n🎯 Math knowledge integration complete!")
    print("The AI should now perform better on mathematical benchmarks.")

if __name__ == "__main__":
    main()