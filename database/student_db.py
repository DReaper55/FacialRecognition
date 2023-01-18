import json

from bson import json_util
from pymongo import MongoClient

from model.student import Student

client = MongoClient("mongodb://localhost:27017/")
db = client["StudentRecord"]
myCollection = db["students"]


# Inserting a document
def insert(student):
    myCollection.insert_one(student.__dict__)


# Querying documents
def getAllStudents():
    results = myCollection.find()

    students = []

    for result in results:
        data = json.loads(json_util.dumps(result))

        if data:
            student = Student(
                Fullname=data["Fullname"],
                DisplayPicture=data["DisplayPicture"],
                Faculty=data["Faculty"],
                Gender=data["Gender"],
                Department=data["Department"],
                DateOfBirth=data["DateOfBirth"],
                Matric=data["Matric"],
                IsGottenIDCard=data["IsGottenIDCard"],
            )

            students.append(student)

    return students


def getOneStudent(matricNumber):
    result = myCollection.find_one({"Matric": matricNumber})
    data = json.loads(json_util.dumps(result))

    student = Student(
        Fullname=data["Fullname"],
        DisplayPicture=data["DisplayPicture"],
        Faculty=data["Faculty"],
        Gender=data["Gender"],
        Department=data["Department"],
        DateOfBirth=data["DateOfBirth"],
        Matric=data["Matric"],
        IsGottenIDCard=data["IsGottenIDCard"],
    )

    return student


# Updating a document
def updateStudent(student):
    myCollection.update_one({"Matric": student.Matric}, {"$set": student.__dict__})


#  Deleting a document
def delete(matricNumber):
    myCollection.delete_one({"Matric": matricNumber})


# Count records in db
def queryCount():
    result = myCollection.count_documents({})
    print(result)
