import tkinter as tk
import cv2
import face_recognition

import time


def search_for_students_with_ai(students):
    # Load the saved images that you want to match against
    saved_images = []
    saved_encodings = []

    for student in students:
        # print(student.Fullname)
        saved_image = face_recognition.load_image_file(student.DisplayPicture)
        saved_encoding = face_recognition.face_encodings(saved_image)[0]
        saved_images.append(saved_image)
        saved_encodings.append([saved_encoding, student])

    # Start the webcam
    cap = cv2.VideoCapture(0)

    # classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "../assets/haarcascade_frontalface_default.xml")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        # Convert the webcam image to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Convert the frame to RGB
        rgb_frame = frame[:, :, ::-1]

        # Find the faces in the webcam image
        faces = face_recognition.face_locations(gray)

        # faces = classifier.detectMultiScale(gray, 1.5, 5)

        for (top, right, bottom, left) in faces:
            # Draw a box around the face
            # cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Get the face encoding from the webcam image
            webcam_encoding = face_recognition.face_encodings(rgb_frame, [(top, right, bottom, left)])[0]

            # Compare the face encodings
            for saved_encoding in saved_encodings:
                results = face_recognition.compare_faces([saved_encoding[0]], webcam_encoding)

                # If the face encodings match, display "Matched"
                if results[0]:
                    foundStudent = saved_encoding[1]
                    print(foundStudent.Fullname)

                    # cv2.putText(frame, foundStudent.Fullname, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    cap.release()
                    cv2.destroyAllWindows()
                    break
                else:
                    cv2.putText(frame, "Not Matched", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Display the webcam image with the face box and match status
        # cv2.imshow("Webcam", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close the window
    cap.release()
    cv2.destroyAllWindows()
