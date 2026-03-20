from Course import Course
from db_connect import get_connection
from student_dba import conn


def get_all_courses():
    q = 'select id,name from courses;'
    with conn.cursor() as cur:
        cur.execute(q)
        res = cur.fetchall()
        return [Course(r[0], r[1]) for r in res]


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


def get_course_by_id(id) -> Course:
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

        return Course(id, name)


def make_course(new_course: Course) -> Course:
    q = f"insert into courses(name) values ('{new_course.name}') returning id "
    with conn.cursor() as cur:
        cur.execute(q)
        r = cur.fetchone()
        conn.commit()

        if r is not None:
            return Course(r[0], new_course.name)
    return None


def rename_course(new_course: Course) -> Course:
    q = (f"""update courses
            set name = N'{new_course.name}' 
            where id = {new_course.id};""")
    with conn.cursor() as cur:
        cur.execute(q)
        conn.commit()

    return get_course_by_id(new_course.id)
