# AttendEase---Automated-Attendance-System-using-Face-Recognition
A **Flask Web Application** for student registration and automated attendance system using face recognition which provides a user interface for image data collection for face recognition training and detection. The system utilizes a combination of **Python, Dlib, OpenCV, Flask, and MySQL**.

 Users can interact with the application to capture images while a Python script processes and organizes the collected data for model training. The use of OpenCV enables real-time face detection, and threading allows the training process to run concurrently with the web application, providing a responsive and seamless user experience. It involves three main components: data collection, training, and real-time attendance marking. It handles HTTP requests, user authentication, and database interactions. Provides routes for user registration, login, marking and viewing attendance data.

The **database** stores student information, including student IDs, names, and passwords. It also stores attendance data, including recognition dates.

**Training engine**: Images of students are collected and stored in tables. Training model is trained on these images to generate encodings which will further facilitate the recognition process.

**Recognition Engine**: The Recognition Engine is responsible for facial recognition. It processes images, detects faces, and matches them with stored encodings in the database. It logs recognition dates for each student.

 <img src="https://github.com/harshitatalwar/AttendEase---Automated-Attendance-System-using-Face-Recognition/assets/134962753/a5dad1d9-d56c-4737-9027-200ca6c73aea" width="500" height="500">

Summary of Python Scripts:

**training_data.py:**

• This script is responsible for training the system to recognize students. It captures images of students' faces, pre-processes them, and stores their facial encodings for later recognition.

• The script runs in a loop, capturing images until it has enough data for training.

• When it reaches the maximum number of images per user (20 in this case), it increments the user ID and continues capturing for the next user.

**real_time.py:**

• This script uses OpenCV and dlib to perform real-time face detection on a webcam feed.

• It detects faces, eyes, noses, and mouths, drawing rectangles around them. It continues capturing video frames until the user presses 'q'.

• The real_time.py script continuously captures video frames from a webcam feed and detects faces, eyes, noses, and mouths using OpenCV and dlib.

• Detected features are outlined with rectangles, and the video feed is displayed on the screen.

**recognise.py:**

• This script uses a pre-trained face recognition model to recognize students.

• It loads the model and detects faces in a real-time video stream.

• It assigns a name label based on student IDs to each recognized face and displays it in the video stream.

• It loads the pre-trained classifier and detects faces in the video stream.

• When a student's face is recognized, their name is displayed on the screen.

• Loading Aligned Face images from the "data" directory. These images are to be pre-processed and aligned for face recognition.

• Calculates the next available user ID and image ID to manage the registration of new students.

• Image Encoding and Storage processing each aligned face image for new students.

• Detects faces in the image and computes face encodings.

• These encodings are saved as NumPy arrays in files under the respective user directories.

• The code iterates through aligned face images, starting from the next available user and image IDs. It checks whether there are faces in each image and, if found, computes and saves face encodings.

**data_labelling.py:**

• This script is responsible for labelling data for training.

• It reads student data from image filenames, pre-processes the images, and assigns labels to each image based on the student's ID.

• The labelled data (features and labels) is used for training the recognition model.

• Labels data for training by reading student data from image filenames, pre-processing images, and assigning labels based on student IDs.

**data_splitting.py:**

• This script splits the labelled data into training and testing sets using the train_test_split function from scikit-learn.

• It separates the features (images) and labels (user IDs) to prepare the data for training, evaluating and testing the recognition model.

**alignment.py:**

• This script uses dlib to align faces in captured images.

• It takes a list of face images and returns a list of aligned faces.

• This alignment step is important for consistent face recognition.

• Aligns faces in captured images using dlib for consistent face recognition.

• Face alignment ensures consistency in face recognition.

**face_recognition.py:**

• This script uses a trained face recognition model to recognize students in a real-time video stream.

• It loads a classifier and assigns names to recognized faces based on the student's ID.

• Recognized names are displayed in the video stream.

**classifier.py:**

• This script contains a function to train a face recognition classifier.

• It loads image data from a specified directory, extracts faces, and trains a classifier using the LBPH (Local Binary Pattern Histograms) method.

• The trained classifier is saved to a file named "classifier.yml."

**app.py:**

• Sets up a Flask web application with routes for registering students, running training data, and managing teacher interfaces.

• When a student is registered, their data is inserted into a MySQL database.

• The application runs on a local server.

• Teachers can mark attendance through the web interface.

• The "Run Training" button triggers the execution of the face registration process.


![IMG-20231103-WA0003](https://github.com/harshitatalwar/AttendEase---Automated-Attendance-System-using-Face-Recognition/assets/134962753/d3020587-2fad-4424-98e6-ea714077bdbe)

![IMG-20231103-WA0002](https://github.com/harshitatalwar/AttendEase---Automated-Attendance-System-using-Face-Recognition/assets/134962753/1a8f6fa3-64ff-4bc5-bc5d-2a0445dcce06)

![IMG-20231103-WA0004](https://github.com/harshitatalwar/AttendEase---Automated-Attendance-System-using-Face-Recognition/assets/134962753/f665568f-853c-4cb1-b165-fcd1a2ed3afb)


![IMG-20231103-WA0001](https://github.com/harshitatalwar/AttendEase---Automated-Attendance-System-using-Face-Recognition/assets/134962753/87e4b2dc-eef9-4846-95a5-d04186de5943)







 <img src="https://github.com/harshitatalwar/AttendEase---Automated-Attendance-System-using-Face-Recognition/assets/134962753/32f17116-704e-4c2a-b0ff-69f3509a21a8" width="400" height="350">
<img src="https://github.com/harshitatalwar/AttendEase---Automated-Attendance-System-using-Face-Recognition/assets/134962753/aa5bfac2-6786-40f3-826c-b9721256c3fc" width="400" height="350">



