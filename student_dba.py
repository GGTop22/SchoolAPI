from db_connect import get_connection
from student import Student

conn = get_connection()

def get_all_students():
    q = 'select id,fio from students;'
    with conn.cursor() as cur:
        cur.execute(q)
        res = cur.fetchall()
        return [Student(r[0], r[1]) for r in res]


def get_student_by_id(id):
    q = f'select id,fio from students where id = {id};'
    with conn.cursor() as cur:
        cur.execute(q)
        r = cur.fetchone()
        if r is not None:
            return Student(r[0], r[1])
    return None

def make_student(new_student: Student) -> Student:
    q = f"insert into students(fio) values ('{new_student.fio}') returning id "
    with conn.cursor() as cur:
        cur.execute(q)
        r = cur.fetchone()
        conn.commit()

        if r is not None:
            return Student(r[0], new_student.fio)
    return None


def rename_student(new_student: Student) -> Student:
    q = (f"""update students
            set fio = N'{new_student.fio}' 
            where id = {new_student.id};""")
    with conn.cursor() as cur:
        cur.execute(q)
        conn.commit()

    return get_student_by_id(new_student.id)

def delete_student(id: int) -> Student:
    deleted_student = get_student_by_id(id)
    print(deleted_student)
    if deleted_student is not None:
        q = (f"""delete from students            
                where id = {id};""")
        with conn.cursor() as cur:
            cur.execute(q)
            conn.commit()

    return deleted_student

