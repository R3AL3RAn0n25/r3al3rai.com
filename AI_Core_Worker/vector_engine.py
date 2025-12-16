#!/usr/bin/env python3
"""
R3ÆLƎR AI: Vector Engine using pgvector + hybrid scoring
Fully backward compatible — falls back to full-text if no embedding
"""

import os
import logging
import numpy as np
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any, Optional
import openai  # You already use external APIs — this is the only new import

logger = logging.getLogger(__name__)

# OpenAI config (use your existing key or local proxy)
openai.api_key = os.getenv("OPENAI_API_KEY", "sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'r3aeler_ai',
    'user': 'r3aler_user_2025',
    'password': 'R3AL3RAdmin816'
}

class VectorEngine:
    EMBEDDING_MODEL = "text-embedding-3-small"  # 1536 dims, $0.02 per 1M tokens
    BATCH_SIZE = 50
    HYBRID_WEIGHT_VECTOR = 0.7   # 70% vector, 30% keyword
    HYBRID_WEIGHT_KEYWORD = 0.3

    @staticmethod
    def get_connection():
        return psycopg2.connect(**DB_CONFIG)

    @staticmethod
    def generate_embedding(text: str) -> Optional[List[float]]:
        """Generate embedding via OpenAI (cached in DB later)"""
        try:
            if not text.strip():
                return None
            response = openai.embeddings.create(
                input=text.strip()[:8000],  # truncate very long entries
                model=VectorEngine.EMBEDDING_MODEL
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Embedding failed: {e}")
            return None

    @staticmethod
    def embed_knowledge_unit(unit_name: str, table_name: str = "knowledge"):
        """One-time or incremental: embed all entries in a unit"""
        conn = VectorEngine.get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get entries without embeddings
        cur.execute(f"""
            SELECT id, content FROM {unit_name}.{table_name}
            WHERE embedding IS NULL OR embedding = '[0]'::vector
            LIMIT %s
        """, (VectorEngine.BATCH_SIZE,))
        
        rows = cur.fetchall()
        if not rows:
            logger.info(f"{unit_name}: All entries already embedded")
            conn.close()
            return

        for row in rows:
            text = f"{row.get('title', '')} {row['content']}".strip()
            embedding = VectorEngine.generate_embedding(text)
            if embedding:
                cur.execute(f"""
                    UPDATE {unit_name}.{table_name}
                    SET embedding = %s
                    WHERE id = %s
                """, (embedding, row['id']))
                logger.info(f"Embedded {unit_name}.id={row['id']}")
        
        conn.commit()
        conn.close()

    @staticmethod
    def hybrid_search(query: str, unit_name: str, limit: int = 5, table: str = "knowledge") -> List[Dict]:
        """Main hybrid search: vector + full-text with reciprocal rank fusion"""
        query_embedding = VectorEngine.generate_embedding(query)
        if not query_embedding:
            # Fall back to pure full-text
            return VectorEngine.fulltext_search(query, unit_name, limit, table)

        conn = VectorEngine.get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        sql = f"""
            WITH vector_results AS (
                SELECT 
                    id, content, title,
                    embedding <=> %s AS vector_distance,
                    ROW_NUMBER() OVER (ORDER BY embedding <=> %s) AS vector_rank
                FROM {unit_name}.{table}
                WHERE embedding IS NOT NULL
                ORDER BY embedding <=> %s
                LIMIT %s
            ),
            keyword_results AS (
                SELECT 
                    id, content, title,
                    ts_rank_cd(to_tsvector('english', content || ' ' || COALESCE(title,'')), 
                               plainto_tsquery('english', %s)) AS keyword_score,
                    ROW_NUMBER() OVER (ORDER BY ts_rank_cd(to_tsvector('english', content || ' ' || COALESCE(title,'')), 
                                                          plainto_tsquery('english', %s)) DESC) AS keyword_rank
                FROM {unit_name}.{table}
                WHERE to_tsvector('english', content || ' ' || COALESCE(title,'')) @@ plainto_tsquery('english', %s)
                ORDER BY keyword_score DESC
                LIMIT %s
            ),
            combined AS (
                SELECT 
                    COALESCE(v.id, k.id) AS id,
                    COALESCE(v.content, k.content) AS content,
                    COALESCE(v.title, k.title) AS title,
                    v.vector_rank, k.keyword_rank
                FROM vector_results v
                FULL OUTER JOIN keyword_results k ON v.id = k.id
            )
            SELECT 
                id, title, content,
                COALESCE(1.0 / (60 + vector_rank), 0) * %s +
                COALESCE(1.0 / (60 + keyword_rank), 0) * %s AS hybrid_score
            FROM combined
            ORDER BY hybrid_score DESC
            LIMIT %s;
        """
        
        cur.execute(sql, (
            query_embedding, query_embedding, query_embedding, limit*3,
            query, query, query, limit*3,
            VectorEngine.HYBRID_WEIGHT_VECTOR,
            VectorEngine.HYBRID_WEIGHT_KEYWORD,
            limit
        ))
        
        results = [dict(row) for row in cur.fetchall()]
        conn.close()
        return results

    @staticmethod
    def fulltext_search(query: str, unit_name: str, limit: int = 5, table: str = "knowledge"):
        """Your original full-text search — kept as fallback"""
        conn = VectorEngine.get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(f"""
            SELECT id, title, content
            FROM {unit_name}.{table}
            WHERE to_tsvector('english', content || ' ' || COALESCE(title,'')) @@ plainto_tsquery('english', %s)
            ORDER BY ts_rank_cd(to_tsvector('english', content || ' ' || COALESCE(title,'')), plainto_tsquery('english', %s)) DESC
            LIMIT %s
        """, (query, query, limit))
        results = [dict(row) for row in cur.fetchall()]
        conn.close()
        return results

    @staticmethod
    def embed_all_units():
        """Run this once (or on a cron) to embed everything"""
        units = [
            ("physics_unit", "knowledge"),
            ("quantum_unit", "knowledge"),
            ("space_unit", "knowledge"),
            ("crypto_unit", "knowledge"),
            ("blackarch_unit", "tools")
        ]
        for unit, table in units:
            logger.info(f"Embedding {unit}...")
            VectorEngine.embed_knowledge_unit(unit, table)