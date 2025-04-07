from collections import Counter
import pickle

class Model:
    def __init__(self):
        self.good_counts = Counter()
        self.bad_counts = Counter()
        self.num_good_emails = 0
        self.num_bad_emails = 0
    
    def write(self, path: str):
        with open(path, 'wb') as f:
            pickle.dump(self, f)
    
    @staticmethod
    def read(path: str):
        with open(path, 'rb') as f:
            return pickle.load(f)
    