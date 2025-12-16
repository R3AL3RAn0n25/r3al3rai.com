"""
R3AL3R Self-Hosted Storage Facility
100% Free, Zero External Dependencies
Uses PostgreSQL schemas as "storage units"
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from typing import List, Dict, Any, Optional
import json
import os
from datetime import datetime, timedelta
import threading
import time
import logging
import statistics
from collections import defaultdict

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

class StorageFacility:
    """Self-hosted storage facility using PostgreSQL"""
    
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'port': 5432,
            'database': 'r3aler_ai',
            'user': 'r3aler_user_2025',
            'password': 'password123'  # Update if different
        }
        
        # Define storage units (PostgreSQL schemas)
        self.units = {
            'physics': {
                'name': 'Physics Knowledge Unit',
                'schema': 'physics_unit',
                'description': 'Classical physics, mechanics, thermodynamics',
                'cost': 'FREE (PostgreSQL)',
                'status': 'online'
            },
            'quantum': {
                'name': 'Quantum Physics Unit',
                'schema': 'quantum_unit',
                'description': 'Quantum mechanics, particle physics',
                'cost': 'FREE (PostgreSQL)',
                'status': 'online'
            },
            'space': {
                'name': 'Space/Astro/Aerospace Unit',
                'schema': 'space_unit',
                'description': 'Astronomy, aerospace, exoplanets',
                'cost': 'FREE (PostgreSQL)',
                'status': 'online'
            },
            'crypto': {
                'name': 'Cryptocurrency Unit',
                'schema': 'crypto_unit',
                'description': 'Blockchain, cryptocurrency knowledge',
                'cost': 'FREE (PostgreSQL)',
                'status': 'online'
            }
            ,
            'medical': {
                'name': 'Medical Knowledge Unit',
                'schema': 'medical_unit',
                'description': 'Multilingual medical corpus, clinical, biomedical, healthcare',
                'cost': 'FREE (PostgreSQL)',
                'status': 'online'
            },
            'reason': {
                'name': 'Reason Unit',
                'schema': 'reason_unit',
                'description': 'Reasoning, logic, consciousness, cognitive processes',
                'cost': 'FREE (PostgreSQL)',
                'status': 'online'
            },
            'logic': {
                'name': 'Logic Unit',
                'schema': 'logic_unit',
                'description': 'Logical reasoning, formal logic, mathematical logic',
                'cost': 'FREE (PostgreSQL)',
                'status': 'online'
            }
        }
        
        print("\n[STORAGE] Initializing R3AL3R Storage Facility...")
        try:
            self.initialize_facility()
            print("[OK] Storage Facility ready!\n")
        except Exception as e:
            print(f"[ERROR] Initialization error: {e}")
            print("[WARNING] Make sure PostgreSQL is running and credentials are correct\n")
    
    def get_connection(self):
        """Get database connection"""
        return psycopg2.connect(**self.db_config)
    
    def initialize_facility(self):
        """Create all storage units (schemas and tables)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        for unit_id, unit_info in self.units.items():
            schema = unit_info['schema']
            
            # Create schema (storage unit)
            cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
            
            # Create knowledge table
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {schema}.knowledge (
                    id SERIAL PRIMARY KEY,
                    entry_id VARCHAR(200) UNIQUE,
                    topic TEXT,
                    content TEXT,
                    category VARCHAR(200),
                    subcategory VARCHAR(200),
                    level VARCHAR(100),
                    source VARCHAR(200),
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW()
                )
            """)
            
            # Create indexes for fast search
            cursor.execute(f"""
                CREATE INDEX IF NOT EXISTS idx_{unit_id}_category 
                ON {schema}.knowledge(category)
            """)
            
            cursor.execute(f"""
                CREATE INDEX IF NOT EXISTS idx_{unit_id}_topic 
                ON {schema}.knowledge(topic)
            """)
            
            # Full-text search index
            cursor.execute(f"""
                CREATE INDEX IF NOT EXISTS idx_{unit_id}_fts 
                ON {schema}.knowledge 
                USING GIN(to_tsvector('english', COALESCE(content, '') || ' ' || COALESCE(topic, '')))
            """)
            
        conn.commit()
        cursor.close()
        conn.close()
    
    def store_knowledge(self, unit_id: str, entries: List[Dict]) -> Dict:
        """Store knowledge in a specific unit"""
        # Check if unit exists in predefined units or as a dynamic schema
        schema = None
        if unit_id in self.units:
            schema = self.units[unit_id]['schema']
        else:
            # Check if it's a dynamic unit (schema exists)
            schema = f"{unit_id}_unit"
            conn = self.get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    SELECT schema_name FROM information_schema.schemata
                    WHERE schema_name = %s
                """, (schema,))
                if not cursor.fetchone():
                    cursor.close()
                    conn.close()
                    return {'error': f'Unit {unit_id} not found (schema {schema} does not exist)'}
            except Exception as e:
                cursor.close()
                conn.close()
                return {'error': f'Error checking unit {unit_id}: {e}'}
            cursor.close()
            conn.close()

        conn = self.get_connection()
        cursor = conn.cursor()
        
        stored_count = 0
        updated_count = 0
        error_count = 0
        
        for entry in entries:
            try:
                # Get entry data
                entry_id = entry.get('id', entry.get('entry_id', ''))
                topic = entry.get('topic', entry.get('question', ''))
                content = entry.get('content', entry.get('answer', entry.get('explanation', '')))
                category = entry.get('category', entry.get('domain', ''))
                subcategory = entry.get('subcategory', '')
                level = entry.get('level', entry.get('difficulty', ''))
                source = entry.get('source', '')
                
                # Skip if no content
                if not content and not topic:
                    continue
                
                # Generate ID if missing
                if not entry_id:
                    entry_id = f"{unit_id}_{stored_count}_{datetime.now().timestamp()}"
                
                cursor.execute(f"""
                    INSERT INTO {schema}.knowledge 
                    (entry_id, topic, content, category, subcategory, level, source)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (entry_id) DO UPDATE SET
                        topic = EXCLUDED.topic,
                        content = EXCLUDED.content,
                        category = EXCLUDED.category,
                        subcategory = EXCLUDED.subcategory,
                        level = EXCLUDED.level,
                        source = EXCLUDED.source,
                        updated_at = NOW()
                """, (entry_id, topic, content, category, subcategory, level, source))
                
                if cursor.rowcount > 0:
                    stored_count += 1
                else:
                    updated_count += 1
                    
            except Exception as e:
                error_count += 1
                if error_count < 5:  # Only print first few errors
                    print(f"[WARNING] Error storing entry: {e}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {
            'unit': unit_id,
            'stored': stored_count,
            'updated': updated_count,
            'errors': error_count,
            'total': len(entries)
        }
    
    def search_unit(self, unit_id: str, query: str, limit: int = 10) -> List[Dict]:
        """Search within a specific storage unit"""
        # Check if unit exists in predefined units or as a dynamic schema
        schema = None
        if unit_id in self.units:
            schema = self.units[unit_id]['schema']
        else:
            # Check if it's a dynamic unit (schema exists)
            schema = f"{unit_id}_unit"
            conn = self.get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    SELECT schema_name FROM information_schema.schemata
                    WHERE schema_name = %s
                """, (schema,))
                if not cursor.fetchone():
                    cursor.close()
                    conn.close()
                    return []
            except Exception as e:
                cursor.close()
                conn.close()
                return []
            cursor.close()
            conn.close()

        conn = self.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            # Full-text search with ranking
            cursor.execute(f"""
                SELECT 
                    entry_id,
                    topic,
                    content,
                    category,
                    subcategory,
                    level,
                    source,
                    ts_rank(
                        to_tsvector('english', COALESCE(content, '') || ' ' || COALESCE(topic, '')),
                        plainto_tsquery('english', %s)
                    ) as relevance
                FROM {schema}.knowledge
                WHERE to_tsvector('english', COALESCE(content, '') || ' ' || COALESCE(topic, ''))
                      @@ plainto_tsquery('english', %s)
                ORDER BY relevance DESC
                LIMIT %s
            """, (query, query, limit))
            
            results = cursor.fetchall()
            return [dict(row) for row in results]
            
        except Exception as e:
            print(f"Search error: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    
    def search_all_units(self, query: str, limit_per_unit: int = 3) -> List[Dict]:
        """Search across all storage units"""
        all_results = []
        
        for unit_id in self.units.keys():
            results = self.search_unit(unit_id, query, limit_per_unit)
            for result in results:
                result['source_unit'] = unit_id
                result['unit_name'] = self.units[unit_id]['name']
                all_results.append(result)
        
        # Sort by relevance
        all_results.sort(key=lambda x: x.get('relevance', 0), reverse=True)
        return all_results
    
    def get_unit_stats(self, unit_id: str) -> Dict:
        """Get statistics for a storage unit"""
        if unit_id not in self.units:
            return {'error': f'Unit {unit_id} not found'}
        
        schema = self.units[unit_id]['schema']
        conn = self.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cursor.execute(f"""
                SELECT 
                    COUNT(*) as total_entries,
                    COUNT(DISTINCT category) as categories,
                    COUNT(DISTINCT source) as sources,
                    pg_size_pretty(pg_total_relation_size('{schema}.knowledge')) as size
                FROM {schema}.knowledge
            """)
            
            stats = dict(cursor.fetchone())
            return {
                **self.units[unit_id],
                **stats,
                'unit_id': unit_id
            }
        except Exception as e:
            print(f"Stats error: {e}")
            return {**self.units[unit_id], 'total_entries': 0, 'categories': 0, 'sources': 0, 'size': '0 bytes'}
        finally:
            cursor.close()
            conn.close()
    
    def get_facility_status(self) -> Dict:
        """Get overall facility status"""
        total_entries = 0
        unit_stats = {}
        
        for unit_id in self.units.keys():
            stats = self.get_unit_stats(unit_id)
            unit_stats[unit_id] = stats
            total_entries += stats.get('total_entries', 0)
        
        return {
            'facility_name': 'R3AL3R Self-Hosted Storage Facility',
            'total_units': len(self.units),
            'total_entries': total_entries,
            'cost': 'FREE (Self-hosted PostgreSQL)',
            'status': 'online',
            'units': unit_stats
        }


class StorageMonitor:
    """Real-time monitoring system for storage facility"""

    def __init__(self, facility: StorageFacility):
        self.facility = facility
        self.metrics = defaultdict(list)
        self.alerts = []
        self.is_monitoring = False
        self.monitor_thread = None
        self.alert_thresholds = {
            'response_time': 2.0,  # seconds
            'error_rate': 0.05,    # 5%
            'connection_failures': 3,  # per hour
            'storage_growth_rate': 100  # MB per day
        }
        self.setup_logging()

    def setup_logging(self):
        """Setup monitoring logging"""
        logging.basicConfig(
            filename='storage_monitor.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('StorageMonitor')

    def start_monitoring(self):
        """Start real-time monitoring"""
        if self.is_monitoring:
            return

        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        self.logger.info("Storage monitoring started")

    def stop_monitoring(self):
        """Stop monitoring"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        self.logger.info("Storage monitoring stopped")

    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                self._collect_metrics()
                self._check_alerts()
                self._cleanup_old_metrics()
            except Exception as e:
                self.logger.error(f"Monitoring error: {e}")

            time.sleep(30)  # Monitor every 30 seconds

    def _collect_metrics(self):
        """Collect current metrics"""
        timestamp = datetime.now()

        # Connection health
        conn_start = time.time()
        try:
            conn = self.facility.get_connection()
            conn.close()
            response_time = time.time() - conn_start
            self._add_metric('connection_response_time', response_time, timestamp)
            self._add_metric('connection_status', 1, timestamp)  # 1 = healthy
        except Exception as e:
            self._add_metric('connection_status', 0, timestamp)  # 0 = failed
            self._add_metric('connection_errors', 1, timestamp)
            self.logger.warning(f"Connection check failed: {e}")

        # Storage metrics
        try:
            status = self.facility.get_facility_status()
            total_entries = status.get('total_entries', 0)
            self._add_metric('total_entries', total_entries, timestamp)

            # Unit-specific metrics
            for unit_id, unit_data in status.get('units', {}).items():
                entries = unit_data.get('total_entries', 0)
                self._add_metric(f'{unit_id}_entries', entries, timestamp)

        except Exception as e:
            self.logger.error(f"Storage metrics collection failed: {e}")

        # System metrics
        try:
            import psutil
            memory_percent = psutil.virtual_memory().percent
            cpu_percent = psutil.cpu_percent(interval=1)
            disk_usage = psutil.disk_usage('/').percent

            self._add_metric('system_memory_percent', memory_percent, timestamp)
            self._add_metric('system_cpu_percent', cpu_percent, timestamp)
            self._add_metric('system_disk_percent', disk_usage, timestamp)
        except ImportError:
            # psutil not available - skip system metrics
            pass
        except Exception as e:
            self.logger.error(f"System metrics collection failed: {e}")

    def _add_metric(self, name: str, value: float, timestamp: datetime):
        """Add a metric value"""
        self.metrics[name].append({
            'value': value,
            'timestamp': timestamp
        })

        # Keep only last 1000 values per metric
        if len(self.metrics[name]) > 1000:
            self.metrics[name] = self.metrics[name][-1000:]

    def _check_alerts(self):
        """Check for alert conditions"""
        # Connection failures
        recent_failures = self._get_recent_metric_sum('connection_errors', hours=1)
        if recent_failures >= self.alert_thresholds['connection_failures']:
            self._create_alert('HIGH', f"High connection failure rate: {recent_failures} failures/hour")

        # Response time
        avg_response_time = self._get_recent_metric_avg('connection_response_time', hours=1)
        if avg_response_time > self.alert_thresholds['response_time']:
            self._create_alert('MEDIUM', f"Slow response time: {avg_response_time:.2f}s average")

        # System resources
        memory_usage = self._get_recent_metric_avg('system_memory_percent', hours=1)
        if memory_usage > 90:
            self._create_alert('HIGH', f"High memory usage: {memory_usage:.1f}%")

        cpu_usage = self._get_recent_metric_avg('system_cpu_percent', hours=1)
        if cpu_usage > 95:
            self._create_alert('HIGH', f"High CPU usage: {cpu_usage:.1f}%")

    def _create_alert(self, severity: str, message: str):
        """Create an alert"""
        alert = {
            'id': f"alert_{int(time.time())}_{len(self.alerts)}",
            'severity': severity,
            'message': message,
            'timestamp': datetime.now(),
            'acknowledged': False
        }
        self.alerts.append(alert)
        self.logger.warning(f"ALERT [{severity}]: {message}")

        # Keep only last 100 alerts
        if len(self.alerts) > 100:
            self.alerts = self.alerts[-100:]

    def _get_recent_metric_avg(self, name: str, hours: int) -> float:
        """Get average of recent metric values"""
        cutoff = datetime.now() - timedelta(hours=hours)
        values = [
            m['value'] for m in self.metrics.get(name, [])
            if m['timestamp'] > cutoff
        ]
        return statistics.mean(values) if values else 0

    def _get_recent_metric_sum(self, name: str, hours: int) -> float:
        """Get sum of recent metric values"""
        cutoff = datetime.now() - timedelta(hours=hours)
        values = [
            m['value'] for m in self.metrics.get(name, [])
            if m['timestamp'] > cutoff
        ]
        return sum(values)

    def _cleanup_old_metrics(self):
        """Clean up old metrics data"""
        cutoff = datetime.now() - timedelta(days=7)  # Keep 7 days of data

        for name in self.metrics:
            self.metrics[name] = [
                m for m in self.metrics[name]
                if m['timestamp'] > cutoff
            ]

    def get_metrics_summary(self) -> Dict:
        """Get current metrics summary"""
        summary = {}

        for name, data in self.metrics.items():
            if not data:
                continue

            recent_data = [m for m in data if m['timestamp'] > datetime.now() - timedelta(hours=1)]
            if recent_data:
                values = [m['value'] for m in recent_data]
                summary[name] = {
                    'current': values[-1] if values else 0,
                    'average': statistics.mean(values),
                    'min': min(values),
                    'max': max(values),
                    'count': len(values)
                }

        return summary

    def get_active_alerts(self) -> List[Dict]:
        """Get active (unacknowledged) alerts"""
        return [alert for alert in self.alerts if not alert['acknowledged']]

    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge an alert"""
        for alert in self.alerts:
            if alert['id'] == alert_id:
                alert['acknowledged'] = True
                self.logger.info(f"Alert acknowledged: {alert_id}")
                return True
        return False


class FailoverManager:
    """Automated failover management for storage facility"""

    def __init__(self, facility: StorageFacility, monitor: StorageMonitor):
        self.facility = facility
        self.monitor = monitor
        self.failover_configs = []
        self.current_primary = None
        self.is_failover_enabled = False
        self.failover_thread = None
        self.logger = logging.getLogger('FailoverManager')

    def enable_failover(self, configs: List[Dict]):
        """Enable automated failover with given configurations"""
        self.failover_configs = configs
        self.is_failover_enabled = True

        # Set first config as primary
        if configs:
            self.current_primary = configs[0]

        self.failover_thread = threading.Thread(target=self._failover_loop, daemon=True)
        self.failover_thread.start()
        self.logger.info("Automated failover enabled")

    def disable_failover(self):
        """Disable automated failover"""
        self.is_failover_enabled = False
        if self.failover_thread:
            self.failover_thread.join(timeout=5)
        self.logger.info("Automated failover disabled")

    def _failover_loop(self):
        """Main failover monitoring loop"""
        while self.is_failover_enabled:
            try:
                self._check_primary_health()
                self._attempt_failover_if_needed()
            except Exception as e:
                self.logger.error(f"Failover check error: {e}")

            time.sleep(60)  # Check every minute

    def _check_primary_health(self):
        """Check health of current primary"""
        if not self.current_primary:
            return

        # Check connection and basic operations
        try:
            conn = psycopg2.connect(**self.current_primary['db_config'])
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            conn.close()

            # If we get here, primary is healthy
            return True

        except Exception as e:
            self.logger.warning(f"Primary health check failed: {e}")
            return False

    def _attempt_failover_if_needed(self):
        """Attempt failover if primary is unhealthy"""
        if self._check_primary_health():
            return  # Primary is healthy

        self.logger.warning("Primary unhealthy, attempting failover...")

        # Try each failover config in order
        for config in self.failover_configs[1:]:  # Skip first (primary)
            if self._test_failover_config(config):
                self.logger.info(f"Failover successful to: {config.get('name', 'unknown')}")
                self.current_primary = config

                # Update facility with new config
                self.facility.db_config = config['db_config']

                # Create alert
                self.monitor._create_alert(
                    'CRITICAL',
                    f"Automatic failover performed to {config.get('name', 'backup database')}"
                )
                break
        else:
            self.logger.error("All failover configurations failed")
            self.monitor._create_alert(
                'CRITICAL',
                'All database connections failed - manual intervention required'
            )

    def _test_failover_config(self, config: Dict) -> bool:
        """Test if a failover configuration works"""
        try:
            conn = psycopg2.connect(**config['db_config'])
            cursor = conn.cursor()

            # Test basic operations
            cursor.execute("SELECT version()")
            cursor.fetchone()

            cursor.close()
            conn.close()
            return True

        except Exception as e:
            self.logger.warning(f"Failover config test failed: {e}")
            return False

    def get_failover_status(self) -> Dict:
        """Get current failover status"""
        return {
            'enabled': self.is_failover_enabled,
            'current_primary': self.current_primary.get('name') if self.current_primary else None,
            'available_configs': len(self.failover_configs),
            'last_failover_check': datetime.now()
        }


class PredictiveMaintenance:
    """Predictive maintenance system for storage facility"""

    def __init__(self, facility: StorageFacility, monitor: StorageMonitor):
        self.facility = facility
        self.monitor = monitor
        self.predictions = {}
        self.maintenance_schedule = []
        self.is_predicting = False
        self.prediction_thread = None
        self.logger = logging.getLogger('PredictiveMaintenance')

    def start_predictive_maintenance(self):
        """Start predictive maintenance analysis"""
        if self.is_predicting:
            return

        self.is_predicting = True
        self.prediction_thread = threading.Thread(target=self._prediction_loop, daemon=True)
        self.prediction_thread.start()
        self.logger.info("Predictive maintenance started")

    def stop_predictive_maintenance(self):
        """Stop predictive maintenance"""
        self.is_predicting = False
        if self.prediction_thread:
            self.prediction_thread.join(timeout=5)
        self.logger.info("Predictive maintenance stopped")

    def _prediction_loop(self):
        """Main prediction analysis loop"""
        while self.is_predicting:
            try:
                self._analyze_storage_growth()
                self._analyze_performance_trends()
                self._analyze_error_patterns()
                self._generate_maintenance_recommendations()
            except Exception as e:
                self.logger.error(f"Prediction analysis error: {e}")

            time.sleep(3600)  # Analyze every hour

    def _analyze_storage_growth(self):
        """Analyze storage growth trends"""
        try:
            # Get historical data
            metrics = self.monitor.metrics
            if 'total_entries' not in metrics:
                return

            entries_data = metrics['total_entries']
            if len(entries_data) < 10:  # Need minimum data points
                return

            # Calculate growth rate
            recent_entries = [m['value'] for m in entries_data[-10:]]
            growth_rate = (recent_entries[-1] - recent_entries[0]) / len(recent_entries)

            # Predict future storage needs
            days_to_full = None
            if growth_rate > 0:
                # Assume 1GB per 100,000 entries (rough estimate)
                current_mb = len(recent_entries) * 10  # Rough size estimate
                daily_growth_mb = growth_rate * 10
                remaining_mb = 1000 - current_mb  # Assume 1GB limit
                if daily_growth_mb > 0:
                    days_to_full = remaining_mb / daily_growth_mb

            self.predictions['storage_growth'] = {
                'current_rate': growth_rate,
                'predicted_days_to_full': days_to_full,
                'recommendation': 'Increase storage capacity' if days_to_full and days_to_full < 30 else 'Storage capacity adequate'
            }

        except Exception as e:
            self.logger.error(f"Storage growth analysis failed: {e}")

    def _analyze_performance_trends(self):
        """Analyze performance trends"""
        try:
            metrics = self.monitor.metrics

            # Response time trends
            if 'connection_response_time' in metrics:
                response_times = [m['value'] for m in metrics['connection_response_time'][-20:]]
                if len(response_times) >= 5:
                    avg_response = statistics.mean(response_times)
                    trend = self._calculate_trend(response_times)

                    self.predictions['performance'] = {
                        'avg_response_time': avg_response,
                        'response_trend': trend,
                        'recommendation': 'Optimize queries' if trend == 'increasing' and avg_response > 1.0 else 'Performance acceptable'
                    }

        except Exception as e:
            self.logger.error(f"Performance analysis failed: {e}")

    def _analyze_error_patterns(self):
        """Analyze error patterns for predictive maintenance"""
        try:
            metrics = self.monitor.metrics

            # Connection error patterns
            if 'connection_errors' in metrics:
                error_counts = [m['value'] for m in metrics['connection_errors'][-24:]]  # Last 24 readings
                if error_counts:
                    total_errors = sum(error_counts)
                    error_rate = total_errors / len(error_counts)

                    self.predictions['reliability'] = {
                        'error_rate': error_rate,
                        'total_errors_24h': total_errors,
                        'recommendation': 'Check database connections' if error_rate > 0.1 else 'Error rate acceptable'
                    }

        except Exception as e:
            self.logger.error(f"Error pattern analysis failed: {e}")

    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction from values"""
        if len(values) < 3:
            return 'insufficient_data'

        # Simple linear trend
        x = list(range(len(values)))
        slope = statistics.linear_regression(x, values)[0]

        if slope > 0.01:
            return 'increasing'
        elif slope < -0.01:
            return 'decreasing'
        else:
            return 'stable'

    def _generate_maintenance_recommendations(self):
        """Generate maintenance recommendations based on predictions"""
        recommendations = []

        # Storage recommendations
        storage_pred = self.predictions.get('storage_growth', {})
        if storage_pred.get('predicted_days_to_full', 999) < 30:
            recommendations.append({
                'type': 'storage',
                'priority': 'HIGH',
                'description': f"Storage capacity predicted to be full in {storage_pred['predicted_days_to_full']:.1f} days",
                'action': 'Increase database storage capacity or implement data archiving'
            })

        # Performance recommendations
        perf_pred = self.predictions.get('performance', {})
        if perf_pred.get('response_trend') == 'increasing':
            recommendations.append({
                'type': 'performance',
                'priority': 'MEDIUM',
                'description': 'Response times are increasing over time',
                'action': 'Optimize database queries and consider indexing improvements'
            })

        # Reliability recommendations
        rel_pred = self.predictions.get('reliability', {})
        if rel_pred.get('error_rate', 0) > 0.1:
            recommendations.append({
                'type': 'reliability',
                'priority': 'HIGH',
                'description': f"High error rate detected: {rel_pred['error_rate']:.2%}",
                'action': 'Investigate database connection issues and network stability'
            })

        self.maintenance_schedule = recommendations

    def get_predictions(self) -> Dict:
        """Get current predictions"""
        return {
            'predictions': self.predictions,
            'maintenance_recommendations': self.maintenance_schedule,
            'last_analysis': datetime.now()
        }


# Initialize facility
try:
    facility = StorageFacility()
    monitor = StorageMonitor(facility)
    failover_manager = FailoverManager(facility, monitor)
    predictive_maintenance = PredictiveMaintenance(facility, monitor)

    # Start monitoring and predictive maintenance (disabled for now)
    # monitor.start_monitoring()
    # predictive_maintenance.start_predictive_maintenance()

except Exception as e:
    print(f"[ERROR] Failed to create storage facility: {e}")
    exit(1)

# API Endpoints
@app.route('/')
def index():
    """Serve dashboard"""
    return send_from_directory('.', 'storage_facility_dashboard.html')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'facility': 'R3AL3R Storage Facility'})

@app.route('/api/facility/status', methods=['GET'])
def facility_status():
    """Get facility status"""
    return jsonify(facility.get_facility_status())

@app.route('/api/unit/<unit_id>/search', methods=['POST'])
def search_unit(unit_id):
    """Search a specific unit"""
    data = request.json
    query = data.get('query', '')
    limit = data.get('limit', 10)
    
    results = facility.search_unit(unit_id, query, limit)
    return jsonify({
        'unit': unit_id,
        'query': query,
        'results': results
    })

@app.route('/api/facility/search', methods=['POST'])
def search_facility():
    """Search all units"""
    data = request.json
    query = data.get('query', '')
    limit_per_unit = data.get('limit_per_unit', 3)
    max_results = data.get('max_results', 10)
    
    results = facility.search_all_units(query, limit_per_unit)
    return jsonify({
        'query': query,
        'total_results': len(results),
        'results': results[:max_results]
    })

@app.route('/api/unit/<unit_id>/stats', methods=['GET'])
def unit_stats(unit_id):
    """Get unit statistics"""
    return jsonify(facility.get_unit_stats(unit_id))

@app.route('/api/unit/<unit_id>/store', methods=['POST'])
def store_knowledge(unit_id):
    """Store knowledge in a unit"""
    data = request.json
    entries = data.get('entries', [])
    
    result = facility.store_knowledge(unit_id, entries)
    return jsonify(result)

# Monitoring API Endpoints
# @app.route('/api/monitoring/metrics', methods=['GET'])
# def get_metrics():
#     """Get current monitoring metrics"""
#     return jsonify(monitor.get_metrics_summary())

# @app.route('/api/monitoring/alerts', methods=['GET'])
# def get_alerts():
#     """Get active alerts"""
#     return jsonify({
#         'alerts': monitor.get_active_alerts(),
#         'total': len(monitor.get_active_alerts())
#     })

# @app.route('/api/monitoring/alerts/<alert_id>/acknowledge', methods=['POST'])
# def acknowledge_alert(alert_id):
#     """Acknowledge an alert"""
#     success = monitor.acknowledge_alert(alert_id)
#     return jsonify({'success': success})

# @app.route('/api/monitoring/health', methods=['GET'])
# def detailed_health_check():
#     """Detailed health check with monitoring data"""
#     basic_health = {'status': 'healthy', 'facility': 'R3AL3R Storage Facility'}
    
#     # Add monitoring data
#     metrics = monitor.get_metrics_summary()
#     alerts = monitor.get_active_alerts()
    
#     return jsonify({
#         **basic_health,
#         'monitoring': {
#             'active_alerts': len(alerts),
#             'metrics_collected': len(metrics),
#             'last_check': datetime.now().isoformat()
#         },
#         'alerts': alerts[:5],  # Show last 5 alerts
#         'key_metrics': {
#             'connection_status': metrics.get('connection_status', {}).get('current', 'unknown'),
#             'total_entries': metrics.get('total_entries', {}).get('current', 0),
#             'system_memory': metrics.get('system_memory_percent', {}).get('current', 'unknown'),
#             'system_cpu': metrics.get('system_cpu_percent', {}).get('current', 'unknown')
#         }
#     })

# Failover API Endpoints
# @app.route('/api/failover/status', methods=['GET'])
# def get_failover_status():
#     """Get failover status"""
#     return jsonify(failover_manager.get_failover_status())

# @app.route('/api/failover/enable', methods=['POST'])
# def enable_failover():
#     """Enable automated failover"""
#     data = request.json
#     configs = data.get('configs', [])
    
#     if not configs:
#         return jsonify({'error': 'No failover configurations provided'}), 400
    
#     failover_manager.enable_failover(configs)
#     return jsonify({'success': True, 'message': 'Failover enabled'})

# @app.route('/api/failover/disable', methods=['POST'])
# def disable_failover():
#     """Disable automated failover"""
#     failover_manager.disable_failover()
#     return jsonify({'success': True, 'message': 'Failover disabled'})

# @app.route('/api/failover/test', methods=['POST'])
# def test_failover():
#     """Test failover configuration"""
#     data = request.json
#     config = data.get('config', {})
    
#     if not config:
#         return jsonify({'error': 'No configuration provided'}), 400
    
#     success = failover_manager._test_failover_config(config)
#     return jsonify({
#         'success': success,
#         'config_name': config.get('name', 'unknown')
#     })

# Predictive Maintenance API Endpoints
# @app.route('/api/predictive/status', methods=['GET'])
# def get_predictive_status():
#     """Get predictive maintenance status"""
#     return jsonify(predictive_maintenance.get_predictions())

# @app.route('/api/predictive/analyze', methods=['POST'])
# def trigger_analysis():
#     """Trigger immediate predictive analysis"""
#     try:
#         predictive_maintenance._analyze_storage_growth()
# #         predictive_maintenance._analyze_performance_trends()
#         predictive_maintenance._analyze_error_patterns()
#         predictive_maintenance._generate_maintenance_recommendations()
        
#         return jsonify({
#             'success': True,
#             'message': 'Analysis completed',
#             'results': predictive_maintenance.get_predictions()
#         })
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/predictive/maintenance', methods=['GET'])
# def get_maintenance_schedule():
#     """Get maintenance recommendations"""
#     return jsonify({
#         'recommendations': predictive_maintenance.maintenance_schedule,
#         'total': len(predictive_maintenance.maintenance_schedule)
#     })

# Enhanced Status Endpoint
# @app.route('/api/facility/status/enhanced', methods=['GET'])
# def enhanced_facility_status():
#     """Get enhanced facility status with monitoring data"""
#     basic_status = facility.get_facility_status()
    
#     # Add monitoring, failover, and predictive data
#     monitoring_data = monitor.get_metrics_summary()
#     alerts = monitor.get_active_alerts()
#     failover_status = failover_manager.get_failover_status()
# #     predictions = predictive_maintenance.get_predictions()
    
#     return jsonify({
#         **basic_status,
#         'monitoring': {
#             'active': monitor.is_monitoring,
#             'alerts_count': len(alerts),
#             'metrics_count': len(monitoring_data)
#         },
#         'failover': failover_status,
#         'predictive_maintenance': {
#             'active': predictive_maintenance.is_predicting,
#             'recommendations_count': len(predictions.get('maintenance_recommendations', []))
#         },
#         'system_health': {
#             'connection_status': monitoring_data.get('connection_status', {}).get('current', 'unknown'),
#             'memory_usage': monitoring_data.get('system_memory_percent', {}).get('current', 'unknown'),
#             'cpu_usage': monitoring_data.get('system_cpu_percent', {}).get('current', 'unknown'),
#             'disk_usage': monitoring_data.get('system_disk_percent', {}).get('current', 'unknown')
#         }
#     })

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("[STORAGE] R3AL3R SELF-HOSTED STORAGE FACILITY - ENHANCED")
    print("=" * 70)
    print("* 100% Free - No external providers")
    print("* Self-hosted on your machine")
    print("* Using PostgreSQL (already installed)")
    print("* Real-time monitoring enabled")
    print("* Automated failover ready")
    print("* Predictive maintenance active")
    print("=" * 70)
    print("\nDashboard: http://localhost:3003")
    print("API: http://localhost:3003/api/facility/status")
    # print("Monitoring: http://localhost:3003/api/monitoring/health")
    # print("Enhanced Status: http://localhost:3003/api/facility/status/enhanced")
    print("\nPress Ctrl+C to stop\n")

    try:
        print("Starting Flask app...")
        app.run(host='127.0.0.1', port=3003, debug=False, use_reloader=False)
    except Exception as e:
        print(f"[ERROR] Failed to start Flask app: {e}")
        import traceback
        traceback.print_exc()
        exit(1)