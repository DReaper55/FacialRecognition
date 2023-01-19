import json

from bson import json_util
from pymongo import MongoClient

from model.attendance import Attendance

client = MongoClient("mongodb://localhost:27017/")
db = client["StudentRecord"]
myCollection = db["attendance"]


# Inserting a document
def insert(attendance):
    myCollection.insert_one(attendance.__dict__)


# Querying documents
def getAllAttendances():
    results = myCollection.find()

    attendances = []

    for result in results:
        data = json.loads(json_util.dumps(result))

        if data:
            attendance = Attendance(
                lectureId=data["lectureId"],
                courseCode=data["courseCode"],
                studentMatric=data["studentMatric"],
            )

            attendances.append(attendance)

    return attendances


def getOneAttendance(courseCode):
    results = myCollection.find({"courseCode": courseCode})

    attendances = []

    for result in results:
        data = json.loads(json_util.dumps(result))

        if data:
            attendance = Attendance(
                lectureId=data["lectureId"],
                courseCode=data["courseCode"],
                studentMatric=data["studentMatric"],
                dateTime=data["dateTime"],
            )

            attendances.append(attendance)

    return attendances


# Updating a document
def updateAttendance(attendance):
    myCollection.update_one({"lectureId": attendance.lectureId}, {"$set": attendance.__dict__})


#  Deleting a document
def delete(lectureId):
    myCollection.delete_one({"lectureId": lectureId})


# Count records in db
def queryCount(courseCode):
    return myCollection.count_documents({"courseCode": courseCode})
