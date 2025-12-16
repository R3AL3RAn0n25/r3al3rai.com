"""
Code Expertise Integration Module for R3ÆLƎR AI
Integrates Google CodeXGLUE datasets for enhanced coding capabilities

Datasets Integrated:
1. code_x_glue_cc_clone_detection_big_clone_bench (1.73M examples)
2. code_x_glue_cc_cloze_testing_all (176k examples)
3. code_x_glue_cc_code_completion_line (13k examples)
4. code_x_glue_cc_clone_detection_poj104 (53k examples)
5. code_x_glue_cc_cloze_testing_maxmin (2.62k examples)

License: Computational Use of Data Agreement (C-UDA)
"""

import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from datasets import load_dataset
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CodeExpertiseIntegration:
    """
    Provides coding expertise enhancement through Google CodeXGLUE datasets
    """

    def __init__(self):
        self.datasets_config = {
            # Priority 1: Clone Detection (BigCloneBench) - 1.73M examples
            "clone_detection_big": {
                "name": "google/code_x_glue_cc_clone_detection_big_clone_bench",
                "priority": 1,
                "max_rows": 5000,
                "cache_duration": timedelta(hours=1),
                "description": "Large-scale code clone detection dataset",
                "use_case": "Detect similar code patterns, refactoring suggestions",
                "fields": ["func1", "func2", "label"]
            },
            
            # Priority 2: Code Completion (Line-level) - 13k examples
            "code_completion_line": {
                "name": "google/code_x_glue_cc_code_completion_line",
                "priority": 2,
                "max_rows": 3000,
                "cache_duration": timedelta(hours=1),
                "description": "Line-level code completion dataset",
                "use_case": "Complete unfinished code lines",
                "fields": ["input", "gt"]  # ground truth
            },
            
            # Priority 3: Cloze Testing (All) - 176k examples
            "cloze_testing_all": {
                "name": "google/code_x_glue_cc_cloze_testing_all",
                "priority": 3,
                "max_rows": 2000,
                "cache_duration": timedelta(hours=1),
                "description": "Fill-in-the-blank code testing dataset",
                "use_case": "Code understanding, context-aware completion",
                "fields": ["code", "mask", "target"]
            },
            
            # Priority 4: Clone Detection (POJ-104) - 53k examples
            "clone_detection_poj": {
                "name": "google/code_x_glue_cc_clone_detection_poj104",
                "priority": 4,
                "max_rows": 2000,
                "cache_duration": timedelta(hours=1),
                "description": "Programming problems clone detection",
                "use_case": "Algorithm similarity detection",
                "fields": ["code", "label"]
            },
            
            # Priority 5: Cloze Testing (MaxMin) - 2.62k examples
            "cloze_testing_maxmin": {
                "name": "google/code_x_glue_cc_cloze_testing_maxmin",
                "priority": 5,
                "max_rows": 1000,
                "cache_duration": timedelta(hours=1),
                "description": "Max/min function cloze testing",
                "use_case": "Algorithm pattern understanding",
                "fields": ["code", "mask", "target"]
            }
        }
        
        self.cache = {}
        self.cache_timestamps = {}
        
        logger.info("Code Expertise Integration initialized with 5 CodeXGLUE datasets")

    def fetch_code_examples(
        self,
        dataset_key: str,
        offset: int = 0,
        limit: int = 100,
        language: str = None
    ) -> List[Dict]:
        """
        Fetch code examples from specified CodeXGLUE dataset
        
        Args:
            dataset_key: Key from datasets_config
            offset: Starting index
            limit: Number of examples to fetch
            language: Programming language filter (java, python, etc.)
        
        Returns:
            List of code examples with metadata
        """
        try:
            if dataset_key not in self.datasets_config:
                logger.error(f"Unknown dataset key: {dataset_key}")
                return []
            
            config = self.datasets_config[dataset_key]
            cache_key = f"{dataset_key}_{offset}_{limit}_{language}"
            
            # Check cache
            if cache_key in self.cache:
                timestamp = self.cache_timestamps.get(cache_key)
                if timestamp and datetime.now() - timestamp < config["cache_duration"]:
                    logger.info(f"Returning cached results for {dataset_key}")
                    return self.cache[cache_key]
            
            # Load dataset
            logger.info(f"Loading dataset: {config['name']}")
            
            # Some datasets have language-specific configurations
            if language and dataset_key in ["code_completion_line", "cloze_testing_all"]:
                dataset = load_dataset(config["name"], language)
            else:
                dataset = load_dataset(config["name"])
            
            # Get train split
            train_data = dataset["train"]
            
            # Apply offset and limit
            end_idx = min(offset + limit, len(train_data), config["max_rows"])
            examples = []
            
            for idx in range(offset, end_idx):
                example = train_data[idx]
                examples.append({
                    "dataset": dataset_key,
                    "index": idx,
                    "data": example,
                    "priority": config["priority"]
                })
            
            # Cache results
            self.cache[cache_key] = examples
            self.cache_timestamps[cache_key] = datetime.now()
            
            logger.info(f"Fetched {len(examples)} examples from {dataset_key}")
            return examples
            
        except Exception as e:
            logger.error(f"Error fetching code examples from {dataset_key}: {str(e)}")
            return []

    def get_completion_candidates(
        self,
        code_context: str,
        num_candidates: int = 5,
        language: str = "java"
    ) -> List[Dict]:
        """
        Get code completion candidates for given context
        
        Args:
            code_context: Incomplete code requiring completion
            num_candidates: Number of completion suggestions
            language: Programming language
        
        Returns:
            List of completion candidates with confidence scores
        """
        try:
            # Fetch completion examples
            examples = self.fetch_code_examples(
                "code_completion_line",
                limit=500,
                language=language
            )
            
            if not examples:
                return []
            
            # Find relevant completions based on context similarity
            candidates = []
            for example in examples:
                data = example["data"]
                input_code = data.get("input", "")
                completion = data.get("gt", "")
                
                # Calculate similarity (simple keyword matching)
                similarity = self._calculate_code_similarity(code_context, input_code)
                
                if similarity > 0.3:  # Threshold
                    candidates.append({
                        "context": input_code,
                        "completion": completion,
                        "similarity": similarity,
                        "language": language
                    })
            
            # Sort by similarity and return top N
            candidates.sort(key=lambda x: x["similarity"], reverse=True)
            return candidates[:num_candidates]
            
        except Exception as e:
            logger.error(f"Error getting completion candidates: {str(e)}")
            return []

    def detect_code_clones(
        self,
        code_snippet: str,
        num_matches: int = 5
    ) -> List[Dict]:
        """
        Detect similar code snippets (clones) from BigCloneBench
        
        Args:
            code_snippet: Code to find clones for
            num_matches: Number of similar code matches to return
        
        Returns:
            List of similar code snippets with similarity scores
        """
        try:
            # Fetch clone detection examples
            examples = self.fetch_code_examples(
                "clone_detection_big",
                limit=1000
            )
            
            if not examples:
                return []
            
            matches = []
            for example in examples:
                data = example["data"]
                func1 = data.get("func1", "")
                func2 = data.get("func2", "")
                is_clone = data.get("label", False)
                
                # Check similarity with both functions
                sim1 = self._calculate_code_similarity(code_snippet, func1)
                sim2 = self._calculate_code_similarity(code_snippet, func2)
                
                if sim1 > 0.4:
                    matches.append({
                        "code": func1,
                        "similarity": sim1,
                        "is_verified_clone": is_clone,
                        "paired_with": func2
                    })
                
                if sim2 > 0.4:
                    matches.append({
                        "code": func2,
                        "similarity": sim2,
                        "is_verified_clone": is_clone,
                        "paired_with": func1
                    })
            
            # Sort by similarity and deduplicate
            matches.sort(key=lambda x: x["similarity"], reverse=True)
            unique_matches = []
            seen_codes = set()
            
            for match in matches:
                code_hash = hash(match["code"][:100])  # Hash first 100 chars
                if code_hash not in seen_codes:
                    unique_matches.append(match)
                    seen_codes.add(code_hash)
                
                if len(unique_matches) >= num_matches:
                    break
            
            return unique_matches
            
        except Exception as e:
            logger.error(f"Error detecting code clones: {str(e)}")
            return []

    def build_code_context(
        self,
        query: str,
        num_examples: int = 3,
        language: str = None
    ) -> str:
        """
        Build code context from relevant examples for enhanced code generation
        
        Args:
            query: User's code-related query
            num_examples: Number of examples to include
            language: Programming language preference
        
        Returns:
            Formatted context string with code examples
        """
        try:
            # Analyze query to determine which datasets to use
            query_lower = query.lower()
            datasets_to_use = []
            
            if any(kw in query_lower for kw in ["complete", "finish", "continue"]):
                datasets_to_use.append("code_completion_line")
            
            if any(kw in query_lower for kw in ["similar", "clone", "duplicate", "refactor"]):
                datasets_to_use.append("clone_detection_big")
            
            if any(kw in query_lower for kw in ["understand", "explain", "what does"]):
                datasets_to_use.append("cloze_testing_all")
            
            # Default: use code completion
            if not datasets_to_use:
                datasets_to_use.append("code_completion_line")
            
            # Detect language from query
            if not language:
                if "java" in query_lower:
                    language = "java"
                elif "python" in query_lower:
                    language = "python"
                else:
                    language = "java"  # Default
            
            # Fetch examples from relevant datasets
            all_examples = []
            for dataset_key in datasets_to_use:
                examples = self.fetch_code_examples(
                    dataset_key,
                    limit=100,
                    language=language if dataset_key == "code_completion_line" else None
                )
                all_examples.extend(examples)
            
            if not all_examples:
                return ""
            
            # Filter by relevance
            relevant_examples = self._filter_examples_by_relevance(query, all_examples)
            
            # Build context string
            context_parts = []
            context_parts.append(f"### Code Examples ({language.upper()}):\n")
            
            for idx, example in enumerate(relevant_examples[:num_examples], 1):
                data = example["data"]
                dataset = example["dataset"]
                
                context_parts.append(f"\n**Example {idx}** (from {dataset}):")
                
                if dataset == "code_completion_line":
                    input_code = data.get("input", "")
                    completion = data.get("gt", "")
                    context_parts.append(f"```{language}\n{input_code}\n// Completion:\n{completion}\n```")
                
                elif dataset == "clone_detection_big":
                    func1 = data.get("func1", "")[:500]  # Limit length
                    context_parts.append(f"```{language}\n{func1}\n```")
                
                elif dataset == "cloze_testing_all":
                    code = data.get("code", "")[:500]
                    context_parts.append(f"```{language}\n{code}\n```")
            
            return "\n".join(context_parts)
            
        except Exception as e:
            logger.error(f"Error building code context: {str(e)}")
            return ""

    def _calculate_code_similarity(self, code1: str, code2: str) -> float:
        """
        Calculate similarity between two code snippets
        Simple keyword-based approach
        
        Args:
            code1: First code snippet
            code2: Second code snippet
        
        Returns:
            Similarity score (0.0 to 1.0)
        """
        # Extract keywords (identifiers, keywords)
        keywords1 = set(re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', code1.lower()))
        keywords2 = set(re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', code2.lower()))
        
        if not keywords1 or not keywords2:
            return 0.0
        
        # Jaccard similarity
        intersection = keywords1.intersection(keywords2)
        union = keywords1.union(keywords2)
        
        return len(intersection) / len(union) if union else 0.0

    def _filter_examples_by_relevance(
        self,
        query: str,
        examples: List[Dict]
    ) -> List[Dict]:
        """
        Filter code examples by relevance to query
        
        Args:
            query: User query
            examples: List of code examples
        
        Returns:
            Filtered and sorted examples
        """
        query_keywords = set(re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', query.lower()))
        
        scored_examples = []
        for example in examples:
            data = example["data"]
            
            # Extract code text from various fields
            code_text = ""
            for field in ["input", "func1", "code", "gt"]:
                if field in data:
                    code_text += str(data[field]) + " "
            
            # Calculate relevance score
            code_keywords = set(re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', code_text.lower()))
            relevance = len(query_keywords.intersection(code_keywords)) / max(len(query_keywords), 1)
            
            scored_examples.append({
                "example": example,
                "relevance": relevance
            })
        
        # Sort by relevance
        scored_examples.sort(key=lambda x: x["relevance"], reverse=True)
        
        return [item["example"] for item in scored_examples if item["relevance"] > 0.1]

    def get_dataset_stats(self) -> Dict:
        """
        Get statistics about loaded datasets
        
        Returns:
            Dictionary with dataset statistics
        """
        stats = {
            "total_datasets": len(self.datasets_config),
            "cache_size": len(self.cache),
            "datasets": {}
        }
        
        for key, config in self.datasets_config.items():
            stats["datasets"][key] = {
                "name": config["name"],
                "priority": config["priority"],
                "max_rows": config["max_rows"],
                "description": config["description"],
                "use_case": config["use_case"]
            }
        
        return stats


# Example usage
if __name__ == "__main__":
    code_exp = CodeExpertiseIntegration()
    
    # Test code completion
    context = "public void copyFile(File src, File dest) throws IOException {"
    candidates = code_exp.get_completion_candidates(context, num_candidates=3)
    print(f"\n=== Code Completion Candidates ({len(candidates)}) ===")
    for idx, candidate in enumerate(candidates, 1):
        print(f"\n{idx}. Similarity: {candidate['similarity']:.2f}")
        print(f"Completion: {candidate['completion'][:100]}...")
    
    # Test clone detection
    test_code = "public static void copyFile(File in, File out) throws IOException"
    clones = code_exp.detect_code_clones(test_code, num_matches=3)
    print(f"\n=== Similar Code Snippets ({len(clones)}) ===")
    for idx, clone in enumerate(clones, 1):
        print(f"\n{idx}. Similarity: {clone['similarity']:.2f}")
        print(f"Code: {clone['code'][:100]}...")
    
    # Test context building
    query = "How to copy a file in Java?"
    context = code_exp.build_code_context(query, num_examples=2, language="java")
    print(f"\n=== Code Context for Query ===")
    print(context[:500] + "...")
    
    # Get stats
    stats = code_exp.get_dataset_stats()
    print(f"\n=== Dataset Statistics ===")
    print(f"Total datasets: {stats['total_datasets']}")
    print(f"Cache size: {stats['cache_size']}")
