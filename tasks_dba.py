from Assignment import Assignment
from Task import Task
from courses_dba import get_course_by_id
from db_connect import get_connection
from student import Student
from Course import Course
from student_dba import conn, get_student_by_id


def get_tasks_by_course_id(course_id) -> list:
    # Сначала получить объект класса Course (если это возможно)
    # Затем получить много объектов класса Task и в каждой занести ссылку на ранее полученный курс
    course = get_course_by_id(course_id)
    if course is None:
        raise Exception("Course not found")
    conn = get_connection()
    q = f"""select t.id, t.task_name,t.content,t.solution_example,t.course_id
            from task t                      
            where course_id={course_id}"""

    with conn.cursor() as cur:
        cur.execute(q)
        rows = cur.fetchall()
        if rows is None:
            return []

        tasks = []

        for row in rows:
            task = Task(row[0], row[1], row[2], row[3], course)
            tasks.append(task)
        return tasks


def get_tasks_by_id(id) -> Task:
    conn = get_connection()
    q = f"""select t.id, t.task_name,t.content,t.solution_example,t.course_id,c.name
            from task t join courses c on t.course_id=c.id                
            where t.id={id}"""

    with conn.cursor() as cur:
        cur.execute(q)
        row = cur.fetchone()
        if row is None:
            return None

    course = Course(row[4], row[5])
    task = Task(row[0], row[1], row[2], row[3], course)

    return task


def add_task(new_task: Task) -> Task | None:
    conn = get_connection()
    q = f"""insert into task (task_name,content,solution_example,course_id)
        values( '{new_task.task_name}', '{new_task.content}', '{new_task.solution_example}', {new_task.course.id})
        returning id ;"""  #

    with conn.cursor() as cur:
        cur.execute(q)
        row = cur.fetchone()
        conn.commit()
        if row is not None:
            return Task(row[0], new_task.task_name, new_task.content, new_task.solution_example, new_task.course)
    return None


def delete_task(old_task_id: int) -> Task | None:
    deleted_task = get_tasks_by_id(old_task_id)
    print(deleted_task)
    if deleted_task is not None:
        q = f"""delete from task 
                 where id = {old_task_id};"""
        with conn.cursor() as cur:
            cur.execute(q)
            conn.commit()

    return deleted_task


def task_update(old_task: Task, new_task: Task) -> Task | None:
    q = (f"""update task
            set task_name = N'{new_task.task_name}'
            and content = {new_task.content}
            and solution_example = {new_task.solution_example} 
            where id = {new_task.id};""")
    with conn.cursor() as cur:
        cur.execute(q)
        conn.commit()

    return get_tasks_by_id(new_task.id)
