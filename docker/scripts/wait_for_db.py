#!/usr/bin/env python3
import os
import sys
import time
import psycopg2

def wait_for_db():
    db_host = os.environ.get('POSTGRES_HOST', 'db')
    db_port = os.environ.get('POSTGRES_PORT', '5432')
    db_name = os.environ.get('POSTGRES_DB', 'django_db')
    db_user = os.environ.get('POSTGRES_USER', 'django_user')
    db_password = os.environ.get('POSTGRES_PASSWORD', '')
    
    print(f"Waiting for PostgreSQL at {db_host}:{db_port}...")
    
    for _ in range(30):
        try:
            conn = psycopg2.connect(
                host=db_host,
                port=db_port,
                dbname=db_name,
                user=db_user,
                password=db_password
            )
            conn.close()
            print("PostgreSQL is ready!")
            return True
        except psycopg2.OperationalError as e:
            print(f"Waiting for database... ({str(e)})")
            time.sleep(1)
    
    print("ERROR: Could not connect to PostgreSQL")
    return False

if __name__ == "__main__":
    if wait_for_db():
        sys.exit(0)
    else:
        sys.exit(1)

