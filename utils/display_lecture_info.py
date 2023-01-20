import tkinter as tk
from datetime import datetime
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry

import secrets

from tktimepicker import SpinTimePickerModern
from tktimepicker import constants

from database.attendance_db import queryCount
from database.registered_students_db import queryCount as qc
from database.courses_db import getAllCourses
from database.lectures_db import insert, updateLecture, delete
from model.lecture import Lecture
from utils.attendance_window import show_attendance_window


def displayAttendanceWindow(lecture, root):
    root.destroy()
    show_attendance_window(lecture, True)


def displayLectureInfo(isCreate, lecture=None):
    root = tk.Tk()
    root.title("Lecture")
    root.geometry("500x500")

    # Create a custom style for the label
    style = ttk.Style()
    style.configure("My.TLabel", background="#f0f0f0", borderradius=5)

    # Get all courses for drop-down menu
    courses = getAllCourses()

    # Create a variable to store the selected option
    selected_option = tk.StringVar()

    # Create new list of just course code and title
    newCourseList = []

    # Add courses to drop-down menu
    for course in courses:
        new_item = f"{course.courseCode}, {course.courseTitle}"
        newCourseList.append(new_item)

    # todo: also set lecture values for update

    # Create the drop-down menu
    dropdown = ttk.OptionMenu(root, selected_option, "", *newCourseList)
    dropdown.grid(row=0, column=1)

    # Create the drop-down menu label
    courseSelectorLabel = ttk.Label(root, text="Select Course:")
    courseSelectorLabel.grid(pady=10, padx=15, row=0, column=0)

    # Create the start date label
    startDateTimeLabel = ttk.Label(root, text="Start Date:")
    startDateTimeLabel.grid(pady=10, padx=15, row=1, column=0)

    # Create the start-date entry widget
    startDatePicker = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)
    startDatePicker.grid(row=1, column=1)

    # Set default start time to now
    startDatePicker.set_date(datetime.now())

    # Create the start time label
    label = ttk.Label(root, text="Start time:")
    label.grid(row=2, column=0)

    # Create start time picker
    start_time_picker = SpinTimePickerModern(root)
    start_time_picker.addAll(constants.HOURS12)  # adds hours clock, minutes and period
    start_time_picker.configureAll(bg="#404040", height=1, fg="#ffffff", font=("Times", 16), hoverbg="#404040",
                                   hovercolor="#d73333", clickedbg="#2e2d2d", clickedcolor="#d73333")
    start_time_picker.configure_separator(bg="#404040", fg="#ffffff")
    start_time_picker.set12Hrs(datetime.now().hour)
    start_time_picker.set24Hrs(datetime.now().hour)
    start_time_picker.setMins(datetime.now().minute)

    start_time_picker.grid(row=2, column=1)

    # Create the end date label
    endDateTimeLabel = ttk.Label(root, text="End Date:")
    endDateTimeLabel.grid(pady=10, padx=15, row=3, column=0)

    # Create the end-date entry widget
    endDatePicker = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)
    endDatePicker.grid(row=3, column=1)

    # Set default end date to now
    endDatePicker.set_date(datetime.now())

    # Create the end time label
    label = ttk.Label(root, text="End time:")
    label.grid(row=4, column=0)

    # Create end time picker
    end_time_picker = SpinTimePickerModern(root)
    end_time_picker.addAll(constants.HOURS12)  # adds hours clock, minutes and period
    end_time_picker.configureAll(bg="#404040", height=1, fg="#ffffff", font=("Times", 16), hoverbg="#404040",
                                 hovercolor="#d73333", clickedbg="#2e2d2d", clickedcolor="#d73333")
    end_time_picker.configure_separator(bg="#404040", fg="#ffffff")
    end_time_picker.set12Hrs(datetime.now().hour + 1)
    end_time_picker.set24Hrs(datetime.now().hour + 1)
    end_time_picker.setMins(datetime.now().minute)

    end_time_picker.grid(row=4, column=1)

    # print(datetime.now().strftime("%d-%m-%Y %I:%M %p"))

    # Take attendance button
    course_reg_btn = ttk.Button(root, text="Take attendance", command=lambda: displayAttendanceWindow(lecture, root))
    course_reg_btn.grid(row=7, column=0)

    if isCreate:
        course_reg_btn.grid_forget()
    else:
        course_reg_btn.grid(row=7, column=0)

    # Create the save button
    save_button = tk.Button(root, text="Save", bg='blue', fg='white', command=lambda: saveLecture(
        selected_option, startDatePicker, start_time_picker, endDatePicker, end_time_picker, isCreate
    ))
    save_button.grid(row=7, column=3)

    # Create the delete button
    delete_button = tk.Button(root, text="Delete", bg='red', fg='white', command=lambda: delete(lecture.lectureId))

    # Hide delete button if creating new record
    if isCreate:
        delete_button.grid_forget()
    else:
        delete_button.grid(row=7, column=2)

    if lecture:
        # Get number of marked students
        numberOfMarkedStudents = queryCount(lecture.courseCode)

        # Get number of registered students
        numberOfRegStudents = qc(lecture.courseCode)

        # Registered students button
        reg_students_btn = ttk.Button(root, text=f"Attendance: {numberOfMarkedStudents}/{numberOfRegStudents} students",
                                      command=lambda: show_attendance_window(lecture, False))
        reg_students_btn.grid(row=8, column=1)


def saveLecture(selected_option, startDatePicker, start_time_picker, endDatePicker, end_time_picker, isCreate):
    # Get course code and title from drop-down menu
    courseCode = selected_option.get().split(',')[0]
    courseTitle = selected_option.get().split(',')[1].replace(" ", "", 1)  # remove space at beginning of title

    startDate = startDatePicker.get()
    mStartTimeHour = start_time_picker.hours24()
    mStartTimeMin = start_time_picker.minutes()

    endDate = endDatePicker.get()
    mEndTimeHour = end_time_picker.hours24()
    mEndTimeMin = end_time_picker.minutes()

    lectureId = secrets.token_hex(6)

    startTime = f"{startDate}, {mStartTimeHour}:{mStartTimeMin}"
    endTime = f"{endDate}, {mEndTimeHour}:{mEndTimeMin}"

    lecture = Lecture(
        courseTitle=courseTitle,
        courseCode=courseCode,
        lectureId=lectureId,
        startTime=startTime,
        endTime=endTime,
    )

    if isCreate:
        insert(lecture)
    else:
        updateLecture(lecture)
