import os

import comfy

base_path = os.path.dirname(os.path.realpath(__file__))
models_dir = os.path.join(base_path, "models")


def get_model_list(models_dir):
    return [f for f in os.listdir(models_dir)]


class ResAdapterLoader:
    def __init__(self):
        self.loaded_lora = None

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "resadapter_name": (get_model_list(models_dir),),
                "strength_model": (
                    "FLOAT",
                    {"default": 1.0, "min": -20.0, "max": 20.0, "step": 0.01},
                ),
                "strength_clip": (
                    "FLOAT",
                    {"default": 1.0, "min": -20.0, "max": 20.0, "step": 0.01},
                ),
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP")
    FUNCTION = "load_resadapter"

    CATEGORY = "loaders"

    def load_resadapter(self, model, clip, resadapter_name, strength_model, strength_clip):
        if strength_model == 0 and strength_clip == 0:
            return (model, clip)

        # load lora...
        lora_path = os.path.join(models_dir, f"{resadapter_name}/pytorch_lora_weights.safetensors")
        lora = None
        if self.loaded_lora is not None:
            if self.loaded_lora[0] == lora_path:
                lora = self.loaded_lora[1]
            else:
                temp = self.loaded_lora
                self.loaded_lora = None
                del temp

        if lora is None:
            lora = comfy.utils.load_torch_file(lora_path, safe_load=True)
            self.loaded_lora = (lora_path, lora)

        # load norm...
        norm_path = os.path.join(models_dir, f"{resadapter_name}/diffusion_pytorch_model.safetensors")
        if os.path.exists(norm_path):
            key_map = {}
            key_map = comfy.lora.model_lora_keys_unet(model.model, key_map)
            norm = comfy.utils.load_torch_file(norm_path, safe_load=True)
            mapping_norm = {}

            for key in norm.keys():
                if ".weight" in key:
                    key_name_in_ori_sd = key_map[key.replace(".weight", "")]
                    mapping_norm[key_name_in_ori_sd] = norm[key]
                elif ".bias" in key:
                    key_name_in_ori_sd = key_map[key.replace(".bias", "")]
                    mapping_norm[key_name_in_ori_sd.replace(".weight", ".bias")] = norm[key]
                else:
                    print("### resadapter: unexpected key", key)
                    mapping_norm[key] = norm[key]

            for k in mapping_norm.keys():
                if k not in model.model.state_dict():
                    print("### resadapter: missing key:", k)
            model.model.load_state_dict(mapping_norm, strict=False)
        else:
            print("For resolution interpolation, we do not need normalization temporally.")

        model_lora, clip_lora = comfy.sd.load_lora_for_models(model, clip, lora, strength_model, strength_clip)
        return (model_lora, clip_lora)


NODE_CLASS_MAPPINGS = {"ResAdapterLoader": ResAdapterLoader}

NODE_DISPLAY_NAME_MAPPINGS = {"ResAdapterLoader": "Load ResAdapter"}
