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

    # def join_dicts(self, d1, d2):
    #     for k in d2.keys():
    #         if k in d1.keys():
    #             d1[k] += [d2[k]]
    #             for idx, (doc_id, fij, tf, wij) in enumerate(d1[k]):
    #                 wij = tf * log10(self.N / self.inverted_idx[k])
    #                 d1[k][idx] = (doc_id, fij, tf, wij)
    #         else:
    #             d1[k] = [d2[k]]
    #
    #     d1[k].sort()
