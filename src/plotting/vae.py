import torch
import torchvision
import io
import matplotlib.pyplot as plt
from PIL import Image
from tensordict.nn import TensorDictModule
from tensordict import TensorDict
import torch.nn.functional as F


def plot_vae_samples(model: TensorDictModule, samples: TensorDict, loc: float, scale: float) -> Image.Image:
    model.eval()
    num_samples = samples['pixels_transformed'].shape[0]
    with torch.no_grad():
        output = model(samples)
        
        p_x = output["p_x"]
        
        samples = F.sigmoid(p_x.loc.cpu())
    
    x_recon = torch.clamp((samples * scale + loc) * 255, min=0, max=255).to(torch.uint8)
    
    grid = torchvision.utils.make_grid(x_recon[:num_samples], nrow=num_samples // 2)
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    ax.set_title("Reconstructed samples")
    ax.imshow(grid.permute(1, 2, 0).cpu().numpy())
    
    img_buf = io.BytesIO()
    
    fig.tight_layout()
    fig.savefig(img_buf, format='png', bbox_inches='tight',dpi=100)

    pil_image = Image.open(img_buf)
        
    return pil_image
