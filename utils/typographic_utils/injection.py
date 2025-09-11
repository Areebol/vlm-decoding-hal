import torch
from PIL import Image, ImageDraw, ImageFont
import torchvision.transforms.functional as TF
from loguru import logger

def add_typographic_prompt(
        image_tensor: torch.Tensor,
        text: str,
        font_size: int = 40,
        font_path: str = "./asset/AovelSansRounded-rdDL.ttf",          
        color: tuple = (255, 255, 255), # (R,G,B), 0~255
        position: tuple = (10, 10)      # (x, y) 
    ):
    pil_img = TF.to_pil_image(image_tensor) 

    draw = ImageDraw.Draw(pil_img)

    if font_path is None:
        logger.warning("No font path provided, using default font.")
        font = ImageFont.load_default()
    else:
        font = ImageFont.truetype(font_path, font_size)

    draw.text(position, text, fill=color, font=font)

    result_tensor = TF.to_tensor(pil_img) 
    return result_tensor

# def add_resized_banner_text(
#         image_tensor: torch.Tensor,
#         text: str,
#         font_path: str = "./asset/AovelSansRounded-rdDL.ttf",
#         banner_ratio: float = 0.12,
#         banner_color: tuple = (0, 0, 0, 180),
#         text_color: tuple = (255, 255, 255),
#         pad_ratio: float = 0.20
# ) -> torch.Tensor:
#     import torchvision.transforms.functional as TF
#     from PIL import ImageFont, ImageDraw, Image
#     import torch

#     # Clone input tensor
#     image_tensor = image_tensor.clone()
#     pil_img = TF.to_pil_image(image_tensor).convert("RGBA")
#     W, H = pil_img.size

#     def get_font(size):
#         try:
#             return ImageFont.truetype(font_path, size)
#         except Exception:
#             return ImageFont.load_default()

#     # Measure text size
#     font = get_font(100)
#     draw = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
#     bbox = draw.textbbox((0, 0), text, font=font)
#     text_w = bbox[2] - bbox[0]
#     text_h = bbox[3] - bbox[1]

#     # Create text image
#     text_img = Image.new("RGBA", (text_w, text_h), (0, 0, 0, 0))
#     draw = ImageDraw.Draw(text_img)
#     draw.text((-bbox[0], -bbox[1]), text, font=font, fill=text_color + (255,))

#     # Resize and paste into banner
#     banner_h_target = int(H * banner_ratio)
#     scale = banner_h_target / text_h
#     new_text_w = max(int(text_w * scale), 1)
#     new_text_h = max(int(text_h * scale), 1)

#     text_img = text_img.resize((new_text_w, new_text_h), Image.LANCZOS)
#     banner_h = int(new_text_h * (1 + pad_ratio * 2))
#     banner = Image.new("RGBA", (W, banner_h), banner_color)

#     paste_x = (W - new_text_w) // 2
#     paste_y = (banner_h - new_text_h) // 2
#     banner.paste(text_img, (paste_x, paste_y), text_img)

#     # Paste banner to bottom of image
#     pil_img.paste(banner, (0, H - banner_h), banner)

#     # Convert back to tensor
#     result_tensor = TF.to_tensor(pil_img.convert("RGB"))  # shape: (3, H, W), range [0,1]
#     return result_tensor

from PIL import ImageFont, ImageDraw, Image
import torch

from PIL import ImageFont, ImageDraw, Image

def add_resized_banner_text_pil(
        image: Image.Image,
        text: str,
        font_path: str = "./asset/AovelSansRounded-rdDL.ttf",
        banner_ratio: float = 0.12,
        banner_color: tuple = (0, 0, 0, 180),
        text_color: tuple = (255, 255, 255),
        pad_ratio: float = 0.0
) -> Image.Image:
    image = image.convert("RGBA")
    W, H = image.size

    def get_font(size):
        try:
            return ImageFont.truetype(font_path, size)
        except Exception:
            return ImageFont.load_default()

    # Use a test font to get original text size
    font = get_font(100)
    dummy_draw = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    bbox = dummy_draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # Compute target banner height and padding
    banner_h_target = int(H * banner_ratio)
    pad = pad_ratio

    # Determine max width and height for text (after padding)
    max_text_w = W * (1 - pad * 2)
    max_text_h = banner_h_target * (1 - pad * 2)

    # Compute scale factor to fit both width and height
    scale_w = max_text_w / text_w
    scale_h = max_text_h / text_h
    scale = min(scale_w, scale_h)

    # Final text size
    new_text_w = max(int(text_w * scale), 1)
    new_text_h = max(int(text_h * scale), 1)

    # Create text image and render
    text_img = Image.new("RGBA", (new_text_w, new_text_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(text_img)

    scaled_font_size = max(int(100 * scale), 1)
    font = get_font(scaled_font_size)

    # Re-measure after font scale for better alignment
    bbox = draw.textbbox((0, 0), text, font=font)
    draw.text((-bbox[0], -bbox[1]), text, font=font, fill=text_color + (255,))

    # Create banner
    banner_h = int(new_text_h * (1 + pad * 2))
    banner = Image.new("RGBA", (W, banner_h), banner_color)

    paste_x = (W - new_text_w) // 2
    paste_y = (banner_h - new_text_h) // 2
    banner.paste(text_img, (paste_x, paste_y), text_img)

    # Paste banner to bottom
    image.paste(banner, (0, H - banner_h), banner)

    return image.convert("RGB")


# -------------------------- demo --------------------------
if __name__ == "__main__":
    import torch
    torch.manual_seed(42)
    dummy = torch.rand(3, 512, 512)
    out_tensor = add_resized_banner_text(
        dummy,
        "ATARI 2025",
        font_path="./asset/AovelSansRounded-rdDL.ttf",
        banner_ratio=0.10
    )
    TF.to_pil_image(out_tensor).save("test_banner.png")