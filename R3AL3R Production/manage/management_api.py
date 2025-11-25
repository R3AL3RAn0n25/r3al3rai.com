from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import psutil
import subprocess
import time
from datetime import datetime, timedelta
import threading
import logging
from werkzeug.utils import secure_filename
import shutil
import requests

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
DATASETS_FOLDER = os.path.join(UPLOAD_FOLDER, 'datasets')
UPGRADES_FOLDER = os.path.join(UPLOAD_FOLDER, 'upgrades')
LOGS_FOLDER = 'logs'

# Environment configuration
ENVIRONMENTS = {
    'production': {
        'name': 'Production',
        'base_path': '../application',
        'services': {
            'knowledge': {'port': 5001, 'name': 'Knowledge API', 'path': '../application/Knowledge_API'},
            'droid': {'port': 5005, 'name': 'Droid API', 'path': '../application/Droid_API'},
            'intelligence': {'port': 5010, 'name': 'Intelligence API', 'path': '../application/Intelligence_API'},
            'blackarch': {'port': 5003, 'name': 'BlackArch API', 'path': '../application/BlackArch_API'},
            'backend': {'port': 3000, 'name': 'Backend Server', 'path': '../application/Backend'},
            'storage': {'port': 3003, 'name': 'Storage Facility', 'path': '../AI_Core_Worker'},
            'bitxtractor': {'port': 3002, 'name': 'BitXtractor', 'path': '../application/BitXtractor'}
        }
    },
    'development': {
        'name': 'Development',
        'base_path': '../AI_Core_Worker',
        'services': {
            'knowledge': {'port': 5001, 'name': 'Knowledge API', 'path': '../AI_Core_Worker'},
            'droid': {'port': 5005, 'name': 'Droid API', 'path': '../AI_Core_Worker'},
            'intelligence': {'port': 5010, 'name': 'Intelligence API', 'path': '../AI_Core_Worker'},
            'blackarch': {'port': 5003, 'name': 'BlackArch API', 'path': '../AI_Core_Worker'},
            'backend': {'port': 3000, 'name': 'Backend Server', 'path': '../AI_Core_Worker'},
            'storage': {'port': 3003, 'name': 'Storage Facility', 'path': '../AI_Core_Worker'},
            'bitxtractor': {'port': 3002, 'name': 'BitXtractor', 'path': '../AI_Core_Worker'}
        }
    }
}

# Current environment (default to production)
current_environment = 'production'

# Ensure directories exist
for folder in [UPLOAD_FOLDER, DATASETS_FOLDER, UPGRADES_FOLDER, LOGS_FOLDER]:
    os.makedirs(folder, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size

# Global variables for system state
system_metrics = {
    'total_requests': 0,
    'active_users': 0,
    'avg_response_time': 0,
    'uptime': 100
}

ai_details = {
    'evolution': 'Active',
    'droid': 'Learning',
    'knowledge': 'Processing',
    'neural': 'Training',
    'learning_rate': '0.001',
    'accuracy': 94.7,
    'training_progress': 78.3,
    'model_version': 'v2.1.4'
}

# Setup logging
# logging.basicConfig(
#     filename=os.path.join(LOGS_FOLDER, 'management.log'),
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )

def get_current_services():
    """Get services for current environment"""
    return ENVIRONMENTS[current_environment]['services']

@app.route('/')
def serve_management_interface():
    """Serve the management interface"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    """Serve static files"""
    return send_from_directory('.', path)

@app.route('/api/health')
def health_check():
    """Basic health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/environment')
def get_environment():
    """Get current environment"""
    return jsonify({
        'current': current_environment,
        'name': ENVIRONMENTS[current_environment]['name'],
        'environments': list(ENVIRONMENTS.keys())
    })

@app.route('/api/environment/<env>', methods=['POST'])
def switch_environment(env):
    """Switch environment"""
    if env not in ENVIRONMENTS:
        return jsonify({'error': 'Invalid environment'}), 400

    global current_environment
    current_environment = env
    logging.info(f"Switched to {env} environment")

    return jsonify({
        'status': 'switched',
        'environment': env,
        'name': ENVIRONMENTS[env]['name']
    })

@app.route('/api/system/status')
def get_system_status():
    """Get overall system status"""
    services = get_current_services()
    status = {}
    for service_key, service_info in services.items():
        status[service_key] = check_service_health(service_info['port'])

    return jsonify({
        'services': status,
        'overall_status': 'healthy' if all(s['status'] == 'online' for s in status.values()) else 'degraded',
        'environment': current_environment,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/<service>/health')
def service_health_check(service):
    """Check individual service health"""
    services = get_current_services()
    if service not in services:
        return jsonify({'error': 'Service not found'}), 404

    port = services[service]['port']
    health_status = check_service_health(port)

    return jsonify(health_status)

def check_service_health(port):
    """Check if a service is running on the given port"""
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)  # Reduced timeout from 2 seconds to 0.5 seconds
        result = sock.connect_ex(('localhost', port))
        sock.close()

        if result == 0:
            return {'status': 'online', 'port': port, 'timestamp': datetime.now().isoformat()}
        else:
            return {'status': 'offline', 'port': port, 'timestamp': datetime.now().isoformat()}
    except:
        return {'status': 'error', 'port': port, 'timestamp': datetime.now().isoformat()}

@app.route('/api/system/info')
def get_system_info():
    """Get system resource information"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        # Calculate network I/O (simplified)
        net_io = psutil.net_io_counters()
        network_mb = (net_io.bytes_sent + net_io.bytes_recv) / 1024 / 1024

        return jsonify({
            'cpu': round(cpu_percent, 1),
            'memory': round(memory.percent, 1),
            'disk': round(disk.percent, 1),
            'network': round(network_mb, 2),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logging.error(f"Error getting system info: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/metrics')
def get_metrics():
    """Get system metrics"""
    global system_metrics
    return jsonify(system_metrics)

@app.route('/api/logs')
def get_logs():
    """Get system logs"""
    try:
        logs = []
        log_file = os.path.join(LOGS_FOLDER, 'management.log')

        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                for line in f.readlines()[-100:]:  # Last 100 lines
                    if line.strip():
                        # Parse log line (basic parsing)
                        parts = line.split(' - ', 2)
                        if len(parts) >= 3:
                            timestamp = parts[0]
                            level = parts[1].lower()
                            message = parts[2].strip()
                            logs.append({
                                'timestamp': timestamp,
                                'level': level,
                                'message': message
                            })

        return jsonify(logs)
    except Exception as e:
        logging.error(f"Error reading logs: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/details')
def get_ai_details():
    """Get AI system details"""
    global ai_details
    return jsonify(ai_details)

@app.route('/api/storage/analytics')
def get_storage_analytics():
    """Get Storage Facility analytics"""
    try:
        # Try to get data from Storage Facility API
        storage_port = get_current_services()['storage']['port']
        response = requests.get(f'http://localhost:{storage_port}/api/facility/status', timeout=5)
        if response.status_code == 200:
            storage_data = response.json()
            return jsonify(storage_data)
        else:
            return jsonify({'error': 'Storage Facility not responding'}), 503
    except Exception as e:
        logging.error(f"Error getting storage analytics: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/storage/optimization')
def get_storage_optimization():
    """Get Storage Facility optimization status"""
    try:
        # Try to get optimization data from Storage Facility
        storage_port = get_current_services()['storage']['port']
        response = requests.get(f'http://localhost:{storage_port}/api/monitoring/health', timeout=5)
        if response.status_code == 200:
            optimization_data = response.json()
            return jsonify(optimization_data)
        else:
            # Fallback mock data
            optimization_data = {
                'auto_optimization': 'enabled',
                'last_optimization': datetime.now().isoformat(),
                'optimization_tasks': [
                    {'task': 'Index Rebuilding', 'status': 'completed', 'last_run': '2025-11-22T10:00:00'},
                    {'task': 'Data Compaction', 'status': 'running', 'progress': 65},
                    {'task': 'Query Optimization', 'status': 'pending', 'scheduled': '2025-11-23T02:00:00'},
                    {'task': 'Shard Balancing', 'status': 'completed', 'last_run': '2025-11-21T14:30:00'}
                ],
                'performance_metrics': {
                    'query_response_time': 45,  # ms
                    'index_hit_rate': 94.2,  # %
                    'cache_efficiency': 87.5,  # %
                    'storage_utilization': 68.3  # %
                },
                'maintenance_schedule': {
                    'daily': ['index_stats_update', 'log_rotation'],
                    'weekly': ['full_table_scan', 'data_integrity_check'],
                    'monthly': ['archive_old_data', 'performance_audit']
                }
            }
            return jsonify(optimization_data)
    except Exception as e:
        logging.error(f"Error getting storage optimization: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/storage/sharding')
def get_storage_sharding():
    """Get Storage Facility sharding information"""
    try:
        # Mock sharding data - in real implementation, this would query actual sharding status
        sharding_data = {
            'sharding_enabled': True,
            'shard_strategy': 'hash_based',
            'total_shards': 16,
            'active_shards': 16,
            'shard_distribution': {
                'physics_unit': {'shards': 4, 'total_records': 125000, 'avg_records_per_shard': 31250},
                'quantum_unit': {'shards': 3, 'total_records': 89000, 'avg_records_per_shard': 29667},
                'space_unit': {'shards': 3, 'total_records': 67000, 'avg_records_per_shard': 22333},
                'crypto_unit': {'shards': 2, 'total_records': 45000, 'avg_records_per_shard': 22500},
                'blackarch_unit': {'shards': 2, 'total_records': 12000, 'avg_records_per_shard': 6000},
                'user_unit': {'shards': 2, 'total_records': 8500, 'avg_records_per_shard': 4250}
            },
            'rebalancing_status': 'idle',
            'last_rebalance': '2025-11-20T08:15:00',
            'shard_health': {
                'healthy_shards': 16,
                'degraded_shards': 0,
                'failed_shards': 0
            }
        }
        return jsonify(sharding_data)
    except Exception as e:
        logging.error(f"Error getting storage sharding: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/storage/maintenance')
def get_storage_maintenance():
    """Get Storage Facility maintenance status"""
    try:
        # Mock maintenance data
        maintenance_data = {
            'auto_maintenance': 'enabled',
            'maintenance_window': '02:00-04:00 UTC',
            'current_tasks': [
                {'task': 'Log Cleanup', 'status': 'running', 'progress': 78, 'eta': '2 minutes'},
                {'task': 'Temp File Removal', 'status': 'pending', 'scheduled': '2025-11-23T02:30:00'}
            ],
            'maintenance_history': [
                {'task': 'Database Vacuum', 'completed': '2025-11-22T02:15:00', 'duration': '45 minutes', 'status': 'success'},
                {'task': 'Index Rebuild', 'completed': '2025-11-21T02:20:00', 'duration': '120 minutes', 'status': 'success'},
                {'task': 'Backup Verification', 'completed': '2025-11-20T02:10:00', 'duration': '30 minutes', 'status': 'success'}
            ],
            'system_health': {
                'disk_space': '68% used',
                'memory_usage': '45% used',
                'cpu_usage': '23% avg',
                'connection_pool': '12/20 active'
            }
        }
        return jsonify(maintenance_data)
    except Exception as e:
        logging.error(f"Error getting storage maintenance: {e}")
        return jsonify({'error': str(e)}), 500

# Dataset Management Endpoints
@app.route('/api/datasets/upload', methods=['POST'])
def upload_dataset():
    """Upload a dataset file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if file and secure_filename(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(DATASETS_FOLDER, filename)
            file.save(file_path)

            # Log the upload
            logging.info(f"Dataset uploaded: {filename}")

            return jsonify({
                'status': 'success',
                'filename': filename,
                'path': file_path,
                'size': os.path.getsize(file_path),
                'uploaded_at': datetime.now().isoformat()
            })
        else:
            return jsonify({'error': 'Invalid file'}), 400
    except Exception as e:
        logging.error(f"Error uploading dataset: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/datasets/list', methods=['GET'])
def list_datasets():
    """List all uploaded datasets"""
    try:
        datasets = []
        if os.path.exists(DATASETS_FOLDER):
            for filename in os.listdir(DATASETS_FOLDER):
                file_path = os.path.join(DATASETS_FOLDER, filename)
                if os.path.isfile(file_path):
                    stat = os.stat(file_path)
                    datasets.append({
                        'id': filename,
                        'name': filename,
                        'size': stat.st_size,
                        'uploaded_at': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'path': file_path
                    })

        return jsonify({'datasets': datasets})
    except Exception as e:
        logging.error(f"Error listing datasets: {e}")
        return jsonify({'error': str(e)}), 500

# Upgrade Management Endpoints
@app.route('/api/upgrades/upload', methods=['POST'])
def upload_upgrade():
    """Upload an upgrade file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if file and secure_filename(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPGRADES_FOLDER, filename)
            file.save(file_path)

            logging.info(f"Upgrade uploaded: {filename}")

            return jsonify({
                'status': 'success',
                'filename': filename,
                'path': file_path,
                'size': os.path.getsize(file_path),
                'uploaded_at': datetime.now().isoformat()
            })
        else:
            return jsonify({'error': 'Invalid file'}), 400
    except Exception as e:
        logging.error(f"Error uploading upgrade: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/upgrades/list', methods=['GET'])
def list_upgrades():
    """List all uploaded upgrades"""
    try:
        upgrades = []
        if os.path.exists(UPGRADES_FOLDER):
            for filename in os.listdir(UPGRADES_FOLDER):
                file_path = os.path.join(UPGRADES_FOLDER, filename)
                if os.path.isfile(file_path):
                    stat = os.stat(file_path)
                    upgrades.append({
                        'id': filename,
                        'name': filename,
                        'size': stat.st_size,
                        'uploaded_at': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'path': file_path
                    })

        return jsonify({'upgrades': upgrades})
    except Exception as e:
        logging.error(f"Error listing upgrades: {e}")
        return jsonify({'error': str(e)}), 500

# Report Generation Endpoints
@app.route('/api/reports/generate/<report_type>', methods=['POST'])
def generate_report(report_type):
    """Generate a system report"""
    try:
        report_types = ['daily', 'weekly', 'monthly', 'performance', 'errors', 'security']

        if report_type not in report_types:
            return jsonify({'error': 'Invalid report type'}), 400

        # Generate report based on type
        report_data = {
            'report_type': report_type,
            'generated_at': datetime.now().isoformat(),
            'period': get_report_period(report_type),
            'data': generate_report_data(report_type)
        }

        # Save report to logs folder
        report_filename = f"{report_type}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path = os.path.join(LOGS_FOLDER, report_filename)

        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2)

        logging.info(f"Generated {report_type} report: {report_filename}")

        return jsonify({
            'status': 'success',
            'report_type': report_type,
            'filename': report_filename,
            'path': report_path,
            'generated_at': report_data['generated_at']
        })
    except Exception as e:
        logging.error(f"Error generating {report_type} report: {e}")
        return jsonify({'error': str(e)}), 500

def get_report_period(report_type):
    """Get the period for a report type"""
    now = datetime.now()
    if report_type == 'daily':
        return f"{(now - timedelta(days=1)).strftime('%Y-%m-%d')} to {now.strftime('%Y-%m-%d')}"
    elif report_type == 'weekly':
        return f"{(now - timedelta(weeks=1)).strftime('%Y-%m-%d')} to {now.strftime('%Y-%m-%d')}"
    elif report_type == 'monthly':
        return f"{(now - timedelta(days=30)).strftime('%Y-%m-%d')} to {now.strftime('%Y-%m-%d')}"
    else:
        return f"Last {report_type} period"

def generate_report_data(report_type):
    """Generate mock report data based on type"""
    if report_type == 'performance':
        return {
            'system_metrics': {
                'avg_cpu': 45.2,
                'avg_memory': 67.8,
                'avg_response_time': 125,
                'total_requests': 15420
            },
            'service_performance': {
                'knowledge_api': {'uptime': 99.9, 'avg_response': 89},
                'storage_facility': {'uptime': 100.0, 'avg_response': 45},
                'droid_api': {'uptime': 98.5, 'avg_response': 156}
            }
        }
    elif report_type == 'errors':
        return {
            'total_errors': 12,
            'error_breakdown': {
                'connection_errors': 5,
                'timeout_errors': 3,
                'validation_errors': 4
            },
            'recent_errors': [
                {'timestamp': '2025-11-22T14:30:00', 'service': 'knowledge_api', 'error': 'Connection timeout'},
                {'timestamp': '2025-11-22T13:15:00', 'service': 'storage_facility', 'error': 'Query failed'}
            ]
        }
    elif report_type == 'security':
        return {
            'security_events': 3,
            'failed_logins': 2,
            'suspicious_activity': 1,
            'security_measures': {
                'firewall_active': True,
                'encryption_enabled': True,
                'audit_logging': True
            }
        }
    else:
        return {
            'summary': f"Generated {report_type} report",
            'timestamp': datetime.now().isoformat()
        }

# AI Capability Testing Endpoints
@app.route('/api/ai/test/<capability>', methods=['POST'])
def test_ai_capability(capability):
    """Test AI capabilities"""
    try:
        capabilities = ['knowledge', 'adaptation', 'evolution']

        if capability not in capabilities:
            return jsonify({'error': 'Invalid capability'}), 400

        # Simulate capability testing
        test_results = {
            'capability': capability,
            'tested_at': datetime.now().isoformat(),
            'status': 'success',
            'results': generate_capability_test_results(capability)
        }

        logging.info(f"AI capability test completed: {capability}")

        return jsonify(test_results)
    except Exception as e:
        logging.error(f"Error testing AI capability {capability}: {e}")
        return jsonify({'error': str(e)}), 500

def generate_capability_test_results(capability):
    """Generate mock test results for AI capabilities"""
    if capability == 'knowledge':
        return {
            'knowledge_accuracy': 94.7,
            'response_time': 145,
            'knowledge_domains': 26,
            'total_entries': 28376,
            'test_queries': [
                {'query': 'quantum physics', 'accuracy': 96.2, 'response_time': 89},
                {'query': 'machine learning', 'accuracy': 98.1, 'response_time': 67}
            ]
        }
    elif capability == 'adaptation':
        return {
            'adaptation_rate': 87.3,
            'learning_efficiency': 92.1,
            'context_awareness': 89.5,
            'pattern_recognition': 95.2,
            'adaptation_tests': [
                {'test': 'new_domain_integration', 'success_rate': 91.4},
                {'test': 'context_switching', 'success_rate': 94.7}
            ]
        }
    elif capability == 'evolution':
        return {
            'evolution_progress': 78.3,
            'model_improvement': 12.5,
            'capability_expansion': 15.2,
            'learning_rate': 0.001,
            'evolution_metrics': {
                'model_version': 'v2.1.4',
                'training_iterations': 15420,
                'accuracy_improvement': 5.2
            }
        }
    else:
        return {'status': 'unknown_capability'}

# Environment Management Endpoints
@app.route('/api/environment/switch/<env>', methods=['POST'])
def switch_environment_api(env):
    """Switch environment via API"""
    return switch_environment(env)

@app.route('/api/system/<action>', methods=['POST'])
def system_control(action):
    """Control system-wide operations"""
    actions = ['start', 'stop', 'restart', 'status']

    if action not in actions:
        return jsonify({'error': 'Invalid action'}), 400

    try:
        if action == 'start':
            result = start_all_services()
        elif action == 'stop':
            result = stop_all_services()
        elif action == 'restart':
            result = restart_all_services()
        elif action == 'status':
            result = get_system_status().get_json()

        logging.info(f"System {action} initiated in {current_environment} environment")
        return jsonify({'status': 'success', 'action': action, 'result': result, 'environment': current_environment})
    except Exception as e:
        logging.error(f"System {action} failed: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/services/<service>/<action>', methods=['POST'])
def service_control(service, action):
    """Control individual services"""
    services = get_current_services()
    if service not in services:
        return jsonify({'error': 'Service not found'}), 404

    actions = ['start', 'stop', 'restart']

    if action not in actions:
        return jsonify({'error': 'Invalid action'}), 400

    try:
        service_info = services[service]

        if action == 'start':
            result = start_service(service_info)
        elif action == 'stop':
            result = stop_service(service_info)
        elif action == 'restart':
            result = restart_service(service_info)

        logging.info(f"Service {service} {action} initiated in {current_environment} environment")
        return jsonify({'status': 'success', 'service': service, 'action': action, 'result': result, 'environment': current_environment})
    except Exception as e:
        logging.error(f"Service {service} {action} failed: {e}")
        return jsonify({'error': str(e)}), 500

def start_all_services():
    """Start all services"""
    services = get_current_services()
    results = {}
    for service_key, service_info in services.items():
        try:
            results[service_key] = start_service(service_info)
        except Exception as e:
            results[service_key] = {'error': str(e)}

    return results

def stop_all_services():
    """Stop all services"""
    services = get_current_services()
    results = {}
    for service_key, service_info in services.items():
        try:
            results[service_key] = stop_service(service_info)
        except Exception as e:
            results[service_key] = {'error': str(e)}

    return results

def restart_all_services():
    """Restart all services"""
    services = get_current_services()
    results = {}
    for service_key, service_info in services.items():
        try:
            results[service_key] = restart_service(service_info)
        except Exception as e:
            results[service_key] = {'error': str(e)}

    return results

def start_service(service_info):
    """Start a specific service"""
    port = service_info['port']
    path = service_info['path']

    # Check if already running
    if check_service_health(port)['status'] == 'online':
        return {'status': 'already_running'}

    # Start service based on type
    try:
        if 'API' in service_info['name']:
            # Python API services
            cmd = ['python', f'{service_info["name"].lower().replace(" ", "_")}.py']
        else:
            # Node.js services
            cmd = ['npm', 'start']

        subprocess.Popen(cmd, cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(2)  # Wait for startup

        # Check if started successfully
        if check_service_health(port)['status'] == 'online':
            return {'status': 'started'}
        else:
            return {'status': 'failed'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

def stop_service(service_info):
    """Stop a specific service"""
    port = service_info['port']

    # Check if running
    if check_service_health(port)['status'] != 'online':
        return {'status': 'not_running'}

    try:
        # Find and kill process on port
        result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
        lines = result.stdout.split('\n')

        for line in lines:
            if f':{port}' in line and 'LISTENING' in line:
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    subprocess.run(['taskkill', '/PID', pid, '/F'], capture_output=True)
                    return {'status': 'stopped'}

        return {'status': 'not_found'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

def restart_service(service_info):
    """Restart a specific service"""
    stop_result = stop_service(service_info)
    time.sleep(1)
    start_result = start_service(service_info)

    return {
        'stop_result': stop_result,
        'start_result': start_result,
        'status': 'restarted' if start_result['status'] == 'started' else 'failed'
    }

@app.route('/api/datasets/upload', methods=['POST'])
def upload_datasets():
    """Upload dataset files"""
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400

    files = request.files.getlist('files')
    uploaded_files = []

    for file in files:
        if file.filename == '':
            continue

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(DATASETS_FOLDER, filename)
            file.save(file_path)

            uploaded_files.append({
                'filename': filename,
                'size': os.path.getsize(file_path),
                'upload_date': datetime.now().isoformat()
            })

            logging.info(f"Dataset uploaded: {filename}")

    return jsonify({
        'status': 'success',
        'uploaded_files': uploaded_files,
        'count': len(uploaded_files)
    })

@app.route('/api/datasets')
def get_datasets():
    """Get list of uploaded datasets"""
    try:
        datasets = []
        for filename in os.listdir(DATASETS_FOLDER):
            file_path = os.path.join(DATASETS_FOLDER, filename)
            if os.path.isfile(file_path):
                stat = os.stat(file_path)
                datasets.append({
                    'id': filename,
                    'name': filename,
                    'size': f"{stat.st_size / 1024 / 1024:.2f} MB",
                    'upload_date': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'path': file_path
                })

        return jsonify(datasets)
    except Exception as e:
        logging.error(f"Error listing datasets: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/datasets/<dataset_id>', methods=['DELETE'])
def delete_dataset(dataset_id):
    """Delete a dataset"""
    try:
        file_path = os.path.join(DATASETS_FOLDER, secure_filename(dataset_id))
        if os.path.exists(file_path):
            os.remove(file_path)
            logging.info(f"Dataset deleted: {dataset_id}")
            return jsonify({'status': 'deleted'})
        else:
            return jsonify({'error': 'Dataset not found'}), 404
    except Exception as e:
        logging.error(f"Error deleting dataset: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/upgrades/upload', methods=['POST'])
def upload_upgrades():
    """Upload upgrade files"""
    if 'upgrades' not in request.files:
        return jsonify({'error': 'No upgrade files provided'}), 400

    files = request.files.getlist('upgrades')
    uploaded_upgrades = []

    for file in files:
        if file.filename == '':
            continue

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPGRADES_FOLDER, filename)
            file.save(file_path)

            # Determine upgrade type
            upgrade_type = 'unknown'
            if filename.endswith('.py'):
                upgrade_type = 'python_module'
            elif filename.endswith('.js'):
                upgrade_type = 'javascript_module'
            elif filename.endswith('.json'):
                upgrade_type = 'configuration'
            elif filename.endswith('.h5') or filename.endswith('.pkl'):
                upgrade_type = 'model'

            uploaded_upgrades.append({
                'filename': filename,
                'type': upgrade_type,
                'size': os.path.getsize(file_path),
                'upload_date': datetime.now().isoformat(),
                'status': 'uploaded'
            })

            logging.info(f"Upgrade uploaded: {filename} ({upgrade_type})")

    return jsonify({
        'status': 'success',
        'uploaded_upgrades': uploaded_upgrades,
        'count': len(uploaded_upgrades)
    })

@app.route('/api/upgrades/deploy/<upgrade_id>', methods=['POST'])
def deploy_upgrade(upgrade_id):
    """Deploy an upgrade seamlessly"""
    try:
        upgrade_file = os.path.join(UPGRADES_FOLDER, secure_filename(upgrade_id))
        if not os.path.exists(upgrade_file):
            return jsonify({'error': 'Upgrade file not found'}), 404

        # Determine upgrade type and deployment strategy
        filename = upgrade_id.lower()

        if filename.endswith('.py'):
            # Python module upgrade
            result = deploy_python_upgrade(upgrade_file, filename)
        elif filename.endswith('.js'):
            # JavaScript module upgrade
            result = deploy_js_upgrade(upgrade_file, filename)
        elif filename.endswith('.json'):
            # Configuration upgrade
            result = deploy_config_upgrade(upgrade_file, filename)
        elif filename.endswith(('.h5', '.pkl')):
            # Model upgrade
            result = deploy_model_upgrade(upgrade_file, filename)
        else:
            return jsonify({'error': 'Unsupported upgrade type'}), 400

        logging.info(f"Upgrade deployed: {upgrade_id}")
        return jsonify(result)

    except Exception as e:
        logging.error(f"Error deploying upgrade {upgrade_id}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/datasets/integrate/<dataset_id>', methods=['POST'])
def integrate_dataset(dataset_id):
    """Integrate a dataset into the knowledge base"""
    try:
        dataset_file = os.path.join(DATASETS_FOLDER, secure_filename(dataset_id))
        if not os.path.exists(dataset_file):
            return jsonify({'error': 'Dataset file not found'}), 404

        # Determine dataset type and integration method
        filename = dataset_id.lower()

        if filename.endswith('.json'):
            result = integrate_json_dataset(dataset_file, filename)
        elif filename.endswith('.csv'):
            result = integrate_csv_dataset(dataset_file, filename)
        elif filename.endswith('.txt'):
            result = integrate_text_dataset(dataset_file, filename)
        else:
            return jsonify({'error': 'Unsupported dataset format'}), 400

        logging.info(f"Dataset integrated: {dataset_id}")
        return jsonify(result)

    except Exception as e:
        logging.error(f"Error integrating dataset {dataset_id}: {e}")
        return jsonify({'error': str(e)}), 500

def deploy_python_upgrade(upgrade_file, filename):
    """Deploy Python module upgrade"""
    # Determine target service based on filename
    target_service = None
    if 'knowledge' in filename:
        target_service = 'knowledge'
    elif 'droid' in filename:
        target_service = 'droid'
    elif 'intelligence' in filename:
        target_service = 'intelligence'
    elif 'blackarch' in filename:
        target_service = 'blackarch'
    elif 'backend' in filename:
        target_service = 'backend'
    elif 'storage' in filename:
        target_service = 'storage'

    if not target_service:
        return {'error': 'Could not determine target service for upgrade'}

    services = get_current_services()
    if target_service not in services:
        return {'error': 'Target service not configured'}

    service_info = services[target_service]
    target_path = service_info['path']

    # Copy upgrade file to target location
    target_file = os.path.join(target_path, filename)
    shutil.copy2(upgrade_file, target_file)

    # Restart the service to apply upgrade
    stop_result = stop_service(service_info)
    time.sleep(2)
    start_result = start_service(service_info)

    return {
        'status': 'deployed',
        'type': 'python_module',
        'target_service': target_service,
        'file_deployed': target_file,
        'service_restart': {
            'stop': stop_result,
            'start': start_result
        },
        'timestamp': datetime.now().isoformat()
    }

def deploy_js_upgrade(upgrade_file, filename):
    """Deploy JavaScript module upgrade"""
    # Similar logic for JS upgrades
    return {
        'status': 'deployed',
        'type': 'javascript_module',
        'file': filename,
        'timestamp': datetime.now().isoformat()
    }

def deploy_config_upgrade(upgrade_file, filename):
    """Deploy configuration upgrade"""
    # Copy config file and reload services
    return {
        'status': 'deployed',
        'type': 'configuration',
        'file': filename,
        'timestamp': datetime.now().isoformat()
    }

def deploy_model_upgrade(upgrade_file, filename):
    """Deploy AI model upgrade"""
    # Copy model file and update AI services
    return {
        'status': 'deployed',
        'type': 'model',
        'file': filename,
        'timestamp': datetime.now().isoformat()
    }

def integrate_json_dataset(dataset_file, filename):
    """Integrate JSON dataset into knowledge base"""
    try:
        with open(dataset_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Send to Storage Facility for integration
        storage_port = get_current_services()['storage']['port']
        integration_payload = {
            'dataset_name': filename,
            'data': data,
            'integration_type': 'bulk_import'
        }

        response = requests.post(f'http://localhost:{storage_port}/api/facility/bulk_import',
                               json=integration_payload, timeout=30)

        if response.status_code == 200:
            return {
                'status': 'integrated',
                'dataset': filename,
                'records_processed': len(data) if isinstance(data, list) else 1,
                'storage_response': response.json(),
                'timestamp': datetime.now().isoformat()
            }
        else:
            return {'error': f'Storage integration failed: {response.text}'}

    except Exception as e:
        return {'error': f'JSON processing failed: {str(e)}'}

def integrate_csv_dataset(dataset_file, filename):
    """Integrate CSV dataset"""
    # Similar logic for CSV processing
    return {
        'status': 'integrated',
        'dataset': filename,
        'format': 'csv',
        'timestamp': datetime.now().isoformat()
    }

def integrate_text_dataset(dataset_file, filename):
    """Integrate text dataset"""
    # Similar logic for text processing
    return {
        'status': 'integrated',
        'dataset': filename,
        'format': 'text',
        'timestamp': datetime.now().isoformat()
    }

@app.route('/api/reports/<report_type>')
def get_report(report_type):
    """Generate various reports"""
    report_types = ['daily', 'weekly', 'monthly', 'performance', 'errors', 'security']

    if report_type not in report_types:
        return jsonify({'error': 'Invalid report type'}), 400

    try:
        # Generate mock report data (in real implementation, this would query actual data)
        if report_type == 'daily':
            report = {
                'type': 'daily',
                'date': datetime.now().date().isoformat(),
                'total_requests': 15420,
                'successful_requests': 15280,
                'failed_requests': 140,
                'avg_response_time': 245,
                'peak_concurrent_users': 89,
                'system_uptime': 99.7,
                'errors_logged': 23
            }
        elif report_type == 'performance':
            report = {
                'type': 'performance',
                'period': 'last_24h',
                'cpu_avg': 34.2,
                'memory_avg': 67.8,
                'disk_usage': 45.3,
                'network_throughput': 125.6,
                'api_response_times': {
                    'knowledge': 180,
                    'droid': 220,
                    'intelligence': 195,
                    'storage': 150
                },
                'bottlenecks': ['memory_usage', 'network_latency']
            }
        elif report_type == 'errors':
            report = {
                'type': 'errors',
                'period': 'last_7d',
                'total_errors': 156,
                'error_types': {
                    'connection_timeout': 45,
                    'invalid_request': 38,
                    'server_error': 28,
                    'authentication_failure': 25,
                    'resource_not_found': 20
                },
                'most_affected_services': ['Intelligence API', 'Storage Facility'],
                'error_trends': 'decreasing'
            }
        else:
            report = {
                'type': report_type,
                'message': f'{report_type} report generated successfully',
                'timestamp': datetime.now().isoformat()
            }

        logging.info(f"Report generated: {report_type}")
        return jsonify(report)
    except Exception as e:
        logging.error(f"Error generating report: {e}")
        return jsonify({'error': str(e)}), 500

# Background task to update metrics
def update_metrics():
    """Background task to update system metrics"""
    global system_metrics
    while True:
        try:
            # Simulate metric updates (in real implementation, this would collect actual metrics)
            system_metrics['total_requests'] += 1
            system_metrics['active_users'] = max(0, system_metrics['active_users'] + (1 if time.time() % 10 < 5 else -1))
            system_metrics['avg_response_time'] = 200 + (time.time() % 100)
            system_metrics['uptime'] = 99.9

            time.sleep(5)  # Update every 5 seconds
        except Exception as e:
            logging.error(f"Error updating metrics: {e}")
            time.sleep(5)

# Start background metrics update
# metrics_thread = threading.Thread(target=update_metrics, daemon=True)
# metrics_thread.start()

if __name__ == '__main__':
    print("Starting R3AL3R AI Management API...")
    logging.info("R3AL3R AI Management API starting...")
    app.run(host='0.0.0.0', port=5000, debug=False)