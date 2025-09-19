import sqlite3
from pathlib import Path
import hashlib
import os

class Database:
    def __init__(self):
        base_dir = Path(__file__).resolve().parent.parent.parent
        self.db_path = base_dir / 'database' / 'agritech.db'
        self.schema_path = base_dir / 'database' / 'schema.sql'
        print(f"Database path: {self.db_path}")
        print(f"Schema path: {self.schema_path}")
        
        # Ensure database directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self.init_db()

    def get_db_connection(self):
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        if not self.db_path.exists():
            conn = self.get_db_connection()
            with open(self.schema_path, 'r') as f:
                conn.executescript(f.read())
            
            # Add default user
            self.create_user('mahesha@gmail.com', 'm@123', 'Mahesh')
            conn.close()

    def hash_password(self, password):
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                     salt, 100000)
        pwdhash = hashlib.sha256(pwdhash).hexdigest()
        return (salt + pwdhash.encode('ascii')).decode('ascii')

    def verify_password(self, stored_password, provided_password):
        """Verify a stored password against one provided by user"""
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                     provided_password.encode('utf-8'), 
                                     salt.encode('ascii'), 
                                     100000)
        pwdhash = hashlib.sha256(pwdhash).hexdigest()
        return pwdhash == stored_password

    def create_user(self, email, password, name=None):
        """Create a new user."""
        conn = self.get_db_connection()
        try:
            hashed_password = self.hash_password(password)
            conn.execute(
                'INSERT INTO users (email, password, name) VALUES (?, ?, ?)',
                (email, hashed_password, name)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def verify_user(self, email, password):
        """Verify user credentials."""
        conn = self.get_db_connection()
        try:
            user = conn.execute(
                'SELECT * FROM users WHERE email = ?',
                (email,)
            ).fetchone()

            if user and self.verify_password(user['password'], password):
                return {'id': user['id'], 'email': user['email'], 'name': user['name']}
            return None
        finally:
            conn.close()