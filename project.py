import csv
import datetime
import cv2

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def take_attendance():
    student_id = input("Enter Student ID: ")
    student_name = input("Enter Student Name: ")

    # in the below line we get
    date = datetime.date.today()

    # in the below line the Initialization of  the camera is happend
    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    if len(faces) > 0:
        attendance = "Present"
        
        photo_filename = f"{student_id}_{date}.jpg"
        cv2.imwrite(photo_filename, frame)
    else:
        attendance = "Absent"

    # Releasing the camera here
    cap.release()
    cv2.destroyAllWindows()

    # here i am Checking if the student already exists
    student_exists = False
    with open('attendance.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == student_id:
                student_exists = True
                break

    #  here i am Updating the CSV file
    with open('attendance.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        if not student_exists:
            writer.writerow(['Student ID', 'Student Name', 'Date', 'Attendance', 'Photo'])
        writer.writerow([student_id, student_name, date, attendance, photo_filename])

if __name__ == "__main__":
    take_attendance()
