"""
HuggingFace Chat Response Dataset Integration
Integrates multiple chat/conversation datasets for improved R3ÆLƎR AI responses
"""

import requests
import logging
import json
import time
from typing import List, Dict, Optional
from datetime import datetime, timedelta

class ChatDatasetIntegration:
    """
    Integrates multiple HuggingFace chat response datasets
    
    Supported Datasets:
    1. OpenAssistant/oasst1 - High-quality human-AI conversations
    2. Hello-SimpleAI/HC3 - Human vs ChatGPT responses
    3. lmsys/chatbot_arena_conversations - Real user-chatbot interactions
    4. anthracite-org/kalo-opus-instruct-22k-no-refusal - Instruction following
    5. teknium/OpenHermes-2.5 - Multi-turn conversations
    """
    
    HF_DATASETS_API = "https://datasets-server.huggingface.co/rows"
    
    # Dataset configurations with their specific fields
    DATASETS = {
        "oasst1": {
            "name": "OpenAssistant/oasst1",
            "fields": ["text", "role"],
            "description": "High-quality human-AI conversations with ratings",
            "priority": 1,
            "max_rows": 500
        },
        "hc3": {
            "name": "Hello-SimpleAI/HC3",
            "fields": ["question", "human_answers", "chatgpt_answers"],
            "description": "Human vs ChatGPT response comparisons",
            "priority": 2,
            "max_rows": 300
        },
        "chatbot_arena": {
            "name": "lmsys/chatbot_arena_conversations",
            "fields": ["conversation_a", "conversation_b", "winner"],
            "description": "Real chatbot arena battles",
            "priority": 3,
            "max_rows": 200
        },
        "openhermes": {
            "name": "teknium/OpenHermes-2.5",
            "fields": ["conversations"],
            "description": "Multi-turn diverse conversations",
            "priority": 4,
            "max_rows": 400
        },
        "ultrachat": {
            "name": "HuggingFaceH4/ultrachat_200k",
            "fields": ["messages"],
            "description": "Large-scale multi-turn dialogues",
            "priority": 5,
            "max_rows": 300
        }
    }
    
    def __init__(self):
        self.cache = {}
        self.cache_ttl = 3600  # 1 hour
        self.last_fetch = {}
        
    def fetch_dataset(self, dataset_key: str, offset: int = 0, limit: int = 100) -> List[Dict]:
        """Fetch data from a specific HuggingFace dataset"""
        
        if dataset_key not in self.DATASETS:
            logging.error(f"Unknown dataset key: {dataset_key}")
            return []
        
        dataset_config = self.DATASETS[dataset_key]
        dataset_name = dataset_config["name"]
        
        # Check cache
        cache_key = f"{dataset_key}_{offset}_{limit}"
        if cache_key in self.cache:
            cache_time = self.last_fetch.get(cache_key, 0)
            if time.time() - cache_time < self.cache_ttl:
                logging.info(f"Using cached data for {dataset_name}")
                return self.cache[cache_key]
        
        try:
            params = {
                "dataset": dataset_name,
                "config": "default",
                "split": "train",
                "offset": offset,
                "length": min(limit, dataset_config["max_rows"])
            }
            
            logging.info(f"Fetching {limit} rows from {dataset_name}...")
            response = requests.get(self.HF_DATASETS_API, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            rows = []
            
            if "rows" in data:
                for row in data["rows"]:
                    row_data = row.get("row", {})
                    rows.append(row_data)
            
            # Cache the results
            self.cache[cache_key] = rows
            self.last_fetch[cache_key] = time.time()
            
            logging.info(f"Fetched {len(rows)} rows from {dataset_name}")
            return rows
            
        except Exception as e:
            logging.error(f"Failed to fetch {dataset_name}: {e}")
            return []
    
    def parse_oasst1_conversation(self, rows: List[Dict]) -> List[Dict]:
        """Parse OpenAssistant conversation format"""
        conversations = []
        
        for row in rows:
            if "text" in row and "role" in row:
                conversations.append({
                    "role": row["role"],
                    "content": row["text"],
                    "source": "OpenAssistant/oasst1",
                    "quality": "high"
                })
        
        return conversations
    
    def parse_hc3_responses(self, rows: List[Dict]) -> List[Dict]:
        """Parse HC3 human vs ChatGPT format"""
        conversations = []
        
        for row in rows:
            if "question" in row:
                question = row["question"]
                
                # Add human responses
                if "human_answers" in row:
                    human_answers = row["human_answers"]
                    if isinstance(human_answers, list):
                        for answer in human_answers[:2]:  # Limit to 2 best
                            conversations.append({
                                "role": "user",
                                "content": question,
                                "source": "HC3",
                                "quality": "high"
                            })
                            conversations.append({
                                "role": "assistant",
                                "content": answer,
                                "source": "HC3-Human",
                                "quality": "high"
                            })
                
                # Add ChatGPT responses
                if "chatgpt_answers" in row:
                    chatgpt_answers = row["chatgpt_answers"]
                    if isinstance(chatgpt_answers, list):
                        for answer in chatgpt_answers[:1]:  # Limit to 1
                            conversations.append({
                                "role": "user",
                                "content": question,
                                "source": "HC3",
                                "quality": "high"
                            })
                            conversations.append({
                                "role": "assistant",
                                "content": answer,
                                "source": "HC3-ChatGPT",
                                "quality": "high"
                            })
        
        return conversations
    
    def parse_openhermes_conversations(self, rows: List[Dict]) -> List[Dict]:
        """Parse OpenHermes multi-turn conversations"""
        conversations = []
        
        for row in rows:
            if "conversations" in row:
                convs = row["conversations"]
                if isinstance(convs, list):
                    for conv in convs:
                        if "from" in conv and "value" in conv:
                            role = "user" if conv["from"] in ["human", "user"] else "assistant"
                            conversations.append({
                                "role": role,
                                "content": conv["value"],
                                "source": "OpenHermes-2.5",
                                "quality": "medium"
                            })
        
        return conversations
    
    def parse_ultrachat_messages(self, rows: List[Dict]) -> List[Dict]:
        """Parse UltraChat message format"""
        conversations = []
        
        for row in rows:
            if "messages" in row:
                messages = row["messages"]
                if isinstance(messages, list):
                    for msg in messages:
                        if "role" in msg and "content" in msg:
                            conversations.append({
                                "role": msg["role"],
                                "content": msg["content"],
                                "source": "UltraChat",
                                "quality": "medium"
                            })
        
        return conversations
    
    def get_conversation_examples(self, context: Dict, max_examples: int = 5) -> List[Dict]:
        """
        Get relevant conversation examples based on context
        
        Args:
            context: Dict with 'domain', 'intent', 'keywords'
            max_examples: Maximum number of examples to return
            
        Returns:
            List of conversation examples
        """
        all_examples = []
        
        # Fetch from multiple datasets
        for dataset_key, config in sorted(self.DATASETS.items(), key=lambda x: x[1]["priority"]):
            try:
                rows = self.fetch_dataset(dataset_key, offset=0, limit=50)
                
                # Parse based on dataset type
                if dataset_key == "oasst1":
                    examples = self.parse_oasst1_conversation(rows)
                elif dataset_key == "hc3":
                    examples = self.parse_hc3_responses(rows)
                elif dataset_key == "openhermes":
                    examples = self.parse_openhermes_conversations(rows)
                elif dataset_key == "ultrachat":
                    examples = self.parse_ultrachat_messages(rows)
                else:
                    examples = []
                
                all_examples.extend(examples)
                
                # Stop if we have enough examples
                if len(all_examples) >= max_examples * 3:
                    break
                    
            except Exception as e:
                logging.error(f"Failed to process {dataset_key}: {e}")
                continue
        
        # Filter by relevance to context
        relevant_examples = self._filter_by_relevance(all_examples, context)
        
        # Return top examples
        return relevant_examples[:max_examples]
    
    def _filter_by_relevance(self, examples: List[Dict], context: Dict) -> List[Dict]:
        """Filter conversation examples by relevance to current context"""
        keywords = context.get("keywords", [])
        domain = context.get("domain", "general")
        
        if not keywords:
            return examples[:10]  # Return first 10 if no keywords
        
        # Score each example by keyword match
        scored_examples = []
        for example in examples:
            content = example.get("content", "").lower()
            score = 0
            
            # Keyword matching
            for keyword in keywords:
                if keyword.lower() in content:
                    score += 2
            
            # Domain matching
            domain_keywords = {
                "technology": ["code", "programming", "software", "app"],
                "cryptocurrency": ["bitcoin", "crypto", "blockchain", "wallet"],
                "forensics": ["forensic", "investigation", "analysis", "evidence"],
                "ai": ["ai", "machine learning", "neural", "model"]
            }
            
            if domain in domain_keywords:
                for dk in domain_keywords[domain]:
                    if dk in content:
                        score += 1
            
            # Quality bonus
            if example.get("quality") == "high":
                score += 1
            
            if score > 0:
                scored_examples.append((score, example))
        
        # Sort by score descending
        scored_examples.sort(key=lambda x: x[0], reverse=True)
        
        return [ex for score, ex in scored_examples]
    
    def build_few_shot_prompt(self, context: Dict, user_message: str, num_examples: int = 3) -> str:
        """
        Build a few-shot learning prompt with relevant examples
        
        Args:
            context: Context dictionary with domain, intent, keywords
            user_message: The current user message
            num_examples: Number of examples to include
            
        Returns:
            Enhanced prompt with examples
        """
        examples = self.get_conversation_examples(context, max_examples=num_examples)
        
        if not examples:
            return ""
        
        # Build few-shot prompt
        prompt_parts = ["\n### Conversation Examples from High-Quality Datasets:\n"]
        
        current_conversation = []
        for i, example in enumerate(examples, 1):
            role = example["role"]
            content = example["content"][:300]  # Limit length
            source = example.get("source", "Unknown")
            
            if role == "user":
                if current_conversation:
                    # Complete previous conversation
                    prompt_parts.append("\n")
                current_conversation = []
                prompt_parts.append(f"\nExample {len([p for p in prompt_parts if 'Example' in p])}:")
                prompt_parts.append(f"\nUser: {content}")
                current_conversation.append("user")
            elif role == "assistant":
                prompt_parts.append(f"\nAssistant: {content}")
                current_conversation.append("assistant")
            
            # Limit to num_examples complete conversations
            if len([p for p in prompt_parts if 'Example' in p]) >= num_examples:
                break
        
        prompt_parts.append("\n\n### Your Task:\n")
        prompt_parts.append(f"Now respond to the user's message in a similar helpful, accurate manner.\n")
        
        return "".join(prompt_parts)
    
    def get_dataset_stats(self) -> Dict:
        """Get statistics about loaded datasets"""
        stats = {
            "total_datasets": len(self.DATASETS),
            "cached_datasets": len(self.cache),
            "datasets": {}
        }
        
        for key, config in self.DATASETS.items():
            stats["datasets"][key] = {
                "name": config["name"],
                "description": config["description"],
                "priority": config["priority"],
                "cached": any(key in cache_key for cache_key in self.cache.keys())
            }
        
        return stats
