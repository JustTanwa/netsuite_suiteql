import sqlite3
def create_lesson(name, description, content):
    conn = sqlite3.connect("lessons.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO lessons (lesson_name, lesson_description, lesson_content)
        VALUES (?, ?, ?)
    """, (
        name,
        description,
        content
    ))
    conn.commit()
    conn.close()

def get_lessons(lesson_id = None):
    conn = sqlite3.connect("lessons.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    if not lesson_id:
        cursor.execute("SELECT * FROM lessons")
    else:
        cursor.execute("SELECT * FROM lessons WHERE id = ?", [lesson_id])
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
    