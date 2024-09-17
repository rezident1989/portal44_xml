import pickle


def save_data(data, name_object):
    with open(f"archive/{name_object}.pickle", "wb") as file_1:
        pickle.dump(data, file_1)


def load_data(name_object):
    with open(f"archive/{name_object}.pickle", "rb") as file_2:
        return pickle.load(file_2)
