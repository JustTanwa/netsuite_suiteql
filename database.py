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

def update_lesson(lesson_id, title=None, description=None, content=None):
    """
    Updates a lesson in the SQLite database based on the provided fields.

    Parameters:
        lesson_id (int): The ID of the lesson to update.
        title (str): New title for the lesson (optional).
        description (str): New description (optional).
        content (str): New HTML content (optional).
        goal (str): New goal (optional).
    """
    fields = []
    values = []

    if title is not None:
        fields.append("lesson_name = ?")
        values.append(title)
    if description is not None:
        fields.append("lesson_description = ?")
        values.append(description)
    if content is not None:
        fields.append("lesson_content = ?")
        values.append(content)

    if not fields:
        raise ValueError("No fields to update.")

    values.append(lesson_id)

    query = f"""
    UPDATE lessons
    SET {', '.join(fields)}
    WHERE id = ?
    """

    conn = sqlite3.connect("lessons.db")  # Adjust path as needed
    cursor = conn.cursor()
    cursor.execute(query, values)
    conn.commit()
    conn.close()