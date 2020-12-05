import pickle
import os


def save_obj(obj, name):
    """
    This function save an object as a pickle.
    :param obj: object to save
    :param name: name of the pickle file.
    :return: -
    """
    with open(name + '.pkl', 'wb') as file:
        pickle.dump(obj, file, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    """
    This function will load a pickle file
    :param name: name of the pickle file
    :return: loaded pickle file
    """
    with open(name + '.pkl', 'rb') as file:
        return pickle.load(file)


def delete_obj(name):
    """
    This function will delete a pickle file
    :param name: name of the pickle file
    :return: -
    """
    if os.path.exists(name):
        os.remove(name)


def load_inverted_index(path):
    """
    This function loads the inverted index file
    :param path: path to file
    :return: the dictionary of the inverted index
    """
    with open(path, 'rb') as file:
        return pickle.load(file)
