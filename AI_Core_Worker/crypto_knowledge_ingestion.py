#!/usr/bin/env python3
"""
R3ALER AI Cryptocurrency Knowledge Ingestion
Fetches crypto resources and stores in Enhanced Storage Facility (Crypto Unit)
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any, Optional
import json
import hashlib
from datetime import datetime
import requests

class CryptoKnowledgeIngestion:
    """Ingest cryptocurrency knowledge into R3ALER Storage Facility"""
    
    CRYPTO_RESOURCES = [
        "https://en.bitcoin.it/wiki/Wallet",
        "https://github.com/protocolbuffers/protobuf.git",
        "https://en.bitcoin.it/wiki/Base58Check_encoding",
        "https://en.bitcoin.it/wiki/Base58Check_encoding#Creating_a_Base58Check_string",
        "https://en.bitcoin.it/wiki/Base58Check_encoding#Encoding_a_Bitcoin_address",
        "https://en.bitcoin.it/wiki/RIPEMD-160",
        "https://en.bitcoin.it/wiki/Private_key",
        "https://github.com/bitcoin/bitcoin.git",
        "https://github.com/bitcoin/bitcoin/blob/master/src/base58.cpp",
        "https://github.com/luke-jr/libbase58.git",
        "http://lenschulwitz.com/b58/base58perl.txt",
        "https://en.bitcoin.it/wiki/Base58Check_encoding#Base58_symbol_chart",
        "https://github.com/spesmilo/electrum.git",
        "https://en.bitcoin.it/wiki/Secp256k1",
        "https://en.bitcoin.it/wiki/Elliptic_Curve_Digital_Signature_Algorithm",
        "https://en.bitcoin.it/wiki/Seed_phrase",
        "https://en.bitcoin.it/wiki/Seed_phrase#Two-factor_seed_phrases",
        "https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#Security",
        "https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#user-content-Specification_Key_derivation",
        "https://datatracker.ietf.org/doc/html/rfc4231",
        "https://datatracker.ietf.org/doc/html/rfc2104",
        "https://www.rfc-editor.org/info/bcp14",
        "https://datatracker.ietf.org/doc/html/rfc2119",
        "https://datatracker.ietf.org/doc/html/rfc3852",
        "https://datatracker.ietf.org/doc/html/rfc3275",
        "https://datatracker.ietf.org/doc/html/rfc2202",
        "https://bitcoin.org/bitcoin.pdf",
        "https://www.cryptopp.com/",
        "https://en.wikipedia.org/wiki/Elliptic-curve_cryptography",
        "https://www.cryptopp.com/wiki/MD5",
        "https://en.bitcoin.it/wiki/Binary_options",
        "https://en.bitcoin.it/wiki/Protocol_documentation#Block_Headers",
        "https://bitcoin.stackexchange.com/questions/2025/what-is-txins-sequence"
    ]
    
    def __init__(self, db_config: Dict = None):
        self.db_config = db_config or {
            'host': 'localhost',
            'port': 5432,
            'database': 'r3aler_ai',
            'user': 'r3aler_user_2025',
            'password': 'password123'
        }
    
    def get_connection(self):
        """Get database connection"""
        return psycopg2.connect(**self.db_config)
    
    def fetch_resource(self, url: str) -> Optional[str]:
        """Fetch resource content from URL"""
        try:
            headers = {'User-Agent': 'R3ALER-AI-Crypto-Ingestion/1.0'}
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"[ERROR] Failed to fetch {url}: {str(e)}")
            return None
    
    def categorize_resource(self, url: str) -> Dict[str, str]:
        """Categorize resource by URL"""
        categories = {
            'bitcoin_fundamentals': ['wallet', 'bitcoin.it/wiki/Wallet', 'private_key', 'seed_phrase'],
            'encoding': ['base58', 'encoding', 'ripemd'],
            'cryptography': ['secp256k1', 'ecdsa', 'elliptic', 'cryptopp', 'md5'],
            'key_derivation': ['bip-32', 'seed', 'derivation'],
            'specifications': ['rfc', 'datatracker.ietf', 'bcp14'],
            'implementations': ['github.com', 'bitcoin/bitcoin', 'electrum', 'libbase58'],
            'protocols': ['protocol_documentation', 'block_headers', 'txins']
        }
        
        category = 'general'
        subcategory = 'cryptocurrency'
        
        url_lower = url.lower()
        for cat, keywords in categories.items():
            if any(kw in url_lower for kw in keywords):
                category = cat
                break
        
        return {'category': category, 'subcategory': subcategory}
    
    def ingest_resources(self, callback=None) -> Dict[str, Any]:
        """Ingest all cryptocurrency resources into Crypto Unit"""
        results = {
            'total_urls': len(self.CRYPTO_RESOURCES),
            'successful': 0,
            'failed': 0,
            'resources': [],
            'timestamp': datetime.now().isoformat()
        }
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        for idx, url in enumerate(self.CRYPTO_RESOURCES, 1):
            if callback:
                callback(f"[{idx}/{len(self.CRYPTO_RESOURCES)}] Processing: {url}")
            
            try:
                content = self.fetch_resource(url)
                if not content:
                    results['failed'] += 1
                    continue
                
                cat_info = self.categorize_resource(url)
                entry_id = hashlib.md5(url.encode()).hexdigest()
                topic = url.split('/')[-1].replace('_', ' ').replace('#', ' - ')
                
                cursor.execute("""
                    INSERT INTO crypto_unit.knowledge 
                    (entry_id, topic, content, category, subcategory, source)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (entry_id) DO UPDATE SET
                        content = EXCLUDED.content
                """, (
                    entry_id,
                    topic,
                    content[:50000],
                    cat_info['category'],
                    cat_info['subcategory'],
                    url
                ))
                
                results['resources'].append({
                    'url': url,
                    'entry_id': entry_id,
                    'category': cat_info['category'],
                    'size': len(content),
                    'timestamp': datetime.now().isoformat()
                })
                
                results['successful'] += 1
                if callback:
                    callback(f"  [OK] Stored: {topic}")
                
            except Exception as e:
                results['failed'] += 1
                if callback:
                    callback(f"  [ERROR] {str(e)}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return results
    
    def get_crypto_unit_stats(self) -> Dict[str, Any]:
        """Get statistics from Crypto Unit"""
        conn = self.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_entries,
                    COUNT(DISTINCT category) as categories,
                    COUNT(DISTINCT source) as sources,
                    pg_size_pretty(pg_total_relation_size('crypto_unit.knowledge')) as size
                FROM crypto_unit.knowledge
            """)
            
            stats = dict(cursor.fetchone())
            return {
                'unit': 'crypto_unit',
                'name': 'Cryptocurrency Unit',
                'status': 'online',
                **stats
            }
        except Exception as e:
            print(f"[ERROR] Failed to get stats: {e}")
            return {'error': str(e)}
        finally:
            cursor.close()
            conn.close()
    
    def search_crypto_knowledge(self, query: str, limit: int = 10) -> List[Dict]:
        """Search cryptocurrency knowledge"""
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
            
            results = cursor.fetchall()
            return [dict(row) for row in results]
        except Exception as e:
            print(f"[ERROR] Search failed: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

def main():
    """Main ingestion process"""
    print("\n" + "="*70)
    print("R3ALER AI - CRYPTOCURRENCY KNOWLEDGE INGESTION")
    print("="*70)
    print("Target: Crypto Unit (Enhanced Storage Facility)")
    print("Resources: 32 cryptocurrency and cryptography sources")
    print("="*70 + "\n")
    
    ingestion = CryptoKnowledgeIngestion()
    
    def progress_callback(message):
        print(message)
    
    print("[STEP 1] Ingesting cryptocurrency resources...\n")
    results = ingestion.ingest_resources(callback=progress_callback)
    
    print(f"\n[STEP 2] Ingestion Summary:")
    print(f"  Total URLs: {results['total_urls']}")
    print(f"  Successful: {results['successful']}")
    print(f"  Failed: {results['failed']}")
    print(f"  Timestamp: {results['timestamp']}")
    
    print(f"\n[STEP 3] Crypto Unit Statistics:")
    stats = ingestion.get_crypto_unit_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n" + "="*70)
    print("INGESTION COMPLETE")
    print("="*70 + "\n")

if __name__ == '__main__':
    main()
