import csv
import datetime
import cv2
import os

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def take_attendance(student_id, student_name):
    # Get today's date
    date = datetime.date.today().isoformat()  # Format date as YYYY-MM-DD

    # Check if the attendance file for today exists
    filename = f'attendance_{date}.csv'
    if not os.path.exists(filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Student Name', 'Registration Number', 'Date', 'Attendance', 'Image Location'])

    # Initialize the camera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Capture the image
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame from camera.")
        cap.release()
        return

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    attendance = "Absent"
    image_location = ""

    if len(faces) > 0:
        attendance = "Present"
        image_location = f"{student_id}_{date}.jpg"
        cv2.imwrite(image_location, frame)  # Save the photo with student's ID and date
    else:
        print("No face detected!")

    # Release the camera
    cap.release()
    cv2.destroyAllWindows()

    # Update the CSV file
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([student_name, student_id, date, attendance, image_location])

    return attendance

if __name__ == "__main__":
    # Get the range of student IDs from the user
    start_id = int(input("Enter the starting student ID: "))
    end_id = int(input("Enter the ending student ID: "))
    
    attendance_count = {"Present": 0, "Absent": 0}

    for student_id in range(start_id, end_id + 1):
        student_name = input(f"Enter name for Student ID {student_id}: ")
        attendance = take_attendance(student_id, student_name)

        if attendance == "Present":
            attendance_count["Present"] += 1
        else:
            attendance_count["Absent"] += 1

    # Summary of attendance
    print("\nAttendance Summary:")
    total_students = end_id - start_id + 1
    print(f"Total Students: {total_students}")
    print(f"Present: {attendance_count['Present']}")
    print(f"Absent: {attendance_count['Absent']}")
