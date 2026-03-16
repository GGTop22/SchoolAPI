from datetime import datetime

from flask import Flask, jsonify, request

from courses_dba import get_course_and_tasks_by_id, get_course_by_id
from db_connect import get_connection
from student import Student
from student_dba import make_student, rename_student, get_all_students, get_student_by_id

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
    return jsonify(course)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
    conn = get_connection()
    cursor = conn.cursor()
