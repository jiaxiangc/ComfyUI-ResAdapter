<div align=center>

## ResAdapter for ComfyUI

We provide ComfyUI-ResAdapter node to help users to use ResAdapter in ComfyUI.

⭐ If ResAdapter is helpful to your images or projects, please help star this repo and [bytedance/res-adapter](https://github.com/bytedance/res-adapter). Thanks! 🤗


</div>

## Installation

```bash 
# Step1: Clone ComfyUI-ResAdapter
git clone git@code.byted.org:lab-cv/ComfyUI-ResAdapter.git

# Step2: Move it to ComfyUI/custom_node
mv ComfyUI-ResAdapter ComfyUI/custom_node/

# Step3: Select Load ResAdapter Node in ComfyUI. We can use it like LoRA Loader.
```

## Download Model

We provide script for automatically downloading resadapter model from huggingface in `__init__.py`. If you can not connect with [huggingface.com](https://huggingface.co/), you can directly download model in [huggingface](https://huggingface.co/jiaxiangc/res-adapter). 

If downloading models take longger time, please checkout your connection with huggingface.com.

## Examples

**ResAdapter with [dreamlike-diffusion-1.0](https://huggingface.co/dreamlike-art/dreamlike-diffusion-1.0) workflow.**
<img src="misc/resadapter-1024x1024.png" witdh=100%>







