from sklearn.model_selection import train_test_split
from data_labelling import labelling_data


data_folder = r"C:\Users\mandv\PycharmProjects\AutomatedAttendace\ProcterAI\data"
max_images_per_user = 20
a, b, _, _ = labelling_data(data_folder, max_images_per_user)


def split_data(a, b, test_size=0.2, random_state=42):

    x_train, x_test, y_train, y_test = train_test_split(a, b, test_size=test_size, random_state=random_state)
    print("Training data shape - Features:", x_train.shape, " Labels:", y_train.shape)
    print("Testing data shape - Features:", x_test.shape, " Labels:", y_test.shape)
    return x_train, x_test, y_train, y_test


# split_data(a, b, test_size=0.2, random_state=42)