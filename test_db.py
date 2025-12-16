import psycopg2

try:
    conn = psycopg2.connect(
        host='127.0.0.1',
        port=5432,
        database='r3aler_ai',
        user='r3aler_user_2025',
        password='Hughe$1816247365492924002'
    )
    print('Database connection successful!')
    conn.close()
except Exception as e:
    print(f'Database connection failed: {e}')