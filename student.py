class Student:
    id: int
    fio: str

    def __init__(self, id, fio):
        self.id = id
        self.fio=fio

    def to_dict(self)-> dict:
        return {
            'id': self.id,
            'fio': self.fio
        }



    def __str__(self):
        return 'Student '+str(self.to_dict())

    def __repr__(self):
        return self.__str__()
