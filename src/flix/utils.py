import pickle


def save_pickle(data, filename):
    with open(f'{filename}.pickle', 'wb') as file:
        pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)


def load_pickle(filename):
    with open(filename, 'rb') as file:
        data = pickle.load(file)
    return data
