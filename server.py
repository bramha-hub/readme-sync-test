from mcp.server.fastmcp import FastMCP
# Create an MCP server
mcp = FastMCP("Demo")

print("Hello from server!")

@mcp.tool()
def usd_to_gbp(amount: float) -> float:
    """Convert USD(dollars) to GBP(pounds sterling)"""
    print("Hello from server!")
    EXCHANGE_RATE = 0.79
    return round (amount * EXCHANGE_RATE, 2)

import torch
import torch.nn as nn
import torch.optim as optim

# ---------------------------
# 1. Define Neural Network
# ---------------------------

class SimpleNN(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(SimpleNN, self).__init__()
        
        self.model = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim)
        )

    def forward(self, x):
        return self.model(x)


# ---------------------------
# 2. Hyperparameters
# ---------------------------

input_dim = 10
hidden_dim = 64
output_dim = 3
learning_rate = 0.001
epochs = 100

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ---------------------------
# 3. Create Model
# ---------------------------

model = SimpleNN(input_dim, hidden_dim, output_dim).to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# ---------------------------
# 4. Dummy Data (Example)
# ---------------------------

X = torch.randn(1000, input_dim).to(device)
y = torch.randint(0, output_dim, (1000,)).to(device)

# ---------------------------
# 5. Training Loop
# ---------------------------

for epoch in range(epochs):
    model.train()

    outputs = model(X)
    loss = criterion(outputs, y)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if (epoch+1) % 10 == 0:
        print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")
