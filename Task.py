from Course import Course



class Task:
    id: int
    task_name: str
    content: str
    solution_example: str
    course: Course

    def __init__(self, id, task_name, content, solution_example, course):
        self.id = id
        self.task_name = task_name
        self.content = content
        self.solution_example = solution_example
        self.course = course
        # if progress < 0 or progress > 100:
        #     raise ValueError("progress should be between 0 and 100")

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'task_name': self.task_name,
            'content': self.content,
            'solution_example': self.solution_example,
            'course': self.course.to_dict()
        }

    def __str__(self):
        return 'Task' + str(self.to_dict())

    def __repr__(self):
        return self.__str__()
