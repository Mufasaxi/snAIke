import torch
import numpy as np
from torch.utils.data import Dataset, DataLoader

class SnAIkeDataset(Dataset):
    def __init__(self, X, y):
        self.X = X
        self.y = y

    def __len__(self):
        return len(self.y)
    
    def __getitem__(self, index):
        return self.X[index], self.y[index]
    

def load_data(x_path, y_path):
    X = np.load(x_path)
    y = np.load(y_path)
    return X, y