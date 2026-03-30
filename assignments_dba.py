from Assignment import Assignment
from db_connect import get_connection
from student import Student
from student_dba import conn
from Course import Course


def get_assignment(student_id, course_id) -> Assignment:
    conn = get_connection()
    q = f"""select s.id, s.fio, c.id, c.name, a.progress
            from assignments a join students s on s.id = a.student_id 
                               join courses c on c.id = a.course_id 
            where student_id={student_id} and course_id={course_id}"""

    with conn.cursor() as cur:
        cur.execute(q)
        row = cur.fetchone()
        if row is None:
            return None

        student_id, fio, course_id, name, progress = row

        return Assignment(Student(id=student_id, fio=fio), Course(id=course_id, name=name), progress=progress)


def add_assignment(new_assignment):
    conn = get_connection()
    q = f"""insert into assignments (student_id, course_id, progress) values({new_assignment.student.id}, {new_assignment.course.id}, {new_assignment.progress})"""  #
    with conn.cursor() as cur:
        cur.execute(q)
        conn.commit()
    return new_assignment


def rewrite_progress(new_assignment: Assignment) -> Assignment:
    q = (f"""update assignments
            set progress = {new_assignment.progress}
            where student_id = {new_assignment.student.id} and course_id = {new_assignment.course.id};""")
    with conn.cursor() as cur:
        cur.execute(q)
        conn.commit()

    return get_assignment(student_id=new_assignment.student.id, course_id=new_assignment.course.id)


def delete_assignment(old_assignment: Assignment):
    deleted_assignment = get_assignment(old_assignment.student.id, old_assignment.course.id)
    print(deleted_assignment)
    if deleted_assignment is not None:
        q = (f"""delete from assignments            
                where student_id = {old_assignment.student.id} and course_id = {old_assignment.course.id};""")
        with conn.cursor() as cur:
            cur.execute(q)
            conn.commit()

    return deleted_assignment
