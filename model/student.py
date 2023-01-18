import dataclasses


@dataclasses.dataclass
class Student:
    def __init__(self, Fullname, Faculty, Department, Matric, Gender, DateOfBirth,
                 DisplayPicture, IsGottenIDCard):
        self.Faculty = Faculty
        self.Department = Department
        self.Matric = Matric
        self.Gender = Gender
        self.DateOfBirth = DateOfBirth
        self.DisplayPicture = DisplayPicture
        self.IsGottenIDCard = IsGottenIDCard
        self.Fullname = Fullname

    def from_dict(self):
        return {
            "Department": self.Department,
            "Faculty": self.Faculty,
            "Matric": self.Matric,
            "Gender": self.Gender,
            "DateOfBirth": self.DateOfBirth,
            "DisplayPicture": self.DisplayPicture,
            "IsGottenIDCard": self.IsGottenIDCard,
            "Fullname": self.Fullname,
        }
