import warnings

warnings.filterwarnings("ignore", category=UserWarning)

import torch  # noqa: E402
import torchvision  # noqa: E402

print(f"PyTorch Version: {torch.__version__}")
print(f"Torchvision Version: {torchvision.__version__}")

# Appleシリコンの場合、これが True になればGPU（MPS）が使えます
print(f"MPS (Metal) available: {torch.backends.mps.is_available()}")
