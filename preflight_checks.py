#!/usr/bin/env python3
"""Preflight checks for R3AL3R AI production startup
Performs: syntax/compile checks, import smoke tests, DB connectivity, cloud storage init check.
"""
import py_compile, traceback, sys, json, os

print('→ Syntax check:')
files = ['r3aler_ai_response_generator.py','response_generator.py','ai_benchmarks.py']
ok = True
for f in files:
    try:
        py_compile.compile(f, doraise=True)
        print('  [OK] ', f)
    except Exception as e:
        ok = False
        print('  [ERR]', f, '->', e)

print('\n→ Import & smoke tests:')
try:
    import importlib
    importlib.invalidate_caches()
    mod_ai = importlib.import_module('R3AL3R_AI')
    mod_rg = importlib.import_module('r3aler_ai_response_generator')
    mod_rg_cls = getattr(mod_rg, 'R3AL3R_ResponseGenerator', None)
    print('  [OK] Imported R3AL3R_AI and RGIA class present:', bool(mod_rg_cls))
except Exception:
    ok = False
    print('  [ERR] Import error:')
    traceback.print_exc()

print('\n→ DB connectivity check (uses .env if present):')
try:
    from dotenv import load_dotenv
    load_dotenv()
    import psycopg2
    DB_CONFIG = {
        'host': os.environ.get('DB_HOST', '127.0.0.1'),
        'port': int(os.environ.get('DB_PORT', '5432')),
        'database': os.environ.get('DB_NAME', 'r3aler_ai'),
        'user': os.environ.get('DB_USER', 'r3aler_user_2025'),
        'password': os.environ.get('DB_PASSWORD', 'password123')
    }
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.close()
        print('  [OK] DB connection successful')
    except Exception as e:
        ok = False
        print('  [WARN] DB connection failed:', e)
except Exception as e:
    ok = False
    print('  [WARN] psycopg2 or dotenv not available or failed:', e)

print('\n→ Cloud storage / R3AL3R Storage Facility check:')
try:
    from AI_Core_Worker.R3AL3R_AI import R3AL3R_AI
    ai = R3AL3R_AI()
    if hasattr(ai, 'get_system_status'):
        status = ai.get_system_status()
        print('  [OK] R3AL3R_AI get_system_status returned keys:', list(status.get('components', {}).keys())[:6])
    else:
        print('  [OK] R3AL3R_AI instantiated (no get_system_status method)')
except Exception:
    ok = False
    print('  [ERR] Cloud storage / AI init error:')
    traceback.print_exc()

print('\n→ PRELIGHT SUMMARY:')
print('  All checks passed' if ok else '  Some checks failed or warned — review output above')
if not ok:
    sys.exit(2)
else:
    sys.exit(0)
