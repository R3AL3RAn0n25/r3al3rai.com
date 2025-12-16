#!/usr/bin/env python3
"""
R3ALER AI Cryptocurrency Knowledge Query Tool
PgAdmin integration for feeding crypto knowledge to R3AL3R AI
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any
import json

class CryptoKnowledgeQueryTool:
    """Query tool for cryptocurrency knowledge in R3ALER Storage Facility"""
    
    def __init__(self, db_config: Dict = None):
        self.db_config = db_config or {
            'host': 'localhost',
            'port': 5432,
            'database': 'r3aler_ai',
            'user': 'r3aler_user_2025',
            'password': 'password123'
        }
    
    def get_connection(self):
        return psycopg2.connect(**self.db_config)
    
    def search_knowledge(self, query: str, limit: int = 10) -> List[Dict]:
        """Full-text search cryptocurrency knowledge"""
        conn = self.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cursor.execute("""
                SELECT 
                    entry_id,
                    topic,
                    content,
                    category,
                    subcategory,
                    source,
                    ts_rank(
                        to_tsvector('english', COALESCE(content, '') || ' ' || COALESCE(topic, '')),
                        plainto_tsquery('english', %s)
                    ) as relevance
                FROM crypto_unit.knowledge
                WHERE to_tsvector('english', COALESCE(content, '') || ' ' || COALESCE(topic, ''))
                      @@ plainto_tsquery('english', %s)
                ORDER BY relevance DESC
                LIMIT %s
            """, (query, query, limit))
            
            return [dict(row) for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()
    
    def get_by_category(self, category: str, limit: int = 20) -> List[Dict]:
        """Get knowledge by category"""
        conn = self.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cursor.execute("""
                SELECT entry_id, topic, content, category, subcategory, source
                FROM crypto_unit.knowledge
                WHERE category = %s
                LIMIT %s
            """, (category, limit))
            
            return [dict(row) for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()
    
    def get_all_categories(self) -> List[str]:
        """Get all available categories"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT DISTINCT category FROM crypto_unit.knowledge
                ORDER BY category
            """)
            
            return [row[0] for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()
    
    def get_knowledge_by_source(self, source_url: str) -> List[Dict]:
        """Get knowledge by source URL"""
        conn = self.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cursor.execute("""
                SELECT entry_id, topic, content, category, subcategory, source
                FROM crypto_unit.knowledge
                WHERE source = %s
            """, (source_url,))
            
            return [dict(row) for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get knowledge base statistics"""
        conn = self.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_entries,
                    COUNT(DISTINCT category) as total_categories,
                    COUNT(DISTINCT source) as total_sources,
                    pg_size_pretty(pg_total_relation_size('crypto_unit.knowledge')) as total_size
                FROM crypto_unit.knowledge
            """)
            
            return dict(cursor.fetchone())
        finally:
            cursor.close()
            conn.close()
    
    def feed_to_r3aler(self, query: str) -> Dict[str, Any]:
        """Feed cryptocurrency knowledge to R3AL3R AI"""
        results = self.search_knowledge(query, limit=20)
        
        if not results:
            return {
                'status': 'no_results',
                'query': query,
                'message': 'No cryptocurrency knowledge found for this query'
            }
        
        # Format for R3AL3R AI consumption
        knowledge_feed = {
            'status': 'success',
            'query': query,
            'total_results': len(results),
            'knowledge_entries': results,
            'categories_found': list(set([r['category'] for r in results])),
            'sources': list(set([r['source'] for r in results]))
        }
        
        return knowledge_feed

def interactive_mode():
    """Interactive query tool"""
    tool = CryptoKnowledgeQueryTool()
    
    print("\n" + "="*70)
    print("R3ALER AI - CRYPTOCURRENCY KNOWLEDGE QUERY TOOL")
    print("="*70)
    print("Commands:")
    print("  search <query>     - Search cryptocurrency knowledge")
    print("  category <name>    - Get knowledge by category")
    print("  categories         - List all categories")
    print("  stats              - Show knowledge base statistics")
    print("  feed <query>       - Feed knowledge to R3AL3R AI")
    print("  exit               - Exit tool")
    print("="*70 + "\n")
    
    while True:
        try:
            user_input = input("r3aler-crypto> ").strip()
            
            if not user_input:
                continue
            
            parts = user_input.split(' ', 1)
            command = parts[0].lower()
            arg = parts[1] if len(parts) > 1 else None
            
            if command == 'exit':
                print("Exiting...")
                break
            
            elif command == 'search':
                if not arg:
                    print("Usage: search <query>")
                    continue
                results = tool.search_knowledge(arg, limit=10)
                print(f"\nFound {len(results)} results:\n")
                for i, result in enumerate(results, 1):
                    print(f"{i}. {result['topic']} [{result['category']}]")
                    print(f"   Source: {result['source']}")
                    print(f"   Relevance: {result['relevance']:.2f}\n")
            
            elif command == 'category':
                if not arg:
                    print("Usage: category <name>")
                    continue
                results = tool.get_by_category(arg, limit=20)
                print(f"\nFound {len(results)} entries in category '{arg}':\n")
                for i, result in enumerate(results, 1):
                    print(f"{i}. {result['topic']}")
                    print(f"   Source: {result['source']}\n")
            
            elif command == 'categories':
                categories = tool.get_all_categories()
                print(f"\nAvailable categories ({len(categories)}):\n")
                for cat in categories:
                    print(f"  - {cat}")
                print()
            
            elif command == 'stats':
                stats = tool.get_stats()
                print("\nKnowledge Base Statistics:")
                for key, value in stats.items():
                    print(f"  {key}: {value}")
                print()
            
            elif command == 'feed':
                if not arg:
                    print("Usage: feed <query>")
                    continue
                feed = tool.feed_to_r3aler(arg)
                print("\nFeeding to R3AL3R AI:")
                print(json.dumps(feed, indent=2))
                print()
            
            else:
                print(f"Unknown command: {command}")
        
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

def pgadmin_query_commands():
    """Generate PgAdmin query commands"""
    commands = {
        'search_base58': """
            SELECT entry_id, topic, content, category, source
            FROM crypto_unit.knowledge
            WHERE to_tsvector('english', content || ' ' || topic) @@ plainto_tsquery('english', 'base58')
            ORDER BY ts_rank(to_tsvector('english', content || ' ' || topic), plainto_tsquery('english', 'base58')) DESC
            LIMIT 20;
        """,
        
        'search_bitcoin': """
            SELECT entry_id, topic, content, category, source
            FROM crypto_unit.knowledge
            WHERE to_tsvector('english', content || ' ' || topic) @@ plainto_tsquery('english', 'bitcoin')
            ORDER BY ts_rank(to_tsvector('english', content || ' ' || topic), plainto_tsquery('english', 'bitcoin')) DESC
            LIMIT 20;
        """,
        
        'search_cryptography': """
            SELECT entry_id, topic, content, category, source
            FROM crypto_unit.knowledge
            WHERE to_tsvector('english', content || ' ' || topic) @@ plainto_tsquery('english', 'cryptography')
            ORDER BY ts_rank(to_tsvector('english', content || ' ' || topic), plainto_tsquery('english', 'cryptography')) DESC
            LIMIT 20;
        """,
        
        'get_by_category': """
            SELECT entry_id, topic, content, category, source
            FROM crypto_unit.knowledge
            WHERE category = 'encoding'
            LIMIT 20;
        """,
        
        'all_categories': """
            SELECT DISTINCT category, COUNT(*) as count
            FROM crypto_unit.knowledge
            GROUP BY category
            ORDER BY count DESC;
        """,
        
        'knowledge_stats': """
            SELECT 
                COUNT(*) as total_entries,
                COUNT(DISTINCT category) as categories,
                COUNT(DISTINCT source) as sources,
                pg_size_pretty(pg_total_relation_size('crypto_unit.knowledge')) as size
            FROM crypto_unit.knowledge;
        """,
        
        'top_sources': """
            SELECT source, COUNT(*) as entry_count
            FROM crypto_unit.knowledge
            GROUP BY source
            ORDER BY entry_count DESC
            LIMIT 20;
        """
    }
    
    return commands

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'pgadmin':
        print("\n" + "="*70)
        print("PGADMIN QUERY COMMANDS FOR R3ALER AI")
        print("="*70 + "\n")
        
        commands = pgadmin_query_commands()
        for name, query in commands.items():
            print(f"-- {name}")
            print(query)
            print()
    else:
        interactive_mode()
