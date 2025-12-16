import psycopg2
from psycopg2.extras import RealDictCursor

try:
    conn = psycopg2.connect(
        host='localhost',
        database='r3aler_ai',
        user='r3aler_user_2025',
        password='password123',
        port=5432
    )
    cursor = conn.cursor()

    # Check specific domain schemas
    domains_to_check = ['physics_unit', 'chemistry_unit', 'biology_unit', 'mathematics_unit']

    for domain in domains_to_check:
        print(f'\nChecking schema: {domain}')

        try:
            # Get tables in this schema
            cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{domain}'")
            tables = cursor.fetchall()
            print(f'  Tables: {[t[0] for t in tables]}')

            if tables:
                for table_info in tables:
                    table_name = table_info[0]
                    print(f'  Checking table: {domain}.{table_name}')

                    try:
                        # Get table structure
                        cursor2 = conn.cursor()
                        cursor2.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = '{domain}' AND table_name = '{table_name}'")
                        columns = cursor2.fetchall()
                        print(f'    Columns: {[(col[0], col[1]) for col in columns]}')

                        # Count rows
                        cursor2.execute(f'SELECT COUNT(*) FROM {domain}."{table_name}"')
                        count = cursor2.fetchone()[0]
                        print(f'    Row count: {count}')

                        cursor2.close()
                    except Exception as e:
                        print(f'    Error checking table: {e}')
            else:
                print('  No tables found in this schema')

        except Exception as e:
            print(f'  Error checking schema: {e}')

    cursor.close()
    conn.close()

except Exception as e:
    print(f'Error: {e}')