import json

from bson import json_util
from pymongo import MongoClient

from model.registered_student import RegisteredStudent

client = MongoClient("mongodb://localhost:27017/")
db = client["StudentRecord"]
myCollection = db["registered_students"]


# Inserting a document
def insert(registeredStudent):
    myCollection.insert_one(registeredStudent.__dict__)


# Querying documents
def getAllRegisteredStudents():
    results = myCollection.find()

    registeredStudents = []

    for result in results:
        data = json.loads(json_util.dumps(result))

        registeredStudent = RegisteredStudent(
            courseCode=data["courseCode"],
            studentMatric=data["studentMatric"],
        )

        registeredStudents.append(registeredStudent)

    return registeredStudents


def getOneRegisteredStudent(courseCode):
    registeredStudents = []

    results = myCollection.find({"courseCode": courseCode})

    for result in results:
        data = json.loads(json_util.dumps(result))

        registeredStudent = RegisteredStudent(
            courseCode=data["courseCode"],
            studentMatric=data["studentMatric"],
        )

        registeredStudents.append(registeredStudent)

    return registeredStudents


# Updating a document
def updateRegisteredStudent(registeredStudent):
    myCollection.update_one({"studentMatric": registeredStudent.studentMatric}, {"$set": registeredStudent.__dict__})


#  Deleting a document
def delete(studentMatric):
    myCollection.delete_one({"studentMatric": studentMatric})


# Count records in db
def queryCount(courseCode):
    return myCollection.count_documents({"courseCode": courseCode})
