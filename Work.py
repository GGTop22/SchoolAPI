from Course import Course
from Task import Task
from student import Student


class Work:
    id: int
    student: Student
    task: Task
    solution: str
    comment: str
    submit_time: str
    mark: int


    def __init__(self, id, student, task, solution, comment, submit_time,mark=None):
        self.id = id
        self.student = student
        self.task = task
        self.solution = solution
        self.comment = comment
        self.mark = mark
        self.submit_time = submit_time

    def set_mark(self, mark):
        if mark >= 0 and mark <= 7:
            self.mark = mark

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'student': self.student.to_dict(),
            'task': self.task.to_dict(),
            'solution': self.solution,
            'comment': self.comment,
            'mark': self.mark,
            'submit_time': self.submit_time
        }

    def __str__(self):
        return 'Task' + str(self.to_dict())

    def __repr__(self):
        return self.__str__()