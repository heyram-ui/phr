import sqlite3

def fix_db():
    conn = sqlite3.connect('health.db')
    c = conn.cursor()
    
    print("Fixing database schema...")

    # Feedback Table (V5)
    try:
        c.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT,
                rating INTEGER,
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        print("Feedback table created/verified.")
    except Exception as e:
        print(f"Error creating Feedback: {e}")

    # Check for emergency_contact in users
    try:
        c.execute("SELECT emergency_contact FROM users LIMIT 1")
    except sqlite3.OperationalError:
        print("Adding emergency_contact column...")
        c.execute("ALTER TABLE users ADD COLUMN emergency_contact TEXT")

    conn.commit()
    conn.close()
    print("Database fixed successfully.")

if __name__ == '__main__':
    fix_db()
