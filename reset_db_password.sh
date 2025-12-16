#!/bin/bash
# Reset R3ALER database user password

sudo -u postgres psql <<EOF
ALTER USER r3aler_user_2025 WITH PASSWORD 'postgres';
\q
EOF

echo "Password reset complete. Testing connection..."
PGPASSWORD='postgres' psql -U r3aler_user_2025 -d r3aler_ai -h localhost -c 'SELECT current_user;'
