from Course import Course
from Task import Task
from Work import Work
from db_connect import get_connection
from student import Student


def get_work_by_id(old_work_id: int) -> Work | None:
    conn = get_connection()
    q = f"""select w.id, w.student_id,w.task_id,w.comment,w.solution,w.submit_time,w.mark,w.isArchived,
                   t.id, t.task_name,t.content,t.solution_example,
                   t.course_id,c.name,s.id,s.fio
            from task t join courses c on t.course_id=c.id join work w on t.id=w.task_id join students s on (s.id=w.student_id)              
            where w.id={old_work_id}"""

    with conn.cursor() as cur:
        cur.execute(q)
        row = cur.fetchone()
        if row is None:
            return None

    course = Course(row[11], row[12])
    task = Task(row[7], row[8], row[9], row[10], course)
    student = Student(row[13], row[14])
    # work = Work(row[0], student, task, row[3], row[4], row[5])
    work = Work(id = row[0], student = student, task = task, solution = row[4], submit_time = row[5], mark = row[6],comment= row[3])

    return work


def get_all_works() -> list[Work]:
    conn = get_connection()
    q = f"""select w.id, w.student_id,w.task_id,w.solution,w.submit_time,w.mark,w.isArchived,
                   t.id, t.task_name,t.content,t.solution_example,
                   t.course_id,c.name,s.id,s.fio
            from task t join courses c on t.course_id=c.id join work w on t.id=w.task_id join students s on (s.id=w.student_id)"""
    with conn.cursor() as cur:
        cur.execute(q)
        rows = cur.fetchall()
        if rows is None:
            return []
    return [Work(row[0], Student(row[12], row[13]), Task(row[6], row[7], row[8], row[9], Course(row[10], row[11])), row[3], row[4], row[5]) for row in rows]

def get_unmarked_works_by_course(course:Course) -> list[Work]:
    conn = get_connection()
    q = f"""select w.id, w.student_id,w.task_id,w.solution,w.submit_time,w.mark,w.isArchived,
                   t.id, t.task_name,t.content,t.solution_example,
                   t.course_id,c.name,s.id,s.fio
            from task t join courses c on t.course_id=c.id join work w on t.id=w.task_id join students s on (s.id=w.student_id) WHERE course_id = {course.id} and w.mark is null"""

    with conn.cursor() as cur:
        cur.execute(q)
        rows = cur.fetchall()
        if rows is None:
            return []
    return [Work(row[0], Student(row[12], row[13]), Task(row[6], row[7], row[8], row[9], Course(row[10], row[11])), row[3], row[4], row[5]) for row in rows]

def add_work(new_work: Work) -> Work | None:
    conn = get_connection()
    qq = f"""update work set isArchived = true where student_id = {new_work.student.id} and task_id = {new_work.task.id}"""
    if new_work.mark is None:
        q = f"""insert into work (student_id,task_id, solution, comment, submit_time,mark,isArchived)
        values( {new_work.student.id}, {new_work.task.id}, '{new_work.solution}', '{new_work.comment}', '{new_work.submit_time}',null,'{new_work.isArchived}') returning id;"""
    else:
        q = f"""insert into work (student_id,task_id, solution, comment, submit_time,mark,isArchived)
        values( {new_work.student.id}, {new_work.task.id}, '{new_work.solution}', '{new_work.comment}', '{new_work.submit_time}', {new_work.mark}),{new_work.isArchived}returning id;"""
    print(q)
    with conn.cursor() as cur:
        cur.execute(qq)
        cur.execute(q)
        row = cur.fetchone()
        conn.commit()
        if row is not None:
            return Work(row[0], new_work.student, new_work.task, new_work.solution, new_work.comment,
                        new_work.submit_time, new_work.mark, new_work.isArchived)
    return None


def delete_work(old_work_id: int) -> Work | None:
    conn = get_connection()
    deleted_work = get_work_by_id(old_work_id)
    print(deleted_work)
    if deleted_work is not None:
        q = f"""delete from work 
                 where id = {old_work_id};"""
        with conn.cursor() as cur:
            cur.execute(q)
            conn.commit()

    return deleted_work

def update_work(new_work: Work) -> Work | None:
    conn = get_connection()
    q = (f"""update work
            set solution = '{new_work.solution}' , comment = '{new_work.comment}' , submit_time = '{new_work.submit_time}', mark = {new_work.mark}
            where id = {new_work.id};""")
    with conn.cursor() as cur:
        cur.execute(q)
        conn.commit()
    return get_work_by_id(new_work.id)

def get_works_by_student_id(student_id: int) -> list[Work]:
    conn = get_connection()
    works = []
    q = f"""select w.id, w.student_id,w.task_id,w.solution,w.submit_time,w.mark,w.isArchived,
                   t.id, t.task_name,t.content,t.solution_example,
                   t.course_id,c.name,s.id,s.fio
            from task t join courses c on t.course_id=c.id join work w on t.id=w.task_id join students s on (s.id=w.student_id)
            where student_id = {student_id}"""
    with conn.cursor() as cur:
        cur.execute(q)
        rows = cur.fetchall()
        if rows is None:
            return []
        for row in rows:
            course = Course(row[10], row[11])
            task = Task(row[6], row[7], row[8], row[9], course)
            student = Student(row[12], row[13])
            work = Work(id = row[0], student = student, task = task, solution = row[4], submit_time = row[5], mark = row[6],comment= row[3])
            works.append(work)
    return works



