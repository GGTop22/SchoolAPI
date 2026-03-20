class Course:
    id: int
    name: str

    def __init__(self, id, name):
        self.id = id
        self.name=name

    def to_dict(self)-> dict:
        return {
            'id': self.id,
            'name': self.name
        }



    def __str__(self):
        return 'Course '+str(self.to_dict())

    def __repr__(self):
        return self.__str__()
