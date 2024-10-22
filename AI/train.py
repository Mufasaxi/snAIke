import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from dataset import SnAIkeDataset, load_data
from model import SnAIkeModel
import os

def train(model, train_loader, criterion, optimiser, device):
    model.train()
    running_loss = 0.0
    for i, (inputs, labels) in enumerate(train_loader):
        inputs, labels = inputs.unsqueeze(1).to(device), labels.to(device).long()
        optimiser.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimiser.step()
        running_loss += loss.item()
    return running_loss / len(train_loader)

def evaluate(model, val_loader, criterion, device):
    model.eval()
    running_loss =  0.0
    correct = 0
    total = 0

    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs, labels = inputs.unsqueeze(1).to(device), labels.to(device).long()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
    accuracy = correct / total
    return running_loss / len(val_loader), accuracy

def main():
    batch_size = 64
    learning_rate = 0.001
    num_epochs = 100 

    X, y = load_data("X_data.npy", "y_data.npy")
    

    split = int(0.8*len(y))
    train_dataset = SnAIkeDataset(X[:split], y[:split])
    val_dataset = SnAIkeDataset(X[split:], y[split:])

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size)

    device = torch.device("cuda" if torch.cuda.is_available else "cpu")
    model = SnAIkeModel().to(device)
    criterion = nn.CrossEntropyLoss()
    optimiser = optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in range(num_epochs):
        train_loss = train(model, train_loader, criterion, optimiser, device)
        val_loss, val_accuracy = evaluate(model, val_loader, criterion, device)

        print(f"Epoch {epoch+1}/{num_epochs}")
        print(f"Train Loss: {train_loss:.4f}")
        print(f"Val Loss: {val_loss:.4f}, Val Accuracy: {val_accuracy:.4f}")

    torch.save(model.state_dict(), 'snAIke_100EPOCHS.pth')

if __name__ == '__main__':
    main()