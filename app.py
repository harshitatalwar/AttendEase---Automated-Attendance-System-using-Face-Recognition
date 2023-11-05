from flask import Flask, render_template, request, session, redirect, url_for
import mysql.connector
import subprocess  # For triggering face recognition
import cv2
import numpy as np
import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime
import pickle

app = Flask(__name__)
app.secret_key = 'key'
app.config['SESSION_TYPE'] = 'filesystem'

# Establish MySQL connection
db_connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456',
    database='attendance_system',
    autocommit=True
)
cursor = db_connection.cursor()

data_folder = r"C:\Users\mandv\PycharmProjects\AutomatedAttendace\ProcterAI\data"
existing_user_ids = set()
for filename in os.listdir(data_folder):
    if filename.startswith("user.") and filename.endswith(".jpg"):
        user_id = int(filename.split(".")[1])
        existing_user_ids.add(user_id)

next_user_id = 1
while next_user_id in existing_user_ids:
    next_user_id += 1


existing_img_ids = set()
for filename in os.listdir(data_folder):
    if filename.startswith("user.") and filename.endswith(".jpg"):
        user_id = int(filename.split(".")[2])
        existing_img_ids.add(user_id)

next_img_id = 1
while next_img_id in existing_img_ids:
    next_img_id += 1
# Function to insert binary image data into the binary_data table


def insert_image_data(connection, user_id, img_id, img_data):
    try:
        cursor = connection.cursor()
        insert_query = "INSERT INTO binary_data (user_id, img_id, image_data) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (user_id, img_id, img_data))
        connection.commit()
        print("Image data inserted successfully for user", user_id, "and img_id", img_id)
    except Error as e:
        print("Error:", e)


def insert_metadata(connection, user_id, img_id, embedding_data):
    try:
        cursor = connection.cursor()
        insert_query = "INSERT INTO metadata (user_id, img_id, embedding) VALUES (%s, %s, %s)"
        serialized_embedding_data = pickle.dumps(embedding_data)  # Serialize the data
        cursor.execute(insert_query, (user_id, img_id, serialized_embedding_data))
        connection.commit()
        print("Metadata inserted successfully for user", user_id)

    except Error as e:
        print("Error:", e)


# Function to insert recognized user into the recognized_users table
def insert_recognized_user(connection,recognized_user):
    try:
        cursor = connection.cursor()

        # Fetch the student name and student id number based on the user_id
        cursor.execute(f"SELECT name, student_id_number FROM students WHERE student_id = {recognized_user}")
        result = cursor.fetchone()

        if result is not None:
            student_name = result[0]
            student_id_number = result[1]
            current_date = datetime.now().strftime('%Y-%m-%d')
            insert_query = "INSERT INTO recognized_users (user_id, student_name, student_id_number, recognition_date) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (recognized_user, student_name, student_id_number, current_date))
            connection.commit()
            print("Recognized user data inserted successfully.")
        else:
            print(f"No student found with user_id {user_id}.")
    except Error as e:
        print("Error:", e)


# Route for registering a student
@app.route('/student', methods=['GET', 'POST'])
def register_student():

    if request.method == 'POST':
        # Get data from the form
        student_name = request.form['studentName']
        student_id = request.form['studentID']
        password = request.form['password']

        # Insert the data into the database
        cursor.execute("INSERT INTO students (name, student_id_number, password) VALUES (%s, %s, %s)", (student_name, student_id, password))
        db_connection.commit()

        return "Student registered successfully!"

    return render_template('register.html')


@app.route('/run_training', methods=['POST'])
def run_training():
    # Define the path to your Python executable within the virtual environment
    python_path = r"C:\Users\mandv\PycharmProjects\AutomatedAttendace\ProcterAI\venv\Scripts\python.exe"


    # Define the path to your training_data.py script
    script_path = r"C:\Users\mandv\PycharmProjects\AutomatedAttendace\ProcterAI\training_data.py"

    try:
        # Run the training_data.py script using the specified Python executable
        result = subprocess.run([python_path, script_path], capture_output=True, text=True, check=True)

        # Print the script's output
        print(result.stdout)

        user_id_here = next_user_id
        img_id = next_img_id

        for img_id in range(img_id, img_id + 19):
            # Generate the image path based on user_id and img_id
            image_path = f"data/user.{user_id_here}.{img_id}.jpg"
            image = cv2.imread(image_path)
            image_data = np.array(image).tobytes()
            insert_image_data(db_connection, user_id_here, img_id, image_data)

        return "Training script executed successfully."
    except subprocess.CalledProcessError as e:
        # If there's an error running the script, print the error message
        print(e.stderr)
        return "Error executing the training script."


@app.route('/finish', methods=['POST'])
def finish():
    # Define the path to your Python executable within the virtual environment
    python_path = r"C:\Users\mandv\PycharmProjects\AutomatedAttendace\ProcterAI\venv\Scripts\python.exe"


    # Define the path to your training_data.py script
    script_path = r"C:\Users\mandv\PycharmProjects\AutomatedAttendace\ProcterAI\face_recognition.py"

    try:
        # Run the training_data.py script using the specified Python executable
        result = subprocess.run([python_path, script_path], capture_output=True, text=True, check=True)

        # Print the script's output
        print(result.stdout)

        encoding_folder = "encodings/"

        user_id_here = next_user_id
        img_id = next_img_id
        print(user_id_here)
        print(img_id)
        user_folder_path = os.path.join(encoding_folder, f"user_{user_id_here}")

        for img_id_to_store in range(next_img_id, next_img_id + 20):
            embedding_start_number = ((user_id_here - 1) * 20) + (img_id_to_store - next_img_id) + 1
            embedding_file_path = os.path.join(user_folder_path, f"encoding_{embedding_start_number}.npy")
            if os.path.exists(embedding_file_path):
                with open(embedding_file_path, 'rb') as embedding_file:
                    embedding_data = embedding_file.read()
                insert_metadata(db_connection, user_id_here, img_id_to_store, embedding_data)
            else:
                # Handle the case when the file is not found
                continue

        return "Recognition script executed successfully."

    except subprocess.CalledProcessError as e:
        # If there's an error running the script, print the error message
        print(e.stderr)
        return "Error executing the face_recognition script."


@app.route('/teacher')
def teacher_interface():
    return render_template('teacher.html')

# Route for marking attendance
@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    # Define the path to your Python executable within the virtual environment
    python_path = r"C:\Users\mandv\PycharmProjects\AutomatedAttendace\ProcterAI\venv\Scripts\python.exe"

    # Define the path to your training_data.py script
    script_path = r"C:\Users\mandv\PycharmProjects\AutomatedAttendace\ProcterAI\real_time.py"

    try:
        # Run the training_data.py script using the specified Python executable
        result = subprocess.run([python_path, script_path], capture_output=True, text=True, check=True)

        # Print the script's output
        print(result.stdout)

        from real_time import recognise
        for face_info in recognise:
            print(
                f"Detected face: {face_info['detected_face']}, Recognized user: {face_info['recognized_user']}, Distance: {face_info['distance']}")

            # Insert recognized users into the recognized_users table
        for face_info in recognise:
            user_id = face_info['detected_face']  # Assuming detected_face contains user IDs
            recognized_user = face_info['recognized_user']
            insert_recognized_user(db_connection, recognized_user)

        return "Attendance marked successfully."
    except subprocess.CalledProcessError as e:
        # If there's an error running the script, print the error message
        print(e.stderr)
        return "Error executing the real_time script."

# Route for displaying recognized users
@app.route('/present', methods=['GET'])
def present():
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT id, student_name, student_id_number, recognition_date FROM recognized_users")
        recognized_users = cursor.fetchall()
        return render_template('Present.html', recognized_users=recognized_users)
    except Error as e:
        print("Error:", e)
        return "Error retrieving recognized users."

@app.route('/')
def start_interface():
    return render_template('start.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the student ID number and password from the form
        student_id_number = request.form['student_id_number']
        password = request.form['password']

        # Check if the entered credentials exist in the student table
        cursor.execute("SELECT * FROM students WHERE student_id_number = %s AND password = %s", (student_id_number, password))
        student = cursor.fetchone()

        if student:
            # Credentials are valid, set a session variable to remember the user
            session['student_id'] = student[0]  # Store the student's ID in the session
            return redirect(url_for('my_attendance'))
        else:
            # Invalid credentials, display a message or redirect to the signup page
            return "Invalid credentials. Please sign up first."

    return render_template('login.html')

@app.route('/my_attendance')
def my_attendance():
    student_id = session.get('student_id')  # Retrieve the student's ID from the session

    if student_id:
        student_data = fetch_student_data(student_id)

        if student_data:
            cursor = db_connection.cursor()
            cursor.execute("SELECT recognition_date FROM recognized_users WHERE user_id = %s", (student_id,))
            attendance_data = cursor.fetchall()

            return render_template('MyAttendance.html', student=student_data, attendance_data=attendance_data)
        else:
            return "Student data not found."
    else:
        return "You are not logged in. Please sign in first."

def fetch_student_data(student_id):
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM recognized_users WHERE user_id = %s", (student_id,))
        student_data = cursor.fetchone()

        if student_data:
            return student_data
        else:
            return None
    except Error as e:
        print("Error:", e)
        return None


if __name__ == '__main__':
    app.run(debug=False)

# Close the database cursor and connection
cursor.close()
db_connection.close()

