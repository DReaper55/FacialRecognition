import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

from database.courses_db import insert, updateCourse
from database.registered_students_db import queryCount
from model.course import Course
from utils.course_registration_window import show_registration_window


def displayCourseInfo(isCreate, course=None):
    root = tk.Tk()
    root.title("Course")
    root.geometry("500x500")

    # Create a custom style for the label
    style = ttk.Style()
    style.configure("My.TLabel", background="#f0f0f0", borderradius=5)

    # Open the image file using PIL
    # image = Image.open(course.DisplayPicture)

    # Convert the image to a PhotoImage object
    # photo_image = ImageTk.PhotoImage(image)

    # Create the label widget to display the image
    # image_path = course.DisplayPicture
    # img = ImageTk.PhotoImage(Image.open(image_path))
    # image_label = ttk.Label(root, image=photo_image, style="My.TLabel")
    # image_label.pack(expand=True, fill='both')

    # Create the Course title label
    courseTitleLabel = ttk.Label(root, text="Course Title:")
    courseTitleLabel.grid(pady=10, padx=15, row=0, column=0)

    # Create the text box
    courseTitleTextbox = ttk.Entry(root)
    courseTitleTextbox.grid(row=0, column=1)

    if not isCreate:
        courseTitleTextbox.insert(0, course.courseTitle)

    # Create the course code label
    courseCodeLabel = ttk.Label(root, text="Course Code:")
    courseCodeLabel.grid(pady=10, padx=15, row=1, column=0)

    # Create the text box
    courseCodeTextbox = ttk.Entry(root)
    courseCodeTextbox.grid(row=1, column=1)

    if not isCreate:
        courseCodeTextbox.insert(0, course.courseCode)

    # Disable the textbox
    if not isCreate:
        courseCodeTextbox.config(state='disable')

    # Create the course Lecturer label
    courseLecturerLabel = ttk.Label(root, text="Course Lecturer:")
    courseLecturerLabel.grid(pady=10, padx=15, row=2, column=0)

    # Create the text box
    courseLecturerTextbox = ttk.Entry(root)
    courseLecturerTextbox.grid(row=2, column=1)

    if not isCreate:
        courseLecturerTextbox.insert(0, course.courseLecturer)

    # Course registration button
    course_reg_btn = ttk.Button(root, text="Register student", command=lambda: show_registration_window(course, True))
    course_reg_btn.grid(row=7, column=0)

# Create the save button
    save_button = tk.Button(root, text="Save", bg='blue', fg='white', command=lambda: saveCourse(
        courseTitleTextbox.get(), courseCodeTextbox.get(), courseLecturerTextbox.get(), isCreate
    ))
    save_button.grid(row=7, column=3)

    # Create the delete button
    delete_button = tk.Button(root, text="Delete", bg='red', fg='white', command=lambda: deleteCourse(course.Matric))

    # Hide delete button if creating new record
    if isCreate:
        delete_button.grid_forget()
    else:
        delete_button.grid(row=7, column=2)

#     Get number of registered students
    numberOfRegStudents = queryCount(course.courseCode)

    # Registered students button
    reg_students_btn = ttk.Button(root, text=f"{numberOfRegStudents} registered students",
                                  command=lambda: show_registration_window(course, False))
    reg_students_btn.grid(row=8, column=1)


def saveCourse(courseTitle, courseCode, courseLecturer, isCreate):
    course = Course(
        courseTitle=courseTitle,
        courseCode=courseCode,
        courseLecturer=courseLecturer,
    )

    if isCreate:
        insert(course)
    else:
        updateCourse(course)


def deleteCourse(courseCodeNumber):
    deleteCourse(courseCodeNumber)
