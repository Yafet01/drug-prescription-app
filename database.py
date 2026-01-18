import sqlite3
import bcrypt
import argparse
from pathlib import Path
import streamlit as st

# Get project directory
PROJECT_DIR = Path(__file__).parent.absolute()

def load_model():
    """Load the ML model with caching."""
    model_path = PROJECT_DIR / "model_saved"
    if model_path.exists():
        try:
            import pickle
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            return model
        except Exception as e:
            st.error(f"Error loading model: {e}")
            return None
    else:
        st.error(f"Model file not found at {model_path}")
        return None

def create_connection():
    """Create a database connection with proper configuration."""
    try:
        db_path = PROJECT_DIR / "users.db"
        conn = sqlite3.connect(str(db_path), timeout=10.0)
        conn.execute("PRAGMA journal_mode=WAL")
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def create_table():
    """Create the users table if it doesn't exist."""
    conn = create_connection()
    if not conn:
        print("Failed to connect to database")
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash BLOB NOT NULL
            )
        ''')
        conn.commit()
        print("Users table created successfully")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
    finally:
        conn.close()

def add_user(username, password):
    """Add a new user with bcrypt password hashing."""
    conn = create_connection()
    if not conn:
        print("Failed to connect to database")
        return
    
    try:
        # Hash the password with bcrypt
        password_bytes = password.encode() if isinstance(password, str) else password
        password_hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        conn.commit()
        print(f"User '{username}' added successfully")
    except sqlite3.IntegrityError:
        print(f"Error: User '{username}' already exists")
    except Exception as e:
        print(f"Error adding user: {e}")
    finally:
        conn.close()

def main():
    """Initialize default users if running as main script."""
    parser = argparse.ArgumentParser(description='User management for Drug Prescription App')
    parser.add_argument('--add-user', nargs=2, metavar=('USERNAME', 'PASSWORD'), 
                        help='Add a new user')
    args = parser.parse_args()
    
    # Create table
    create_table()
    
    # Add default users
    print("Adding default users...")
    add_user("admin", "admin123")
    add_user("demo", "demo123")
    
    # Handle --add-user argument
    if args.add_user:
        username, password = args.add_user
        add_user(username, password)

if __name__ == "__main__":
    main()

