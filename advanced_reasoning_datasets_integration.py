"""
R3ÆLƎR AI Advanced Reasoning Datasets Integration
Integrates 12 specialized reasoning and logic datasets into the Storage Facility
"""

import os
import sys
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import time

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'AI_Core_Worker'))

try:
    from AI_Core_Worker.self_hosted_storage_facility import StorageFacility
    from datasets import load_dataset
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install required packages:")
    print("pip install datasets psycopg2-binary")
    sys.exit(1)

# Configure Hugging Face datasets to use R: drive for cache (119GB free space available)
os.environ['HF_DATASETS_CACHE'] = r'R:\hf_datasets_cache'
os.environ['HF_HOME'] = r'R:\hf_home'

# Ensure cache directories exist
os.makedirs(r'R:\hf_datasets_cache', exist_ok=True)
os.makedirs(r'R:\hf_home', exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dataset_integration.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AdvancedReasoningDatasetsIntegration:
    """
    Integrates advanced reasoning and logic datasets into R3ÆLƎR Storage Facility
    """

    def __init__(self):
        self.facility = StorageFacility()
        self.datasets_config = {
            "opencode_reasoning": {
                "dataset": "nvidia/OpenCodeReasoning",
                "config": "split_0",
                "unit": "code",
                "description": "Code reasoning and programming logic",
                "max_samples": 1000,
                "requires_auth": True
            },
            "physics_reasoning": {
                "dataset": "multimodal-reasoning-lab/Physics",
                "unit": "physics",
                "description": "Advanced physics reasoning problems",
                "max_samples": 500,
                "requires_auth": True
            },
            "arc_eval": {
                "dataset": "multi-domain-reasoning/arc_eval",
                "unit": "reason",
                "description": "Multi-domain reasoning evaluation",
                "max_samples": 1000,
                "requires_auth": False
            },
            "claude_reasoning": {
                "dataset": "TeichAI/claude-sonnet-4.5-high-reasoning-250x",
                "unit": "reason",
                "description": "High-level AI reasoning patterns",
                "max_samples": 250,
                "requires_auth": True,
                "custom_prompt": True
            },
            "logi_glue_rules": {
                "dataset": "logicreasoning/logi_glue",
                "config": "Rulebert-Union-Rules",
                "unit": "logic",
                "description": "Logical reasoning with rules",
                "max_samples": 500,
                "requires_auth": False
            },
            "logi_glue_animal": {
                "dataset": "logicreasoning/logi_glue",
                "config": "abduction_animal",
                "unit": "logic",
                "description": "Abductive reasoning with animals",
                "max_samples": 500,
                "requires_auth": False
            },
            "logi_glue_person": {
                "dataset": "logicreasoning/logi_glue",
                "config": "abduction_person",
                "unit": "logic",
                "description": "Abductive reasoning with persons",
                "max_samples": 500,
                "requires_auth": False
            },
            "formal_logic_simple": {
                "dataset": "pccl-org/formal-logic-simple-order-simple-objects-clavorier-500",
                "unit": "logic",
                "description": "Formal logic with simple objects",
                "max_samples": 500,
                "requires_auth": False
            },
            "formal_logic_complex": {
                "dataset": "pccl-org/formal-logic-simple-order-new-objects-bigger-50",
                "unit": "logic",
                "description": "Formal logic with complex objects",
                "max_samples": 50,
                "requires_auth": False
            },
            "prop_logic": {
                "dataset": "marc-er/prop_logic",
                "unit": "logic",
                "description": "Propositional logic problems",
                "max_samples": 1000,
                "requires_auth": False
            },
            "logical_fallacies": {
                "dataset": "brucewlee1/mmlu-logical-fallacies",
                "unit": "logic",
                "description": "Logical fallacies identification",
                "max_samples": 500,
                "requires_auth": False
            },
            "mbpp": {
                "dataset": "google-research-datasets/mbpp",
                "config": "full",
                "unit": "code",
                "description": "Code generation and programming problems",
                "max_samples": 1000,
                "requires_auth": False
            }
        }

    def load_dataset_entries(self, dataset_config: Dict) -> List[Dict]:
        """Load and process a dataset into knowledge entries"""
        dataset_name = dataset_config["dataset"]
        config = dataset_config.get("config")
        max_samples = dataset_config.get("max_samples", 1000)

        logger.info(f"Loading dataset: {dataset_name}")

        try:
            # Check disk space on R: drive before downloading (where cache is stored)
            import shutil
            total, used, free = shutil.disk_usage('R:')
            free_gb = free / (1024**3)
            if free_gb < 5.0:  # Less than 5GB free on R: drive (119GB total available)
                logger.warning(f"Low disk space on R: drive: {free_gb:.2f}GB free. Skipping {dataset_name}")
                return []

            # Load dataset with streaming to save space
            if config:
                ds = load_dataset(dataset_name, config, streaming=True)
            else:
                ds = load_dataset(dataset_name, streaming=True)

            # Get the first split (usually 'train')
            split_name = list(ds.keys())[0]
            dataset = ds[split_name]

            entries = []
            processed_count = 0

            # Convert to iterator for streaming
            for example in dataset:
                if processed_count >= max_samples:
                    break

                # Process the entry based on dataset type
                entry = self.process_entry(example, dataset_config)
                if entry:
                    entries.append(entry)
                    processed_count += 1

            logger.info(f"Processed {processed_count} entries from {dataset_name}")
            return entries

        except Exception as e:
            logger.warning(f"Failed to load dataset {dataset_name}: {e}")
            return []

    def process_entry(self, example: Dict, dataset_config: Dict) -> Optional[Dict]:
        """Process a single dataset entry"""
        dataset_name = dataset_config["dataset"]

        # Route to appropriate processing method
        if "opencode" in dataset_name.lower():
            return self.process_code_reasoning_entry(example, dataset_config)
        elif "physics_reasoning" in dataset_config.get("description", "").lower():
            return self.process_physics_reasoning_entry(example, dataset_config)
        elif "arc_eval" in dataset_config.get("description", "").lower():
            return self.process_arc_eval_entry(example, dataset_config)
        elif "claude_reasoning" in dataset_config.get("description", "").lower():
            return self.process_claude_reasoning_entry(example, dataset_config)
        elif "logi_glue" in dataset_name:
            return self.process_logi_glue_entry(example, dataset_config)
        elif "formal-logic" in dataset_name:
            return self.process_formal_logic_entry(example, dataset_config)
        elif "prop_logic" in dataset_name:
            return self.process_prop_logic_entry(example, dataset_config)
        elif "logical-fallacies" in dataset_name:
            return self.process_fallacies_entry(example, dataset_config)
        elif "mbpp" in dataset_name:
            return self.process_mbpp_entry(example, dataset_config)
        else:
            # Generic processing
            return self.process_generic_entry(example, dataset_config)

    def process_code_reasoning_entry(self, example: Dict, config: Dict) -> Optional[Dict]:
        """Process OpenCodeReasoning dataset entry"""
        content = example.get('problem', '')
        solution = example.get('solution', '')

        if not content:
            return None

        return {
            'id': f"opencode_{hash(content) % 1000000}",
            'topic': 'Code Reasoning',
            'content': f"Problem: {content}\n\nSolution: {solution}",
            'category': 'Programming',
            'subcategory': 'Code Reasoning',
            'level': 'Advanced',
            'source': 'NVIDIA OpenCodeReasoning'
        }

    def process_physics_reasoning_entry(self, example: Dict, config: Dict) -> Optional[Dict]:
        """Process Physics reasoning dataset entry"""
        question = example.get('question', '')
        answer = example.get('answer', '')
        explanation = example.get('explanation', '')

        if not question:
            return None

        return {
            'id': f"physics_reason_{hash(question) % 1000000}",
            'topic': 'Physics Reasoning',
            'content': f"Question: {question}\n\nAnswer: {answer}\n\nExplanation: {explanation}",
            'category': 'Physics',
            'subcategory': 'Reasoning',
            'level': 'Advanced',
            'source': 'Multimodal Reasoning Lab Physics'
        }

    def process_arc_eval_entry(self, example: Dict, config: Dict) -> Optional[Dict]:
        """Process ARC evaluation dataset entry"""
        question = example.get('question', '')
        choices = example.get('choices', [])
        answer = example.get('answerKey', '')

        if not question:
            return None

        choices_text = '\n'.join([f"{chr(65+i)}. {choice}" for i, choice in enumerate(choices)])

        return {
            'id': f"arc_{hash(question) % 1000000}",
            'topic': 'Multi-domain Reasoning',
            'content': f"Question: {question}\n\nChoices:\n{choices_text}\n\nCorrect Answer: {answer}",
            'category': 'Reasoning',
            'subcategory': 'Multi-domain',
            'level': 'Advanced',
            'source': 'ARC Evaluation'
        }

    def process_claude_reasoning_entry(self, example: Dict, config: Dict) -> Optional[Dict]:
        """Process Claude reasoning dataset entry"""
        content = example.get('content', '')
        reasoning = example.get('reasoning', '')

        if not content:
            return None

        return {
            'id': f"claude_{hash(content) % 1000000}",
            'topic': 'AI Reasoning',
            'content': f"Content: {content}\n\nReasoning: {reasoning}",
            'category': 'Reasoning',
            'subcategory': 'AI Patterns',
            'level': 'Advanced',
            'source': 'Claude Reasoning Dataset'
        }

    def process_logi_glue_entry(self, example: Dict, config: Dict) -> Optional[Dict]:
        """Process LogiGLUE dataset entry"""
        premise = example.get('premise', '')
        hypothesis = example.get('hypothesis', '')
        label = example.get('label', '')

        if not premise:
            return None

        return {
            'id': f"logi_glue_{hash(premise) % 1000000}",
            'topic': 'Logical Reasoning',
            'content': f"Premise: {premise}\n\nHypothesis: {hypothesis}\n\nLabel: {label}",
            'category': 'Logic',
            'subcategory': 'Reasoning',
            'level': 'Advanced',
            'source': 'LogiGLUE Dataset'
        }

    def process_formal_logic_entry(self, example: Dict, config: Dict) -> Optional[Dict]:
        """Process Formal Logic dataset entry"""
        problem = example.get('problem', '')
        solution = example.get('solution', '')

        if not problem:
            return None

        return {
            'id': f"formal_logic_{hash(problem) % 1000000}",
            'topic': 'Formal Logic',
            'content': f"Problem: {problem}\n\nSolution: {solution}",
            'category': 'Logic',
            'subcategory': 'Formal Logic',
            'level': 'Advanced',
            'source': 'Formal Logic Dataset'
        }

    def process_prop_logic_entry(self, example: Dict, config: Dict) -> Optional[Dict]:
        """Process Propositional Logic dataset entry"""
        premise = example.get('premise', '')
        hypothesis = example.get('hypothesis', '')
        label = example.get('label', '')

        if not premise:
            return None

        return {
            'id': f"prop_logic_{hash(premise) % 1000000}",
            'topic': 'Propositional Logic',
            'content': f"Premise: {premise}\n\nHypothesis: {hypothesis}\n\nEntailment: {label}",
            'category': 'Logic',
            'subcategory': 'Propositional',
            'level': 'Advanced',
            'source': 'Propositional Logic Dataset'
        }

    def process_fallacies_entry(self, example: Dict, config: Dict) -> Optional[Dict]:
        """Process Logical Fallacies dataset entry"""
        question = example.get('question', '')
        choices = example.get('choices', [])
        answer = example.get('answer', '')

        if not question:
            return None

        choices_text = '\n'.join([f"{chr(65+i)}. {choice}" for i, choice in enumerate(choices)])

        return {
            'id': f"fallacies_{hash(question) % 1000000}",
            'topic': 'Logical Fallacies',
            'content': f"Question: {question}\n\nChoices:\n{choices_text}\n\nCorrect Answer: {answer}",
            'category': 'Logic',
            'subcategory': 'Fallacies',
            'level': 'Advanced',
            'source': 'MMLU Logical Fallacies'
        }

    def process_mbpp_entry(self, example: Dict, config: Dict) -> Optional[Dict]:
        """Process MBPP dataset entry"""
        task_id = example.get('task_id', '')
        text = example.get('text', '')
        code = example.get('code', '')
        test_list = example.get('test_list', [])

        if not text:
            return None

        test_cases = '\n'.join(test_list) if test_list else 'No test cases provided'

        return {
            'id': f"mbpp_{task_id}",
            'topic': 'Code Generation',
            'content': f"Task: {text}\n\nCode:\n{code}\n\nTest Cases:\n{test_cases}",
            'category': 'Programming',
            'subcategory': 'Code Generation',
            'level': 'Intermediate',
            'source': 'MBPP Dataset'
        }

    def process_generic_entry(self, example: Dict, config: Dict) -> Optional[Dict]:
        """Generic processing for unrecognized datasets"""
        content_parts = []
        for key, value in example.items():
            if isinstance(value, str) and value:
                content_parts.append(f"{key.title()}: {value}")

        content = '\n\n'.join(content_parts)
        if not content:
            return None

        return {
            'id': f"generic_{hash(content) % 1000000}",
            'topic': config.get('description', 'Unknown'),
            'content': content,
            'category': config.get('unit', 'Unknown'),
            'subcategory': 'Dataset',
            'level': 'Mixed',
            'source': config.get('dataset', 'Unknown')
        }

    def integrate_datasets(self):
        """Main integration function - stores data in cloud Storage Facility, not locally"""
        logger.info("Starting Advanced Reasoning Datasets Integration")
        logger.info("📚 Data will be stored in R3ÆLƎR Cloud Storage Facility (PostgreSQL), not on local machine")
        logger.info("💾 Temporary downloads use R: drive cache (119GB available)")

        total_entries = 0

        for dataset_key, config in self.datasets_config.items():
            logger.info(f"Processing dataset: {dataset_key}")

            # Check if authentication is required
            if config.get('requires_auth', False):
                logger.warning(f"Dataset {dataset_key} requires authentication. Please ensure you are logged in with: huggingface-cli login")

            # Load dataset entries
            entries = self.load_dataset_entries(config)

            if not entries:
                logger.warning(f"No entries loaded for {dataset_key}")
                continue

            # Store in appropriate unit
            unit_id = config['unit']
            result = self.facility.store_knowledge(unit_id, entries)

            if 'error' in result:
                logger.error(f"Failed to store {dataset_key}: {result['error']}")
            else:
                stored = result.get('stored', 0)
                total_entries += stored
                logger.info(f"Successfully stored {stored} entries for {dataset_key}")

            # Small delay to avoid overwhelming the system
            time.sleep(1)

        logger.info(f"Integration complete! Total entries processed: {total_entries}")
        return total_entries

def main():
    """Main execution function"""
    print("🔬 R3ÆLƎR AI Advanced Reasoning Datasets Integration")
    print("=" * 60)

    try:
        integrator = AdvancedReasoningDatasetsIntegration()
        total_entries = integrator.integrate_datasets()

        print("\n✅ Integration Complete!")
        print(f"📊 Total entries integrated: {total_entries}")
        print("\n📚 Datasets integrated:")
        for key, config in integrator.datasets_config.items():
            print(f"  • {key}: {config['description']}")

    except Exception as e:
        logger.error(f"Integration failed: {e}")
        print(f"\n❌ Integration failed: {e}")
        print("Please check the logs for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()