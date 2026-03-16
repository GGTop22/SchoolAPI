from db_connect import get_connection


def get_course_and_tasks_by_id(id) -> dict:
    with get_connection() as conn:
        cur = conn.cursor()

        cur.execute(
            """
            SELECT id, name
            FROM courses
            WHERE id = %s
            """,
            (id,)
        )

        course_row = cur.fetchone()
        if course_row is None:
            return None

        id, name = course_row

        cur.execute(
            """
            SELECT t.id, t.task_name, t.content, t.course_id
            FROM task t
            WHERE t.course_id = %s
            """,
            (id,)
        )

        tasks = [{"id": row[0], "task_name": row[1], "content": row[2], "course_id": row[3]}
                 for row in cur.fetchall()]

        return {
            "id": id,
            "name": name,
            "tasks": tasks
        }


def get_course_by_id(id) -> dict:
    with get_connection() as conn:
        cur = conn.cursor()

        cur.execute(
            """
            SELECT id, name
            FROM courses
            WHERE id = %s
            """,
            (id,)
        )

        course_row = cur.fetchone()
        if course_row is None:
            return None

        id, name = course_row

        return {
            "id": id,
            "name": name,
        }
