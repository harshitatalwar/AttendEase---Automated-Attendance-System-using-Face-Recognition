# import mysql.connector
# from mysql.connector import Error
# import os
# import pickle
# from datetime import datetime
#
#
# data_folder = r"C:\Users\mandv\PycharmProjects\AutomatedAttendace\ProcterAI\data"
# existing_user_ids = set()
# for filename in os.listdir(data_folder):
#     if filename.startswith("user.") and filename.endswith(".jpg"):
#         user_id = int(filename.split(".")[1])
#         existing_user_ids.add(user_id)
#
# next_user_id = 1
# while next_user_id in existing_user_ids:
#     next_user_id += 1
#
#
# # Function to establish a database connection
# def connect_to_database():
#     try:
#         connection = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="123456",
#             database="attendance_system"
#         )
#         if connection.is_connected():
#             print("Connected to the database")
#             return connection
#     except Error as e:
#         print("Error:", e)
#         return None
#
# # Assuming you have the date in the format '25/10/2023'
# date_string = '25/10/2023'
#
# def insert_recognized_user(connection, user_id, recognized_user):
#     try:
#         cursor = connection.cursor()
#
#         # Fetch the student name based on the user_id
#         cursor.execute(f"SELECT name, student_id_number FROM students WHERE student_id = {user_id}")
#         result = cursor.fetchone()
#         student_name = result[0]
#         student_id_number = result[1]
#         # current_date = datetime.now().strftime("%d-%m-%Y")
#         # Convert the date string to the desired format
#         current_date = datetime.strptime(date_string, '%d/%m/%Y').strftime('%Y-%m-%d')
#         insert_query = "INSERT INTO recognized_users (user_id, student_name, student_id_number, recognition_date) VALUES (%s, %s, %s, %s)"
#         cursor.execute(insert_query, (recognized_user, student_name, student_id_number, current_date))
#         connection.commit()
#         print("Recognized user data inserted successfully.")
#     except Error as e:
#         print("Error:", e)
#
#
# def fetch_recognized_users(connection):
#     try:
#         cursor = connection.cursor(dictionary=True)
#         cursor.execute("SELECT id, student_name, student_id_number, recognition_date FROM recognized_users")
#         recognized_users = cursor.fetchall()
#         return recognized_users
#     except Error as e:
#         print("Error:", e)
#         return None
#
#
# # Function to insert metadata (embedding) into the metadata table
# def insert_metadata(connection, user_id, img_id, embedding_data):
#     try:
#         cursor = connection.cursor()
#         insert_query = "INSERT INTO metadata (user_id, img_id, embedding) VALUES (%s, %s, %s)"
#         serialized_embedding_data = pickle.dumps(embedding_data)  # Serialize the data
#         cursor.execute(insert_query, (user_id, img_id, serialized_embedding_data))
#         connection.commit()
#         print("Metadata inserted successfully for user", user_id)
#     except Error as e:
#         print("Error:", e)
#
# # Function to insert binary image data into the binary_data table
# def insert_image_data(connection, user_id, img_id, img_data):
#     try:
#         cursor = connection.cursor()
#         insert_query = "INSERT INTO binary_data (user_id, img_id, image_data) VALUES (%s, %s, %s)"
#         print("Image data inserted successfully for user", user_id, "and img_id", img_id)
#         cursor.execute(insert_query, (user_id, img_id, img_data))
#         connection.commit()
#     except Error as e:
#         print("Error:", e)
#
# # Function to close the database connection
# def close_database(connection):
#     if connection.is_connected():
#         connection.close()
#         print("Database connection closed")
#
# # Example usage:
# _name_= "_main_"
# if _name_ == "_main_":
#     db_connection = connect_to_database()
#     if db_connection:
#         encoding_folder = "encodings/"
#
#
#         for user_id in range(1, next_user_id):
#             user_folder_path = os.path.join(encoding_folder, f"user_{user_id}")
#
#             # Insert metadata (embedding)
#             embedding_start_number = ((user_id - 1) * 20) + 1
#             embedding_file_path = os.path.join(user_folder_path, f"encoding_{embedding_start_number}.npy")
#             with open(embedding_file_path, 'rb') as embedding_file:
#                 embedding_data = embedding_file.read()
#
#             for img_id in range(1, 21):
#                 # Calculate the actual img_id based on user_id
#                 if user_id == 1:
#                     img_id = img_id
#                 else:
#                     img_id = (user_id - 1) * 20 + img_id
#
#                 # Generate the image file path based on the naming convention
#                 img_path = f"data/user.{user_id}.{img_id}.jpg"
#
#                 insert_metadata(db_connection, user_id, img_id, embedding_data)
#                 insert_image_data(db_connection, user_id, img_id, img_path)
#
#         close_database(db_connection)