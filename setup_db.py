import sqlite3
conn = sqlite3.connect("lessons.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lesson_name TEXT NOT NULL,
    lesson_description TEXT,
    lesson_content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()