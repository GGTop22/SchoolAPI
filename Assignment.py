from Course import Course
from student import Student


class Assignment:
    student: Student
    course: Course
    progress: float

    def __init__(self, student, course, progress):
        self.student = student
        self.course = course
        self.progress = progress

    def to_dict(self) -> dict:
        return {
            'student': self.student.to_dict(),
            'course': self.course.to_dict(),
            'progress': self.progress
        }

    def __str__(self):
        return 'Assignment' + str(self.to_dict())

    def __repr__(self):
        return self.__str__()
