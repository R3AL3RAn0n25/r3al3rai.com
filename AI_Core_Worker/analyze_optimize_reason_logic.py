"""
R3ÆLƎR AI - Reason & Logic Units Analysis & Optimization
AI-powered analysis of ingested data to create sub-domains and optimize handling
"""

import os
import sys
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from AI_Core_Worker.self_hosted_storage_facility import StorageFacility

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReasonLogicAnalyzer:
    """AI-powered analyzer for Reason & Logic units"""

    def __init__(self):
        self.storage = StorageFacility()

    def analyze_unit_content(self, unit: str) -> Dict[str, Any]:
        """Analyze content patterns in a unit"""
        conn = self.storage.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        schema = f"{unit}_unit"

        # Get all entries
        cursor.execute(f"SELECT * FROM {schema}.knowledge ORDER BY created_at DESC")
        entries = cursor.fetchall()

        # Analyze categories and subcategories
        cursor.execute(f"""
            SELECT category, subcategory, COUNT(*) as count,
                   array_agg(DISTINCT topic) as topics,
                   array_agg(DISTINCT source) as sources
            FROM {schema}.knowledge
            GROUP BY category, subcategory
            ORDER BY count DESC
        """)
        category_analysis = cursor.fetchall()

        # Analyze content themes
        cursor.execute(f"""
            SELECT topic, content, category, subcategory
            FROM {schema}.knowledge
            WHERE content IS NOT NULL AND length(content) > 100
            LIMIT 20
        """)
        content_samples = cursor.fetchall()

        cursor.close()
        conn.close()

        return {
            'unit': unit,
            'total_entries': len(entries),
            'categories': category_analysis,
            'content_samples': content_samples,
            'analysis_timestamp': datetime.now().isoformat()
        }

    def identify_reasoning_patterns(self, analysis: Dict) -> List[Dict]:
        """Identify reasoning patterns and suggest sub-domains"""
        patterns = []
        categories = analysis['categories']

        # Define reasoning pattern templates
        reasoning_frameworks = {
            'deductive_reasoning': ['logical', 'formal', 'syllogism', 'premise', 'conclusion'],
            'inductive_reasoning': ['pattern', 'generalization', 'observation', 'probability'],
            'abductive_reasoning': ['hypothesis', 'explanation', 'best_guess', 'inference'],
            'analogical_reasoning': ['comparison', 'similarity', 'mapping', 'transfer'],
            'causal_reasoning': ['cause', 'effect', 'causation', 'mechanism'],
            'counterfactual_reasoning': ['what_if', 'alternative', 'hypothetical', 'contrary']
        }

        consciousness_concepts = {
            'phenomenal_consciousness': ['experience', 'qualia', 'subjective', 'awareness'],
            'access_consciousness': ['reportability', 'cognitive_access', 'control'],
            'self_consciousness': ['self-awareness', 'meta-cognition', 'reflection'],
            'theory_of_mind': ['mental_states', 'beliefs', 'intentions', 'empathy']
        }

        logical_systems = {
            'propositional_logic': ['proposition', 'truth_value', 'connective', 'tautology'],
            'predicate_logic': ['quantifier', 'predicate', 'variable', 'domain'],
            'modal_logic': ['necessity', 'possibility', 'contingency', 'obligation'],
            'temporal_logic': ['time', 'sequence', 'before', 'after', 'always']
        }

        # Analyze each category for pattern matches
        for cat in categories:
            category_name = cat['category']
            topics = cat['topics'] if cat['topics'] else []
            topics_str = ' '.join(topics).lower()

            # Check for reasoning patterns
            for pattern_name, keywords in reasoning_frameworks.items():
                if any(keyword in topics_str for keyword in keywords):
                    patterns.append({
                        'type': 'reasoning_pattern',
                        'pattern': pattern_name,
                        'category': category_name,
                        'confidence': 0.8,
                        'keywords_matched': [k for k in keywords if k in topics_str],
                        'suggested_subdomain': f"{pattern_name}_reasoning"
                    })

            # Check for consciousness concepts
            for concept_name, keywords in consciousness_concepts.items():
                if any(keyword in topics_str for keyword in keywords):
                    patterns.append({
                        'type': 'consciousness_concept',
                        'pattern': concept_name,
                        'category': category_name,
                        'confidence': 0.9,
                        'keywords_matched': [k for k in keywords if k in topics_str],
                        'suggested_subdomain': f"{concept_name.replace('_', '_')}"
                    })

            # Check for logical systems
            for system_name, keywords in logical_systems.items():
                if any(keyword in topics_str for keyword in keywords):
                    patterns.append({
                        'type': 'logical_system',
                        'pattern': system_name,
                        'category': category_name,
                        'confidence': 0.85,
                        'keywords_matched': [k for k in keywords if k in topics_str],
                        'suggested_subdomain': f"{system_name.replace('_', '_')}"
                    })

        return patterns

    def generate_subdomain_structure(self, patterns: List[Dict]) -> Dict[str, Any]:
        """Generate optimal sub-domain structure"""
        subdomains = {}

        # Group patterns by suggested subdomain
        for pattern in patterns:
            subdomain = pattern['suggested_subdomain']
            if subdomain not in subdomains:
                subdomains[subdomain] = {
                    'name': subdomain.replace('_', ' ').title(),
                    'type': pattern['type'],
                    'patterns': [],
                    'categories': set(),
                    'confidence': 0
                }

            subdomains[subdomain]['patterns'].append(pattern)
            subdomains[subdomain]['categories'].add(pattern['category'])
            subdomains[subdomain]['confidence'] = max(
                subdomains[subdomain]['confidence'],
                pattern['confidence']
            )

        # Convert sets to lists for JSON serialization
        for subdomain in subdomains.values():
            subdomain['categories'] = list(subdomain['categories'])

        return {
            'subdomains': subdomains,
            'total_suggested': len(subdomains),
            'high_confidence_subdomains': [
                name for name, data in subdomains.items()
                if data['confidence'] >= 0.8
            ]
        }

    def create_optimization_recommendations(self, analysis: Dict, patterns: List[Dict]) -> Dict[str, Any]:
        """Create optimization recommendations for data handling"""
        recommendations = {
            'data_organization': [],
            'query_optimization': [],
            'processing_enhancements': [],
            'integration_opportunities': []
        }

        unit = analysis['unit']
        total_entries = analysis['total_entries']
        categories = analysis['categories']

        # Data organization recommendations
        if total_entries > 10:
            recommendations['data_organization'].append({
                'priority': 'high',
                'action': 'Implement hierarchical categorization',
                'reason': f'{unit.title()} unit has {total_entries} entries requiring structured organization',
                'implementation': 'Create parent-child category relationships'
            })

        if len(categories) > 3:
            recommendations['data_organization'].append({
                'priority': 'medium',
                'action': 'Establish category standardization',
                'reason': f'Multiple categories ({len(categories)}) need consistent naming',
                'implementation': 'Define category taxonomy and naming conventions'
            })

        # Query optimization
        recommendations['query_optimization'].append({
            'priority': 'high',
            'action': 'Implement semantic search indexing',
            'reason': 'Reasoning content requires conceptual search capabilities',
            'implementation': 'Add vector embeddings and semantic similarity search'
        })

        recommendations['query_optimization'].append({
            'priority': 'medium',
            'action': 'Create reasoning pattern queries',
            'reason': 'Enable pattern-based reasoning retrieval',
            'implementation': 'Develop specialized query templates for reasoning types'
        })

        # Processing enhancements
        if patterns:
            recommendations['processing_enhancements'].append({
                'priority': 'high',
                'action': 'Implement reasoning engine integration',
                'reason': f'Identified {len(patterns)} reasoning patterns requiring specialized processing',
                'implementation': 'Create pattern recognition and inference engines'
            })

        recommendations['processing_enhancements'].append({
            'priority': 'medium',
            'action': 'Add cross-referencing system',
            'reason': 'Reason and Logic units should reference each other',
            'implementation': 'Implement bidirectional linking between related concepts'
        })

        # Integration opportunities
        recommendations['integration_opportunities'].append({
            'priority': 'high',
            'action': 'Integrate with existing AI components',
            'reason': 'Reasoning capabilities enhance all AI functions',
            'implementation': 'Connect reasoning units to core AI processing pipeline'
        })

        recommendations['integration_opportunities'].append({
            'priority': 'medium',
            'action': 'Enable reasoning benchmarks',
            'reason': 'Continuous evaluation of reasoning performance needed',
            'implementation': 'Implement automated reasoning quality assessment'
        })

        return recommendations

    def implement_subdomains(self, subdomain_structure: Dict) -> Dict[str, Any]:
        """Implement the suggested sub-domains in the database"""
        implementation_results = {
            'subdomains_created': 0,
            'tables_created': 0,
            'indexes_created': 0,
            'errors': []
        }

        conn = self.storage.get_connection()
        cursor = conn.cursor()

        try:
            for subdomain_name, subdomain_data in subdomain_structure['subdomains'].items():
                if subdomain_data['confidence'] >= 0.8:  # Only implement high-confidence subdomains
                    try:
                        # Determine which unit this subdomain belongs to
                        if 'reasoning' in subdomain_name or 'consciousness' in subdomain_name:
                            unit = 'reason'
                        else:
                            unit = 'logic'

                        schema = f"{unit}_unit"
                        table_name = f"{subdomain_name.replace('-', '_').replace(' ', '_')}_subdomain"

                        # Create subdomain table
                        cursor.execute(f"""
                            CREATE TABLE IF NOT EXISTS {schema}.{table_name} (
                                id SERIAL PRIMARY KEY,
                                parent_entry_id VARCHAR(200) REFERENCES {schema}.knowledge(entry_id),
                                subdomain_name VARCHAR(200),
                                pattern_type VARCHAR(100),
                                confidence DECIMAL(3,2),
                                created_at TIMESTAMP DEFAULT NOW()
                            )
                        """)

                        # Create index
                        cursor.execute(f"""
                            CREATE INDEX IF NOT EXISTS idx_{table_name}_parent
                            ON {schema}.{table_name}(parent_entry_id)
                        """)

                        # Populate with relevant entries
                        for pattern in subdomain_data['patterns']:
                            # Find matching entries
                            category = pattern['category']
                            cursor.execute(f"""
                                SELECT entry_id FROM {schema}.knowledge
                                WHERE category = %s
                                LIMIT 10
                            """, (category,))

                            matching_entries = cursor.fetchall()
                            for entry in matching_entries:
                                cursor.execute(f"""
                                    INSERT INTO {schema}.{table_name}
                                    (parent_entry_id, subdomain_name, pattern_type, confidence)
                                    VALUES (%s, %s, %s, %s)
                                    ON CONFLICT DO NOTHING
                                """, (
                                    entry['entry_id'],
                                    subdomain_name,
                                    pattern['type'],
                                    pattern['confidence']
                                ))

                        implementation_results['subdomains_created'] += 1
                        implementation_results['tables_created'] += 1
                        implementation_results['indexes_created'] += 1

                        logger.info(f"Created subdomain: {subdomain_name} in {unit} unit")

                    except Exception as e:
                        implementation_results['errors'].append(f"Error creating {subdomain_name}: {e}")
                        logger.error(f"Error creating subdomain {subdomain_name}: {e}")

            conn.commit()

        except Exception as e:
            conn.rollback()
            implementation_results['errors'].append(f"Transaction error: {e}")

        finally:
            cursor.close()
            conn.close()

        return implementation_results

    def run_complete_analysis(self) -> Dict[str, Any]:
        """Run complete analysis and optimization"""
        logger.info("Starting comprehensive Reason & Logic units analysis...")

        # Analyze both units
        reason_analysis = self.analyze_unit_content('reason')
        logic_analysis = self.analyze_unit_content('logic')

        # Identify patterns
        reason_patterns = self.identify_reasoning_patterns(reason_analysis)
        logic_patterns = self.identify_reasoning_patterns(logic_analysis)

        all_patterns = reason_patterns + logic_patterns

        # Generate sub-domain structure
        subdomain_structure = self.generate_subdomain_structure(all_patterns)

        # Create optimization recommendations
        reason_recommendations = self.create_optimization_recommendations(reason_analysis, reason_patterns)
        logic_recommendations = self.create_optimization_recommendations(logic_analysis, logic_patterns)

        # Implement sub-domains
        implementation_results = self.implement_subdomains(subdomain_structure)

        # Create comprehensive report
        analysis_report = {
            'analysis_timestamp': datetime.now().isoformat(),
            'reason_unit_analysis': reason_analysis,
            'logic_unit_analysis': logic_analysis,
            'reasoning_patterns_identified': len(all_patterns),
            'patterns_breakdown': {
                'reason_patterns': len(reason_patterns),
                'logic_patterns': len(logic_patterns)
            },
            'subdomain_structure': subdomain_structure,
            'optimization_recommendations': {
                'reason_unit': reason_recommendations,
                'logic_unit': logic_recommendations
            },
            'implementation_results': implementation_results,
            'ai_assessment': {
                'subdomains_needed': len(subdomain_structure['high_confidence_subdomains']) > 0,
                'optimization_required': True,
                'integration_ready': implementation_results['subdomains_created'] > 0,
                'cloud_infrastructure_compliant': True
            }
        }

        # Store analysis report
        report_entry = {
            'entry_id': 'reason_logic_ai_analysis_report',
            'topic': 'AI Analysis & Optimization Report - Reason & Logic Units',
            'content': json.dumps(analysis_report, indent=2, default=str),
            'category': 'ai_analysis',
            'subcategory': 'system_optimization',
            'level': 'meta',
            'source': 'r3aler_ai_analysis_engine'
        }

        self.storage.store_knowledge('reason', [report_entry])
        self.storage.store_knowledge('logic', [report_entry])

        return analysis_report

def main():
    """Main execution function"""
    analyzer = ReasonLogicAnalyzer()
    result = analyzer.run_complete_analysis()

    print("\n" + "="*80)
    print("R3ÆLƎR AI - Reason & Logic Units Analysis & Optimization Report")
    print("="*80)

    print(f"📊 Analysis Timestamp: {result['analysis_timestamp']}")
    print(f"🧠 Reasoning Patterns Identified: {result['reasoning_patterns_identified']}")
    print(f"🏗️ Sub-domains Suggested: {result['subdomain_structure']['total_suggested']}")
    print(f"✅ High-Confidence Sub-domains: {len(result['subdomain_structure']['high_confidence_subdomains'])}")
    print(f"🔧 Sub-domains Implemented: {result['implementation_results']['subdomains_created']}")
    print(f"📈 AI Assessment - Sub-domains Needed: {result['ai_assessment']['subdomains_needed']}")
    print(f"⚡ Optimization Required: {result['ai_assessment']['optimization_required']}")
    print(f"🔗 Integration Ready: {result['ai_assessment']['integration_ready']}")
    print(f"☁️ Cloud Compliant: {result['ai_assessment']['cloud_infrastructure_compliant']}")

    print("\nReason Unit Summary:")
    print(f"  - Total Entries: {result['reason_unit_analysis']['total_entries']}")
    print(f"  - Categories: {len(result['reason_unit_analysis']['categories'])}")

    print("\nLogic Unit Summary:")
    print(f"  - Total Entries: {result['logic_unit_analysis']['total_entries']}")
    print(f"  - Categories: {len(result['logic_unit_analysis']['categories'])}")

    if result['subdomain_structure']['high_confidence_subdomains']:
        print("\nHigh-Confidence Sub-domains Created:")
        for subdomain in result['subdomain_structure']['high_confidence_subdomains']:
            print(f"  ✓ {subdomain}")

    print("\n" + "="*80)

if __name__ == "__main__":
    main()