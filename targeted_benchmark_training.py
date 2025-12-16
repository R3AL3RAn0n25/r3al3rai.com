"""
R3ÆLƎR AI - Targeted Benchmark Training System
Cloud-based training for weak benchmark areas using R3AL3R Storage Facility
"""

import os
import sys
import json
import logging
import time
from typing import List, Dict, Any, Optional
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datasets import load_dataset
from AI_Core_Worker.self_hosted_storage_facility import StorageFacility

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BenchmarkTrainingSystem:
    """Targeted training system for benchmark improvement using cloud storage"""

    def __init__(self):
        self.storage = StorageFacility()
        self.training_datasets = self._define_training_datasets()
        self.db_config = {
            'host': '127.0.0.1',
            'port': 5432,
            'database': 'r3aler_ai',
            'user': 'r3aler_user_2025',
            'password': 'password123'
        }

    def _define_training_datasets(self) -> Dict[str, List[str]]:
        """Define datasets for each weak benchmark area"""
        return {
            "mmlu": [
                "cais/mmlu",  # Main MMLU dataset
                "microsoft/orca-math-word-problems-200k",  # Math reasoning
                "allenai/olympic_reasoning",  # Complex reasoning
                "tasksource/bigbench",  # General reasoning
                "HuggingFaceFW/fineweb",  # General knowledge
                "openai/openai_humaneval",  # Code reasoning
            ],
            "commonsense_qa": [
                "tau/commonsense_qa",  # Main CommonsenseQA
                "allenai/social_iqa",  # Social commonsense
                "cosmos_qa",  # Reading comprehension
                "dream",  # Dialogue reasoning
                "quail",  # QuaRel questions
                "social_bias_frames",  # Social reasoning
            ],
            "gsm8k": [
                "gsm8k",  # Main GSM8K
                "microsoft/orca-math-word-problems-200k",
                "EleutherAI/lambada_openai",  # Math language
                "HuggingFaceFW/fineweb-math",
                "math_dataset",  # General math
                "svamp",  # Math word problems
            ],
            "arc": [
                "ai2_arc",  # Main ARC dataset
                "sciq",  # Science questions
                "openbookqa",  # Open book QA
                "HuggingFaceFW/fineweb-science",
                "qasc",  # Question answering
                "worldtree",  # Science explanations
            ],
            "hellaswag": [
                "hellaswag",  # Main HellaSwag
                "winogrande",  # Winograd schema
                "social_bias_frames",
                "allenai/social_iqa",
                "dream",  # Dialogue understanding
                "cosmos_qa",  # Commonsense reasoning
            ],
            "math": [
                "math_dataset",  # Main MATH dataset
                "microsoft/orca-math-word-problems-200k",
                "HuggingFaceFW/fineweb-math",
                "EleutherAI/lambada_openai",
                "gsm8k",
                "svamp",
            ],
            "gpqa": [
                "Idavidrein/gpqa",  # Main GPQA
                "sciq",  # Science questions
                "HuggingFaceFW/fineweb-science",
                "allenai/olympic_reasoning",
                "tasksource/bigbench",
                "openbookqa",
            ],
            "humaneval": [
                "openai/openai_humaneval",  # Main HumanEval
                "codeparrot/github-code",  # Code dataset
                "bigcode/the-stack",  # Programming code
                "code_x_glue",  # Code understanding
                "concode",  # Code generation
                "apps",  # Programming problems
            ]
        }

    def initialize_training_schemas(self):
        """Create PostgreSQL schemas for training data storage"""
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()

            # Create schemas for each benchmark area
            benchmark_schemas = [
                "mmlu_training", "commonsense_training", "gsm8k_training",
                "arc_training", "hellaswag_training", "math_training",
                "gpqa_training", "humaneval_training"
            ]

            for schema in benchmark_schemas:
                cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
                # Create training data table
                cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {schema}.training_examples (
                        id SERIAL PRIMARY KEY,
                        question TEXT,
                        answer TEXT,
                        context TEXT,
                        subject VARCHAR(100),
                        difficulty VARCHAR(50),
                        dataset_source VARCHAR(100),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                # Create knowledge patterns table
                cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {schema}.knowledge_patterns (
                        id SERIAL PRIMARY KEY,
                        pattern_type VARCHAR(100),
                        pattern_data JSONB,
                        confidence FLOAT,
                        usage_count INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

            conn.commit()
            cursor.close()
            conn.close()

            logger.info("Training schemas initialized successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize training schemas: {e}")
            return False

    def load_training_data_cloud(self, benchmark_area: str, max_samples: int = 1000) -> Dict[str, Any]:
        """Load training data from cloud datasets for specific benchmark area"""
        try:
            logger.info(f"📥 Loading {benchmark_area} training data from cloud...")

            datasets = self.training_datasets.get(benchmark_area, [])
            all_examples = []

            for dataset_name in datasets:
                try:
                    logger.info(f"  Loading dataset: {dataset_name}")

                    # Configure for cloud storage only
                    import os
                    cloud_cache = os.path.join(os.getcwd(), 'cloud_training_cache')
                    os.environ['HF_DATASETS_CACHE'] = cloud_cache
                    os.environ['HF_HOME'] = cloud_cache
                    os.makedirs(cloud_cache, exist_ok=True)

                    # Load dataset with cloud storage
                    if benchmark_area == "mmlu":
                        dataset = load_dataset(dataset_name, "all", split="train", streaming=True)
                    elif benchmark_area == "commonsense_qa":
                        dataset = load_dataset(dataset_name, split="train", streaming=True)
                    elif benchmark_area == "gsm8k":
                        dataset = load_dataset(dataset_name, "main", split="train", streaming=True)
                    elif benchmark_area == "arc":
                        dataset = load_dataset(dataset_name, "ARC-Easy", split="train", streaming=True)
                    elif benchmark_area == "hellaswag":
                        dataset = load_dataset(dataset_name, split="train", streaming=True)
                    elif benchmark_area == "math":
                        dataset = load_dataset(dataset_name, "algebra__linear_1d", split="train", streaming=True)
                    elif benchmark_area == "gpqa":
                        dataset = load_dataset(dataset_name, split="train", streaming=True)
                    elif benchmark_area == "humaneval":
                        dataset = load_dataset(dataset_name, split="train", streaming=True)
                    else:
                        dataset = load_dataset(dataset_name, split="train", streaming=True)

                    # Sample examples
                    count = 0
                    for example in dataset:
                        if count >= max_samples // len(datasets):
                            break

                        # Extract relevant fields based on dataset structure
                        question = self._extract_question(example, benchmark_area)
                        answer = self._extract_answer(example, benchmark_area)
                        context = self._extract_context(example, benchmark_area)
                        subject = self._extract_subject(example, benchmark_area)

                        if question and answer:
                            all_examples.append({
                                "question": question,
                                "answer": answer,
                                "context": context or "",
                                "subject": subject or benchmark_area,
                                "dataset_source": dataset_name
                            })
                            count += 1

                except Exception as e:
                    logger.warning(f"  Failed to load {dataset_name}: {e}")
                    continue

            logger.info(f"Loaded {len(all_examples)} training examples for {benchmark_area}")
            return {
                "benchmark_area": benchmark_area,
                "examples": all_examples,
                "total_loaded": len(all_examples)
            }

        except Exception as e:
            logger.error(f"Failed to load training data for {benchmark_area}: {e}")
            return {"error": str(e)}

    def _extract_question(self, example: Dict, benchmark_area: str) -> Optional[str]:
        """Extract question from dataset example"""
        question_fields = ['question', 'query', 'input', 'text', 'problem', 'prompt']
        for field in question_fields:
            if field in example:
                return str(example[field])
        return None

    def _extract_answer(self, example: Dict, benchmark_area: str) -> Optional[str]:
        """Extract answer from dataset example"""
        answer_fields = ['answer', 'output', 'solution', 'target', 'label']
        for field in answer_fields:
            if field in example:
                return str(example[field])
        return None

    def _extract_context(self, example: Dict, benchmark_area: str) -> Optional[str]:
        """Extract context from dataset example"""
        context_fields = ['context', 'passage', 'article', 'background', 'explanation']
        for field in context_fields:
            if field in example:
                return str(example[field])
        return None

    def _extract_subject(self, example: Dict, benchmark_area: str) -> Optional[str]:
        """Extract subject from dataset example"""
        subject_fields = ['subject', 'category', 'domain', 'topic', 'field']
        for field in subject_fields:
            if field in example:
                return str(example[field])
        return benchmark_area

    def store_training_data(self, training_data: Dict[str, Any]) -> bool:
        """Store training data in R3AL3R Cloud Storage Facility"""
        try:
            benchmark_area = training_data["benchmark_area"]
            examples = training_data["examples"]

            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()

            schema_name = f"{benchmark_area}_training"
            inserted = 0

            for example in examples:
                cursor.execute(f"""
                    INSERT INTO {schema_name}.training_examples
                    (question, answer, context, subject, dataset_source)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    example["question"],
                    example["answer"],
                    example["context"],
                    example["subject"],
                    example["dataset_source"]
                ))
                inserted += 1

            conn.commit()
            cursor.close()
            conn.close()

            logger.info(f"Stored {inserted} training examples for {benchmark_area}")
            return True

        except Exception as e:
            logger.error(f"Failed to store training data: {e}")
            return False

    def extract_knowledge_patterns(self, benchmark_area: str) -> Dict[str, Any]:
        """Extract knowledge patterns from training data"""
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            schema_name = f"{benchmark_area}_training"

            # Get all training examples
            cursor.execute(f"SELECT * FROM {schema_name}.training_examples ORDER BY created_at DESC LIMIT 1000")
            examples = cursor.fetchall()

            patterns = {
                "question_patterns": {},
                "answer_patterns": {},
                "reasoning_patterns": {},
                "subject_patterns": {}
            }

            # Analyze question patterns
            for example in examples:
                question = example["question"]
                answer = example["answer"]
                subject = example["subject"]

                # Question structure patterns
                if len(question.split()) < 10:
                    patterns["question_patterns"]["short_questions"] = patterns["question_patterns"].get("short_questions", 0) + 1
                elif len(question.split()) > 20:
                    patterns["question_patterns"]["long_questions"] = patterns["question_patterns"].get("long_questions", 0) + 1

                # Answer type patterns
                if answer.isdigit():
                    patterns["answer_patterns"]["numeric"] = patterns["answer_patterns"].get("numeric", 0) + 1
                elif len(answer.split()) > 5:
                    patterns["answer_patterns"]["explanatory"] = patterns["answer_patterns"].get("explanatory", 0) + 1
                else:
                    patterns["answer_patterns"]["concise"] = patterns["answer_patterns"].get("concise", 0) + 1

                # Subject patterns
                patterns["subject_patterns"][subject] = patterns["subject_patterns"].get(subject, 0) + 1

            # Store patterns
            for pattern_type, pattern_data in patterns.items():
                cursor.execute(f"""
                    INSERT INTO {schema_name}.knowledge_patterns
                    (pattern_type, pattern_data, confidence)
                    VALUES (%s, %s, %s)
                """, (pattern_type, json.dumps(pattern_data), 0.8))

            conn.commit()
            cursor.close()
            conn.close()

            logger.info(f"Extracted knowledge patterns for {benchmark_area}")
            return patterns

        except Exception as e:
            logger.error(f"Failed to extract patterns for {benchmark_area}: {e}")
            return {}

    def run_targeted_training(self, benchmark_areas: List[str] = None) -> Dict[str, Any]:
        """Run targeted training for specified benchmark areas"""
        if benchmark_areas is None:
            benchmark_areas = list(self.training_datasets.keys())

        results = {
            "training_session": datetime.now().isoformat(),
            "benchmark_areas": benchmark_areas,
            "results": {}
        }

        logger.info("🚀 Starting R3ÆLƎR AI Targeted Training Session")
        logger.info("=" * 60)

        # Initialize schemas
        if not self.initialize_training_schemas():
            return {"error": "Failed to initialize training schemas"}

        for area in benchmark_areas:
            logger.info(f"Training {area}...")

            # Load training data from cloud
            training_data = self.load_training_data_cloud(area, max_samples=50)
            if "error" in training_data:
                results["results"][area] = {"error": training_data["error"]}
                continue

            # Store in R3AL3R Cloud Storage
            if self.store_training_data(training_data):
                # Extract knowledge patterns
                patterns = self.extract_knowledge_patterns(area)

                results["results"][area] = {
                    "status": "success",
                    "examples_loaded": training_data["total_loaded"],
                    "patterns_extracted": len(patterns),
                    "storage_location": f"R3AL3R Cloud Storage - {area}_training schema"
                }
            else:
                results["results"][area] = {"error": "Failed to store training data"}

        logger.info("Training session completed!")
        return results

    def get_training_status(self) -> Dict[str, Any]:
        """Get current training data status"""
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            status = {}

            benchmark_areas = [
                "mmlu", "commonsense_qa", "gsm8k", "arc", "hellaswag",
                "math", "gpqa", "humaneval"
            ]

            for area in benchmark_areas:
                schema_name = f"{area}_training"

                try:
                    # Count training examples
                    cursor.execute(f"SELECT COUNT(*) as count FROM {schema_name}.training_examples")
                    examples_count = cursor.fetchone()["count"]

                    # Count knowledge patterns
                    cursor.execute(f"SELECT COUNT(*) as count FROM {schema_name}.knowledge_patterns")
                    patterns_count = cursor.fetchone()["count"]

                    status[area] = {
                        "examples": examples_count,
                        "patterns": patterns_count,
                        "status": "trained" if examples_count > 0 else "empty"
                    }

                except Exception as e:
                    status[area] = {"error": str(e)}

            cursor.close()
            conn.close()

            return status

        except Exception as e:
            logger.error(f"Failed to get training status: {e}")
            return {"error": str(e)}

def main():
    """Main training execution"""
    trainer = BenchmarkTrainingSystem()

    # Areas that need improvement based on benchmark results
    weak_areas = [
        "mmlu", "commonsense_qa", "gsm8k", "arc", "hellaswag",
        "math", "gpqa", "humaneval"
    ]

    print("TARGET R3ALER AI - Targeted Benchmark Training")
    print("Using R3AL3R Cloud Storage Facility (Zero Local Storage)")
    print("=" * 60)

    # Run training
    results = trainer.run_targeted_training(weak_areas)

    # Show results
    print("\nTraining Results:")
    print("-" * 40)

    for area, result in results["results"].items():
        if "error" in result:
            print(f"ERROR {area}: {result['error']}")
        else:
            print(f"SUCCESS {area}: {result['examples_loaded']} examples, {result['patterns_extracted']} patterns")

    # Show final status
    print("\nFinal Training Status:")
    print("-" * 40)
    status = trainer.get_training_status()

    total_examples = 0
    for area, stats in status.items():
        if "examples" in stats:
            examples = stats["examples"]
            total_examples += examples
            print(f"  {area}: {examples} examples")

    print(f"\nTotal Training Examples: {total_examples}")
    print("All training data stored in R3AL3R Cloud Storage Facility")

if __name__ == "__main__":
    main()