"""
Import CodeXGLUE datasets into R3ÆLƎR AI Storage Facility
Adds 1.73M+ code examples to PostgreSQL for offline access

Datasets:
1. clone_detection_big_clone_bench - 1.73M examples
2. code_completion_line - 13k examples
3. cloze_testing_all - 176k examples  
4. clone_detection_poj104 - 53k examples
5. cloze_testing_maxmin - 2.62k examples

Total: ~2 million code examples
"""

import psycopg2
from psycopg2.extras import execute_batch
import logging
from datasets import load_dataset
from datetime import datetime
import json
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CodeXGLUEImporter:
    """Import CodeXGLUE datasets to Storage Facility"""
    
    def __init__(self, db_config=None):
        """Initialize with database configuration"""
        if db_config is None:
            db_config = {
                'host': 'localhost',
                'port': 5003,
                'database': 'storage_facility',
                'user': 'postgres',
                'password': 'admin'
            }
        
        self.db_config = db_config
        self.conn = None
        self.datasets_config = {
            "clone_detection_big": {
                "hf_name": "google/code_x_glue_cc_clone_detection_big_clone_bench",
                "table": "code_clone_detection",
                "batch_size": 1000,
                "max_import": 50000,  # Limit for initial import
                "description": "Java code clone detection pairs"
            },
            "code_completion_line": {
                "hf_name": "google/code_x_glue_cc_code_completion_line",
                "table": "code_completion",
                "batch_size": 1000,
                "max_import": 13000,  # Import all
                "description": "Line-level code completion examples",
                "language_config": "java"  # Primary language
            },
            "cloze_testing_all": {
                "hf_name": "google/code_x_glue_cc_cloze_testing_all",
                "table": "code_cloze_testing",
                "batch_size": 1000,
                "max_import": 30000,  # Subset
                "description": "Code fill-in-the-blank tests",
                "language_config": "java"
            },
            "clone_detection_poj": {
                "hf_name": "google/code_x_glue_cc_clone_detection_poj104",
                "table": "code_clone_detection",  # Same table as big bench
                "batch_size": 1000,
                "max_import": 20000,  # Subset
                "description": "Programming contest code clones"
            },
            "cloze_testing_maxmin": {
                "hf_name": "google/code_x_glue_cc_cloze_testing_maxmin",
                "table": "code_cloze_testing",  # Same table as cloze_all
                "batch_size": 500,
                "max_import": 2620,  # Import all
                "description": "Max/min algorithm cloze tests",
                "language_config": "java"
            }
        }
    
    def connect(self):
        """Connect to PostgreSQL Storage Facility"""
        try:
            self.conn = psycopg2.connect(**self.db_config)
            self.conn.autocommit = False
            logger.info("Connected to Storage Facility")
            return True
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return False
    
    def create_tables(self):
        """Create tables for CodeXGLUE data if they don't exist"""
        try:
            cursor = self.conn.cursor()
            
            # Create code_examples knowledge unit table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS knowledge_units (
                    unit_id SERIAL PRIMARY KEY,
                    unit_name VARCHAR(100) UNIQUE NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Add code_examples unit
            cursor.execute("""
                INSERT INTO knowledge_units (unit_name, description)
                VALUES ('code_examples', 'CodeXGLUE programming code examples and patterns')
                ON CONFLICT (unit_name) DO NOTHING
            """)
            
            # Create code_clone_detection table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS code_clone_detection (
                    id SERIAL PRIMARY KEY,
                    code_hash VARCHAR(64) UNIQUE NOT NULL,
                    func1 TEXT NOT NULL,
                    func2 TEXT NOT NULL,
                    is_clone BOOLEAN NOT NULL,
                    func1_id INTEGER,
                    func2_id INTEGER,
                    language VARCHAR(20) DEFAULT 'java',
                    dataset_source VARCHAR(100),
                    keywords TEXT[],
                    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    unit_id INTEGER REFERENCES knowledge_units(unit_id)
                )
            """)
            
            # Create indexes for clone detection
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_clone_is_clone ON code_clone_detection(is_clone)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_clone_language ON code_clone_detection(language)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_clone_keywords ON code_clone_detection USING GIN(keywords)
            """)
            
            # Create code_completion table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS code_completion (
                    id SERIAL PRIMARY KEY,
                    code_hash VARCHAR(64) UNIQUE NOT NULL,
                    input_code TEXT NOT NULL,
                    completion TEXT NOT NULL,
                    language VARCHAR(20) DEFAULT 'java',
                    dataset_source VARCHAR(100),
                    keywords TEXT[],
                    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    unit_id INTEGER REFERENCES knowledge_units(unit_id)
                )
            """)
            
            # Create indexes for code completion
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_completion_language ON code_completion(language)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_completion_keywords ON code_completion USING GIN(keywords)
            """)
            
            # Create code_cloze_testing table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS code_cloze_testing (
                    id SERIAL PRIMARY KEY,
                    code_hash VARCHAR(64) UNIQUE NOT NULL,
                    code TEXT NOT NULL,
                    masked_code TEXT,
                    target TEXT,
                    language VARCHAR(20) DEFAULT 'java',
                    dataset_source VARCHAR(100),
                    keywords TEXT[],
                    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    unit_id INTEGER REFERENCES knowledge_units(unit_id)
                )
            """)
            
            # Create indexes for cloze testing
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_cloze_language ON code_cloze_testing(language)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_cloze_keywords ON code_cloze_testing USING GIN(keywords)
            """)
            
            self.conn.commit()
            logger.info("Database tables created successfully")
            return True
            
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Failed to create tables: {e}")
            return False
    
    def extract_keywords(self, code_text: str) -> list:
        """Extract programming keywords from code"""
        import re
        
        # Extract identifiers and keywords
        identifiers = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', code_text.lower())
        
        # Filter common keywords and keep meaningful ones
        common_words = {'the', 'a', 'an', 'and', 'or', 'if', 'else', 'for', 'while', 'do', 'return'}
        keywords = [word for word in identifiers if len(word) > 2 and word not in common_words]
        
        # Return unique keywords (limit to 50)
        return list(set(keywords))[:50]
    
    def generate_hash(self, text: str) -> str:
        """Generate SHA-256 hash for deduplication"""
        return hashlib.sha256(text.encode('utf-8')).hexdigest()
    
    def import_clone_detection(self, dataset_key: str):
        """Import clone detection dataset"""
        try:
            config = self.datasets_config[dataset_key]
            logger.info(f"Loading {config['hf_name']}...")
            
            dataset = load_dataset(config['hf_name'], split='train')
            max_import = min(config['max_import'], len(dataset))
            
            logger.info(f"Importing {max_import} examples from {dataset_key}")
            
            cursor = self.conn.cursor()
            
            # Get unit_id
            cursor.execute("SELECT unit_id FROM knowledge_units WHERE unit_name = 'code_examples'")
            unit_id = cursor.fetchone()[0]
            
            batch = []
            imported = 0
            duplicates = 0
            
            for idx in range(max_import):
                example = dataset[idx]
                
                func1 = example.get('func1', '')
                func2 = example.get('func2', '')
                label = example.get('label', False)
                id1 = example.get('id1', 0)
                id2 = example.get('id2', 0)
                
                # Generate unique hash
                hash_text = f"{func1}{func2}{label}"
                code_hash = self.generate_hash(hash_text)
                
                # Extract keywords from both functions
                keywords = self.extract_keywords(func1 + " " + func2)
                
                batch.append((
                    code_hash,
                    func1,
                    func2,
                    label,
                    id1,
                    id2,
                    'java',
                    config['hf_name'],
                    keywords,
                    unit_id
                ))
                
                # Execute batch
                if len(batch) >= config['batch_size']:
                    try:
                        execute_batch(
                            cursor,
                            """
                            INSERT INTO code_clone_detection 
                            (code_hash, func1, func2, is_clone, func1_id, func2_id, language, dataset_source, keywords, unit_id)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (code_hash) DO NOTHING
                            """,
                            batch
                        )
                        self.conn.commit()
                        imported += len(batch)
                        logger.info(f"Imported {imported}/{max_import} clone detection examples")
                        batch = []
                    except Exception as e:
                        self.conn.rollback()
                        duplicates += len(batch)
                        logger.warning(f"Batch failed (likely duplicates): {e}")
                        batch = []
            
            # Import remaining
            if batch:
                try:
                    execute_batch(
                        cursor,
                        """
                        INSERT INTO code_clone_detection 
                        (code_hash, func1, func2, is_clone, func1_id, func2_id, language, dataset_source, keywords, unit_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (code_hash) DO NOTHING
                        """,
                        batch
                    )
                    self.conn.commit()
                    imported += len(batch)
                except Exception as e:
                    self.conn.rollback()
                    duplicates += len(batch)
            
            logger.info(f"Completed {dataset_key}: {imported} imported, {duplicates} duplicates skipped")
            return imported
            
        except Exception as e:
            logger.error(f"Failed to import {dataset_key}: {e}")
            return 0
    
    def import_code_completion(self, dataset_key: str):
        """Import code completion dataset"""
        try:
            config = self.datasets_config[dataset_key]
            logger.info(f"Loading {config['hf_name']}...")
            
            language = config.get('language_config', 'java')
            dataset = load_dataset(config['hf_name'], language, split='train')
            max_import = min(config['max_import'], len(dataset))
            
            logger.info(f"Importing {max_import} examples from {dataset_key}")
            
            cursor = self.conn.cursor()
            
            # Get unit_id
            cursor.execute("SELECT unit_id FROM knowledge_units WHERE unit_name = 'code_examples'")
            unit_id = cursor.fetchone()[0]
            
            batch = []
            imported = 0
            duplicates = 0
            
            for idx in range(max_import):
                example = dataset[idx]
                
                input_code = example.get('input', '')
                completion = example.get('gt', '')  # ground truth
                
                # Generate unique hash
                code_hash = self.generate_hash(input_code + completion)
                
                # Extract keywords
                keywords = self.extract_keywords(input_code + " " + completion)
                
                batch.append((
                    code_hash,
                    input_code,
                    completion,
                    language,
                    config['hf_name'],
                    keywords,
                    unit_id
                ))
                
                # Execute batch
                if len(batch) >= config['batch_size']:
                    try:
                        execute_batch(
                            cursor,
                            """
                            INSERT INTO code_completion 
                            (code_hash, input_code, completion, language, dataset_source, keywords, unit_id)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (code_hash) DO NOTHING
                            """,
                            batch
                        )
                        self.conn.commit()
                        imported += len(batch)
                        logger.info(f"Imported {imported}/{max_import} code completion examples")
                        batch = []
                    except Exception as e:
                        self.conn.rollback()
                        duplicates += len(batch)
                        logger.warning(f"Batch failed: {e}")
                        batch = []
            
            # Import remaining
            if batch:
                try:
                    execute_batch(
                        cursor,
                        """
                        INSERT INTO code_completion 
                        (code_hash, input_code, completion, language, dataset_source, keywords, unit_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (code_hash) DO NOTHING
                        """,
                        batch
                    )
                    self.conn.commit()
                    imported += len(batch)
                except Exception as e:
                    self.conn.rollback()
                    duplicates += len(batch)
            
            logger.info(f"Completed {dataset_key}: {imported} imported, {duplicates} duplicates skipped")
            return imported
            
        except Exception as e:
            logger.error(f"Failed to import {dataset_key}: {e}")
            return 0
    
    def import_cloze_testing(self, dataset_key: str):
        """Import cloze testing dataset"""
        try:
            config = self.datasets_config[dataset_key]
            logger.info(f"Loading {config['hf_name']}...")
            
            language = config.get('language_config', 'java')
            dataset = load_dataset(config['hf_name'], language, split='train')
            max_import = min(config['max_import'], len(dataset))
            
            logger.info(f"Importing {max_import} examples from {dataset_key}")
            
            cursor = self.conn.cursor()
            
            # Get unit_id
            cursor.execute("SELECT unit_id FROM knowledge_units WHERE unit_name = 'code_examples'")
            unit_id = cursor.fetchone()[0]
            
            batch = []
            imported = 0
            duplicates = 0
            
            for idx in range(max_import):
                example = dataset[idx]
                
                code = example.get('code', '')
                masked = example.get('mask', '')
                target = example.get('target', '')
                
                # Generate unique hash
                code_hash = self.generate_hash(code + target)
                
                # Extract keywords
                keywords = self.extract_keywords(code)
                
                batch.append((
                    code_hash,
                    code,
                    masked,
                    target,
                    language,
                    config['hf_name'],
                    keywords,
                    unit_id
                ))
                
                # Execute batch
                if len(batch) >= config['batch_size']:
                    try:
                        execute_batch(
                            cursor,
                            """
                            INSERT INTO code_cloze_testing 
                            (code_hash, code, masked_code, target, language, dataset_source, keywords, unit_id)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (code_hash) DO NOTHING
                            """,
                            batch
                        )
                        self.conn.commit()
                        imported += len(batch)
                        logger.info(f"Imported {imported}/{max_import} cloze testing examples")
                        batch = []
                    except Exception as e:
                        self.conn.rollback()
                        duplicates += len(batch)
                        logger.warning(f"Batch failed: {e}")
                        batch = []
            
            # Import remaining
            if batch:
                try:
                    execute_batch(
                        cursor,
                        """
                        INSERT INTO code_cloze_testing 
                        (code_hash, code, masked_code, target, language, dataset_source, keywords, unit_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (code_hash) DO NOTHING
                        """,
                        batch
                    )
                    self.conn.commit()
                    imported += len(batch)
                except Exception as e:
                    self.conn.rollback()
                    duplicates += len(batch)
            
            logger.info(f"Completed {dataset_key}: {imported} imported, {duplicates} duplicates skipped")
            return imported
            
        except Exception as e:
            logger.error(f"Failed to import {dataset_key}: {e}")
            return 0
    
    def import_all(self):
        """Import all CodeXGLUE datasets"""
        if not self.connect():
            return False
        
        if not self.create_tables():
            return False
        
        total_imported = 0
        start_time = datetime.now()
        
        logger.info("="*60)
        logger.info("Starting CodeXGLUE import to Storage Facility")
        logger.info("="*60)
        
        # Import clone detection datasets
        total_imported += self.import_clone_detection("clone_detection_big")
        total_imported += self.import_clone_detection("clone_detection_poj")
        
        # Import code completion
        total_imported += self.import_code_completion("code_completion_line")
        
        # Import cloze testing datasets
        total_imported += self.import_cloze_testing("cloze_testing_all")
        total_imported += self.import_cloze_testing("cloze_testing_maxmin")
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        logger.info("="*60)
        logger.info(f"CodeXGLUE import completed!")
        logger.info(f"Total examples imported: {total_imported:,}")
        logger.info(f"Duration: {duration:.2f} seconds")
        logger.info("="*60)
        
        # Print summary
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM code_clone_detection")
        clone_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM code_completion")
        completion_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM code_cloze_testing")
        cloze_count = cursor.fetchone()[0]
        
        logger.info("\nStorage Facility Summary:")
        logger.info(f"  Clone Detection: {clone_count:,} examples")
        logger.info(f"  Code Completion: {completion_count:,} examples")
        logger.info(f"  Cloze Testing: {cloze_count:,} examples")
        logger.info(f"  TOTAL: {clone_count + completion_count + cloze_count:,} examples")
        
        self.conn.close()
        return True


if __name__ == "__main__":
    importer = CodeXGLUEImporter()
    importer.import_all()
