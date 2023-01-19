import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

from database.student_db import getAllStudents, getOneStudent, updateStudent, insert
from model.student import Student


def displayStudentInfo(isCreate, student=None):
    root = tk.Tk()

    if isCreate:
        root.title("Create new record")
    else:
        root.title(f"{student.Fullname} Details")
    root.geometry("500x500")

    # Create a custom style for the label
    style = ttk.Style()
    style.configure("My.TLabel", background="#f0f0f0", borderradius=5)

    # Open the image file using PIL
    if isCreate:
        image = Image.open(student.DisplayPicture)

        # Convert the image to a PhotoImage object
        photo_image = ImageTk.PhotoImage(image)

        # Create the label widget to display the image
        image_path = student.DisplayPicture
        img = ImageTk.PhotoImage(Image.open(image_path))
        # image_label = ttk.Label(root, image=photo_image, style="My.TLabel")
        # image_label.pack(expand=True, fill='both')

    # Create the Full name label
    fNameLabel = ttk.Label(root, text="Full Name:")
    fNameLabel.grid(pady=10, padx=15, row=0, column=0)

    # Create the text box
    fNameTextbox = ttk.Entry(root)
    fNameTextbox.grid(row=0, column=1)

    if not isCreate:
        fNameTextbox.insert(0, student.Fullname)

    # Create the Matric label
    matricLabel = ttk.Label(root, text="Matric:")
    matricLabel.grid(pady=10, padx=15, row=1, column=0)

    # Create the text box
    matricTextbox = ttk.Entry(root)
    matricTextbox.grid(row=1, column=1)

    if not isCreate:
        matricTextbox.insert(0, student.Matric)

    # Disable the textbox
    if not isCreate:
        matricTextbox.config(state='disable')

    # Create the Department label
    departLabel = ttk.Label(root, text="Department:")
    departLabel.grid(pady=10, padx=15, row=2, column=0)

    # Create the text box
    departLabelTextbox = ttk.Entry(root)
    departLabelTextbox.grid(row=2, column=1)

    if not isCreate:
        departLabelTextbox.insert(0, student.Department)

    # Create the Faculty label
    facultyLabel = ttk.Label(root, text="Faculty:")
    facultyLabel.grid(pady=10, padx=15, row=3, column=0)

    # Create the text box
    facultyLabelTextbox = ttk.Entry(root)
    facultyLabelTextbox.grid(row=3, column=1)

    if not isCreate:
        facultyLabelTextbox.insert(0, student.Faculty)

    # Create a variable to store the selected gender
    gender = tk.StringVar()

    # Create the radio buttons
    male_button = tk.Radiobutton(root, text="Male", variable=gender, value="Male")
    female_button = tk.Radiobutton(root, text="Female", variable=gender, value="Female")

    # Pack the radio buttons
    male_button.grid(row=4, column=0)
    female_button.grid(row=4, column=1)

    if student.Gender.lower() == "male":
        male_button.select()
        gender.set(student.Gender)
    if student.Gender.lower() == "female":
        female_button.select()
        gender.set(student.Gender)

# Create the save button
    save_button = tk.Button(root, text="Save", bg='blue', fg='white', command=lambda: saveStudent(
        fNameTextbox.get(), matricTextbox.get(), departLabelTextbox.get(), facultyLabelTextbox.get(),
        gender.get(), student, isCreate
    ))
    save_button.grid(row=7, column=2)

    # Create the delete button
    delete_button = tk.Button(root, text="Delete", bg='red', fg='white', command=lambda: deleteStudent(student.Matric))
    delete_button.grid(row=7, column=0)

    # Hide delete button if creating new record
    if isCreate:
        delete_button.grid_forget()
    else:
        delete_button.grid(row=7, column=0)


def saveStudent(fullname, matric, depart, faculty, gender, mStudent, isCreate):
    student = Student(
        Fullname=fullname,
        Faculty=faculty,
        Gender=gender,
        Matric=matric,
        Department=depart,
        DateOfBirth=mStudent.DateOfBirth,
        DisplayPicture=mStudent.DisplayPicture,
        IsGottenIDCard=mStudent.IsGottenIDCard
    )

    if isCreate:
        student.DateOfBirth = ""
        student.DisplayPicture = ""
        student.IsGottenIDCard = "False"

        insert(student)
    else:
        updateStudent(student)


def deleteStudent(matricNumber):
    deleteStudent(matricNumber)
