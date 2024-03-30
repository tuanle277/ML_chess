import torch
import torch.nn as nn

class ChessModel(nn.Module):
    def __init__(self):
        super(ChessModel, self).__init__()
        self.conv1 = nn.Conv2d(12, 64, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1)
        self.fc1 = nn.Linear(128 * 8 * 8, 1024)
        self.fc2 = nn.Linear(1024, 4096)  # Assuming 4096 possible moves
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = x.view(-1, 128 * 8 * 8)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        x = self.softmax(x)
        return x

def load_model(model_path, device='cpu'):
    """
    Loads a trained ChessModel from the specified file.

    :param model_path: Path to the file containing the saved model state.
    :param device: The device to load the model onto ('cpu' or 'cuda').
    :return: The loaded ChessModel instance.
    """
    # Initialize the model architecture
    model = ChessModel()

    # Load the saved state_dict into the model
    model.load_state_dict(torch.load(model_path, map_location=device))

    # Set the model to evaluation mode
    model.eval()

    return model
