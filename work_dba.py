from Course import Course
from Task import Task
from Work import Work
from db_connect import get_connection
from student import Student


def get_work_by_id(old_work_id: int) -> Work | None:
    conn = get_connection()
    q = f"""select w.id, w.student_id,w.task_id,w.solution,w.submit_time,w.mark,
                   t.id, t.task_name,t.content,t.solution_example,
                   t.course_id,c.name,s.id,s.fio
            from task t join courses c on t.course_id=c.id join work w on t.id=w.task_id join students s on (s.id=w.student_id)              
            where w.id={old_work_id}"""

    with conn.cursor() as cur:
        cur.execute(q)
        row = cur.fetchone()
        if row is None:
            return None

    course = Course(row[10], row[11])
    task = Task(row[6], row[7], row[8], row[9], course)
    student = Student(row[12], row[13])
    work = Work(row[0], student, task, row[3], row[4], row[5])

    return work


def add_work(new_work: Work) -> Work | None:
    conn = get_connection()
    q = f"""insert into work (student_id,task_id, solution, comment, submit_time,mark)
        values( {new_work.student.id}, {new_work.task.id}, '{new_work.solution}', '{new_work.comment}', '{new_work.submit_time}', {new_work.mark}) returning id;"""

    with conn.cursor() as cur:
        cur.execute(q)
        row = cur.fetchone()
        conn.commit()
        if row is not None:
            return Work(row[0], new_work.student, new_work.task, new_work.solution, new_work.comment,
                        new_work.submit_time, new_work.mark)
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
