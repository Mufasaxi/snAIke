import torch.nn as nn
import torch.nn.functional as F


class SnAIkeModel(nn.Module):
    def __init__(self):
        super(SnAIkeModel, self).__init__()

        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2,2)
        self.fc1 = nn.Linear(64 * 5 * 6, 128)
        self.fc2 = nn.Linear(128, 4)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = self.pool(self.relu(self.conv3(x)))
        x = x.view(-1, 64 * 5 * 6)
        x = self.relu(self.fc1(x))
        x = self.fc2(x) 
        
        return F.log_softmax(x, dim=1)