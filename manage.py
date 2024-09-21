import psycopg2
import os
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()

    # Database connection parameters
    db_params = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT')
    }

    try:
        # Connect to the database
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Get the current user's name
        cur.execute("SELECT current_user;")
        current_user = cur.fetchone()[0]

        # Check connection limit
        cur.execute("SELECT rolname, rolconnlimit FROM pg_roles WHERE rolname = %s;", (current_user,))
        role_info = cur.fetchone()

        if role_info:
            print(f"User: {role_info[0]}")
            print(f"Connection limit: {role_info[1]}")
            if role_info[1] < 100:  # Assuming 100 is a reasonable threshold
                print("Warning: Connection limit is set to a low value. Consider contacting your database provider to increase this limit.")
        else:
            print(f"No role information found for user: {current_user}")

        # Terminate idle connections
        cur.execute("""
            SELECT pg_terminate_backend(pid) 
            FROM pg_stat_activity 
            WHERE usename = %s AND state = 'idle';
        """, (current_user,))
        
        terminated_connections = cur.rowcount
        print(f"Terminated {terminated_connections} idle connection(s).")

        # Commit changes and close connection
        conn.commit()
        cur.close()
        conn.close()

    except psycopg2.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()