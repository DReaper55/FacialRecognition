import json

from bson import json_util
from pymongo import MongoClient

from model.lecture import Lecture

client = MongoClient("mongodb://localhost:27017/")
db = client["StudentRecord"]
myCollection = db["lectures"]


# Inserting a document
def insert(lecture):
    myCollection.insert_one(lecture.__dict__)


# Querying documents
def getAllLectures():
    results = myCollection.find()

    lectures = []

    for result in results:
        data = json.loads(json_util.dumps(result))

        if data:
            lecture = Lecture(
                courseCode=data["courseCode"],
                courseTitle=data["courseTitle"],
                lectureId=data["lectureId"],
                startTime=data["startTime"],
                endTime=data["endTime"],
            )

            lectures.append(lecture)

    return lectures


def getOneLecture(lectureId):
    result = myCollection.find_one({"lectureId": lectureId})
    data = json.loads(json_util.dumps(result))

    lecture = Lecture(
        courseCode=data["courseCode"],
        courseTitle=data["courseTitle"],
        lectureId=data["lectureId"],
        startTime=data["startTime"],
        endTime=data["endTime"],
    )

    return lecture


# Updating a document
def updateLecture(lecture):
    myCollection.update_one({"lectureId": lecture.lectureId}, {"$set": lecture.__dict__})


#  Deleting a document
def delete(lectureId):
    myCollection.delete_one({"lectureId": lectureId})


# Count records in db
def queryCount():
    return myCollection.count_documents({})
