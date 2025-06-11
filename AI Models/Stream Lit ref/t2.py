import torch
print("Using device:", "CUDA" if torch.cuda.is_available() else "CPU")