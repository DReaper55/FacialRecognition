import json

from bson import json_util
from pymongo import MongoClient

from model.course import Course

client = MongoClient("mongodb://localhost:27017/")
db = client["StudentRecord"]
myCollection = db["courses"]


# Inserting a document
def insert(course):
    myCollection.insert_one(course.__dict__)


# Querying documents
def getAllCourses():
    results = myCollection.find()

    courses = []

    for result in results:
        data = json.loads(json_util.dumps(result))

        if data:
            course = Course(
                courseCode=data["courseCode"],
                courseLecturer=data["courseLecturer"],
                courseTitle=data["courseTitle"],
            )

            courses.append(course)

    return courses


def getOneCourse(courseCode):
    result = myCollection.find_one({"courseCode": courseCode})
    data = json.loads(json_util.dumps(result))

    course = Course(
        courseCode=data["courseCode"],
        courseLecturer=data["courseLecturer"],
        courseTitle=data["courseTitle"],
    )

    return course


# Updating a document
def updateCourse(course):
    myCollection.update_one({"courseCode": course.courseCode}, {"$set": course.__dict__})


#  Deleting a document
def delete(courseCode):
    myCollection.delete_one({"courseCode": courseCode})


# Count records in db
def queryCount():
    return myCollection.count_documents()
