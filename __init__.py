import os
from huggingface_hub import hf_hub_download
from .resadapter_loraloader import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS


def download_models(model_name, models_dir):
    hf_hub_download(repo_id="jiaxiangc/res-adapter", subfolder=f"{model_name}", filename="pytorch_lora_weights.safetensors", local_dir=models_dir)
    if "interpolation" not in model_name:
        hf_hub_download(repo_id="jiaxiangc/res-adapter", subfolder=model_name, filename="diffusion_pytorch_model.safetensors", local_dir=models_dir)


base_path = os.path.dirname(os.path.realpath(__file__))
models_dir = os.path.join(base_path, "models")

os.makedirs(models_dir, exist_ok=True)

MODEL_LIST = ["resadapter_v1_sd1.5", "resadapter_v1_sd1.5_interpolation", "resadapter_v1_sd1.5_extrapolation", 
              "resadapter_v1_sdxl", "resadapter_v1_sdxl_interpolation", "resadapter_v1_sdxl_extrapolation"]

for MODEL in MODEL_LIST:
    if not os.path.exists(os.path.join(models_dir, MODEL)):
        download_models(MODEL, models_dir)

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
