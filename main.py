from datetime import datetime

from flask import Flask, jsonify, request

from Assignment import Assignment
from Course import Course
from Task import Task
from Work import Work
from assignments_dba import get_assignment, add_assignment, rewrite_progress, delete_assignment
from courses_dba import get_course_and_tasks_by_id, get_course_by_id, get_all_courses, make_course, rename_course, \
    delete_course
from db_connect import get_connection
from student import Student
from student_dba import make_student, rename_student, get_all_students, get_student_by_id, delete_student
from tasks_dba import get_tasks_by_course_id, get_tasks_by_id, add_task, delete_task
from work_dba import get_work_by_id, add_work, delete_work

app = Flask(__name__)


@app.get('/students')
def get_students():
    students = get_all_students()
    students_2 = [r.to_dict() for r in students]
    return jsonify(students_2)


@app.route('/students', methods=['POST'])
def create_student():
    id = 0
    fio = request.get_json()['fio']
    tmp_student = Student(id, fio)
    added_student = make_student(tmp_student)

    return jsonify({
        "message": "Student created",
        "fio": fio,
        "id": added_student.id
    })


@app.route('/students/<int:id>', methods=['GET'])
def get_student(id: int):
    student = get_student_by_id(id)
    if student is None:
        return jsonify({'message': 'Student Not Found'}), 404
    return jsonify(student.to_dict())


@app.put('/students/<int:id>')
def edit_student(id: int):
    fio = request.get_json()['fio']
    tmp_student = Student(id, fio)
    edited_student = rename_student(tmp_student)
    if edited_student is None:
        return jsonify({'message': 'Reader Not Found'}), 404
    return jsonify(edited_student.to_dict())


# @app.route('/courses', methods=['GET'])
# def add_course():
#
#     id = request.get_json()['id']
#     name = request.get_json()['name']
#     tmp_reader = course(id, name)
#     added_reader = create_reader(tmp_reader)
#     return jsonify(added_reader.to_dict())

@app.get('/course_with_tasks/<int:id>')
def get_course_with_tasks(id):
    course = get_course_and_tasks_by_id(id)
    if course is None:
        return jsonify({'message': 'Course Not Found'}), 404
    return jsonify(course)


@app.get('/courses/<int:id>')
def get_course(id):
    course = get_course_by_id(id)
    if course is None:
        return jsonify({'message': 'Course Not Found'}), 404
    return jsonify(course.to_dict())


@app.get('/courses')
def get_courses():
    courses = get_all_courses()
    courses_2 = [r.to_dict() for r in courses]
    return jsonify(courses_2)


@app.post('/courses')
def create_course():
    id = 0
    name = request.get_json()['name']
    tmp_course = Course(id, name)
    added_course = make_course(tmp_course)

    return jsonify({
        "message": "Course created",
        "name": name,
        "id": added_course.id
    })


@app.put('/courses/<int:id>')
def edit_course(id: int):
    name = request.get_json()['name']
    tmp_course = Course(id, name)
    edited_course = rename_course(tmp_course)
    if edited_course is None:
        return jsonify({'message': 'Course Not Found'}), 404
    return jsonify(edited_course.to_dict())


@app.get('/assignments')
def get_assignments():
    student_id = request.args.get('student_id')
    course_id = request.args.get('course_id')
    assignment = get_assignment(student_id, course_id)
    if assignment is None:
        return jsonify({'message': 'Assignment Not Found'}), 404
    return jsonify(assignment.to_dict())


@app.put('/assignments')  # Разобраться что на входе (смотри блокнот 12 Тест )
def edit_assignment():
    student_id = request.get_json()['student_id']
    course_id = request.get_json()['course_id']
    progress = request.get_json()['progress']
    tmp_stud = Student(student_id, '')
    tmp_course = Course(course_id, '')
    try:
        tmp_as = Assignment(tmp_stud, tmp_course, progress)
        edited_assignment = rewrite_progress(tmp_as)

        if edited_assignment is None:
            return jsonify({'message': 'Assignment Not Found'}), 404
        return jsonify(edited_assignment.to_dict())
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@app.post('/assignments')
def add_student_to_course():
    student_id = request.get_json()['student_id']
    course_id = request.get_json()['course_id']
    assignment = get_assignment(student_id, course_id)
    if assignment is None:
        # добавить assignment в базу данных
        course = get_course_by_id(course_id)
        if course is None:
            return jsonify({'message': 'Course Not Found'}), 404
        student = get_student_by_id(student_id)
        if student is None:
            return jsonify({'message': 'Student Not Found'}), 404
        new_assignment = Assignment(student, course, progress=0)
        add_assignment(new_assignment)
        return jsonify(new_assignment.to_dict())
    else:
        return jsonify({'message': 'Unable to add Student to the course (already included)'}), 403


@app.delete('/courses/<int:id>')
def del_course(id: int):
    try:
        deleted_course = delete_course(id)
        if deleted_course is None:
            return jsonify({'message': 'Course Not Found'}), 404
        return jsonify(deleted_course.to_dict())
    except Exception as e:
        return jsonify({'message': 'Unable to delete this course'}), 403


@app.delete('/students/<int:id>')
def del_student(id: int):
    try:
        deleted_student = delete_student(id)
        if deleted_student is None:
            return jsonify({'message': 'Student Not Found'}), 404
        return jsonify(deleted_student.to_dict())
    except Exception as e:
        return jsonify({'message': 'Unable to delete this student'}), 403


@app.delete('/assignments')
def del_assignment():
    student_id = request.get_json()['student_id']
    course_id = request.get_json()['course_id']
    progress = 100
    tmp_stud = Student(student_id, '')
    tmp_course = Course(course_id, '')
    try:
        tmp_as = Assignment(tmp_stud, tmp_course, progress)
        deleted_assignment = delete_assignment(tmp_as)

        if deleted_assignment is None:
            return jsonify({'message': 'Assignment Not Found'}), 404
        return jsonify({"message": "Student removed from course"})
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@app.get('/tasks/course/<int:id>')
def get_tasks_by_course(id: int):
    try:
        tasks_list = get_tasks_by_course_id(id)
    except Exception as e:
        return jsonify({'message': str(e)}), 404
    if tasks_list is None:
        return jsonify({'message': 'Course has no tasks'}), 404
    tasks_2 = [t.to_dict() for t in tasks_list]
    return jsonify(tasks_2)


@app.get('/tasks/<int:id>')
def get_one_task(id: int):
    task = get_tasks_by_id(id)
    if task is None:
        return jsonify({'message': 'Task Not Found'}), 404
    return jsonify(task.to_dict())


@app.post('/tasks')
def create_task():
    task_id = 0
    if "task_name" not in request.json:
        return jsonify({'message': 'Invalid data'}), 400
    task_name = request.get_json()['task_name']
    if "content" not in request.json:
        return jsonify({'message': 'Invalid data'}), 400
    task_contents = request.get_json()['content']
    if "solution_example" not in request.json:
        return jsonify({'message': 'Invalid data'}), 400
    task_solution_example = request.get_json()['solution_example']
    if "course_id" not in request.json:
        return jsonify({'message': 'Invalid data'}), 400
    task_course_id = request.get_json()['course_id']
    course = get_course_by_id(task_course_id)
    if course is None:
        return jsonify({'message': 'Course Not Found'}), 404
    new_task = Task(task_id, task_name, task_contents, task_solution_example, course)
    added_task = add_task(new_task)
    return jsonify(added_task.to_dict())


@app.put('/tasks/<int:id>')
def update_task(id: int):
    task_name = request.get_json()['task_name']
    content = request.get_json()['content']
    solution_example = request.get_json()['solution_example']
    try:
        edited_task = update_task(task_name, content, solution_example)

        if edited_task is None:
            return jsonify({'message': 'Task Not Found'}), 404
        return jsonify(edited_task.to_dict())
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@app.delete('/tasks/<int:id>')
def remove_task(id: int):
    try:
        deleted_task = delete_task(id)
        if deleted_task is None:
            return jsonify({'message': 'Task Not Found'}), 404
        return jsonify(deleted_task.to_dict())
    except Exception as e:
        return jsonify({'message': 'Unable to delete this task'}), 403


@app.get('/work/<int:id>')
def get_one_work(id: int):
    work = get_work_by_id(id)
    if work is None:
        return jsonify({'message': 'Work Not Found'}), 404
    return jsonify(work.to_dict())


@app.post('/work')
def create_work():
    work_id = 0
    if "student_id" not in request.json:
        return jsonify({'message': 'Invalid data'}), 400
    student_id = request.get_json()['student_id']
    if "task_id" not in request.json:
        return jsonify({'message': 'Invalid data'}), 400
    task_id = request.get_json()['task_id']
    if "solution" not in request.json:
        return jsonify({'message': 'Invalid data'}), 400
    solution = request.get_json()['solution']
    if "comment" not in request.json:
        return jsonify({'message': 'Invalid data'}), 400
    comment = request.get_json()['comment']
    if "submit_time" not in request.json:
        return jsonify({'message': 'Invalid data'}), 400
    submit_time = request.get_json()['submit_time']
    if "mark" not in request.json:
        return jsonify({'message': 'Invalid data'}), 400
    mark = request.get_json()['mark']
    task = get_tasks_by_id(task_id)
    if task is None:
        return jsonify({'message': 'Task Not Found'}), 404
    student = get_student_by_id(student_id)
    if student is None:
        return jsonify({'message': 'Student Not Found'}), 404
    new_work = Work(work_id, student, task, solution, comment, submit_time, mark)
    added_work = add_work(new_work)
    return jsonify(added_work.to_dict())


@app.delete('/work/<int:id>')
def remove_work(id: int):
    try:
        deleted_work = delete_work(id)
        if deleted_work is None:
            return jsonify({'message': 'Work Not Found'}), 404
        return jsonify(deleted_work.to_dict())
    except Exception as e:
        return jsonify({'message': 'Unable to delete this work'}), 403


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
    conn = get_connection()
    cursor = conn.cursor()

    # @app.delete('/task')
    # def del_task():
