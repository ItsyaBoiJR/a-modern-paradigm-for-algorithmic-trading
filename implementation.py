import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

class DeltaEngine(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(DeltaEngine, self).__init__()
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        last_hidden_state = lstm_out[:, -1, :]
        output = self.fc(last_hidden_state)
        probabilities = self.softmax(output)
        return probabilities

def generate_synthetic_data(seq_length, num_features, num_samples):
    data = np.random.randn(num_samples, seq_length, num_features)
    labels = np.random.randint(0, 2, size=(num_samples,))
    return torch.tensor(data, dtype=torch.float32), torch.tensor(labels, dtype=torch.long)

def train_model(model, data, labels, epochs=10, lr=0.001):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        outputs = model(data)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        if (epoch + 1) % 2 == 0:
            print(f"Epoch [{epoch + 1}/{epochs}], Loss: {loss.item():.4f}")

def simulate_trading(model, data):
    model.eval()
    with torch.no_grad():
        predictions = model(data)
        actions = torch.argmax(predictions, dim=1)
        return actions

if __name__ == '__main__':
    seq_length = 10
    num_features = 5
    num_samples = 100
    hidden_size = 16
    output_size = 2

    # Generate synthetic data
    data, labels = generate_synthetic_data(seq_length, num_features, num_samples)

    # Initialize and train the Delta Engine
    model = DeltaEngine(input_size=num_features, hidden_size=hidden_size, output_size=output_size)
    train_model(model, data, labels, epochs=10, lr=0.001)

    # Simulate trading
    test_data, _ = generate_synthetic_data(seq_length, num_features, 10)
    actions = simulate_trading(model, test_data)
    print("Simulated trading actions:", actions.numpy())