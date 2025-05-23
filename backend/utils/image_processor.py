import os
import uuid
from typing import Optional, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter, UnidentifiedImageError
import numpy as np

class ImageProcessor:
    def __init__(self, file_handler):
        self.file_handler = file_handler

    async def _save_processed_image(self, image: Image.Image, original_path: str, operation_name: str, execution_id: str, node_id: str, target_format: str = "PNG") -> str:
        try:
            relative_original_path = os.path.relpath(original_path, start=self.file_handler.base_upload_dir)
            original_subdir = os.path.dirname(relative_original_path)
        except ValueError:
            original_subdir = self.file_handler.workflow_upload_subdir

        pil_format = target_format.upper()
        if pil_format == "JPG": pil_format = "JPEG"
        extension = target_format.lower()

        output_filename_base = f"{execution_id}_{node_id}_{operation_name}_{str(uuid.uuid4())[:8]}"

        output_path = os.path.join(self.file_handler.base_upload_dir, original_subdir, f"{output_filename_base}.{extension}")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        if pil_format == "JPEG" and image.mode in ('RGBA', 'LA', 'P'):
            if image.mode == 'P' and 'transparency' in image.info:
                 image = image.convert('RGBA').convert('RGB')
            elif image.mode != 'P':
                 image = image.convert('RGB')

        image.save(output_path, format=pil_format)
        return output_path

    async def apply_style_transfer(self, image_path: str, style: str, intensity: float, execution_id: str, node_id: str) -> str:
        try:
            img = Image.open(image_path).convert("RGB")
        except UnidentifiedImageError:
            raise ValueError(f"Cannot identify image file: {image_path}")

        if style == "vintage":
            r, g, b = img.split()
            r = r.point(lambda i: i * 0.393 + 0.769 * i + 0.189 * i)
            g = g.point(lambda i: i * 0.349 + 0.686 * i + 0.168 * i)
            b = b.point(lambda i: i * 0.272 + 0.534 * i + 0.131 * i)
            img = Image.merge("RGB", (r, g, b))
            img = img.filter(ImageFilter.GaussianBlur(radius=intensity * 0.5))
        elif style == "neon":
            img = img.filter(ImageFilter.CONTOUR)
            img = img.point(lambda p: p * (1 + intensity * 2))
        elif style == "watercolor":
            img = img.filter(ImageFilter.MedianFilter(size=int(3 + intensity * 4)))
            img = img.filter(ImageFilter.SMOOTH_MORE)
        elif style == "oil_painting":
            img = img.filter(ImageFilter.ModeFilter(size=int(5 + intensity * 5)))
        else:
            img = img.filter(ImageFilter.GaussianBlur(radius=intensity))

        return await self._save_processed_image(img, image_path, f"styled_{style}", execution_id, node_id)

    async def apply_text_overlay(
        self, image_path: str, text_content: str, position: str,
        font_size: int, font_color: str, background_color: str,
        execution_id: str, node_id: str
    ) -> str:
        try:
            img = Image.open(image_path).convert("RGBA")
        except UnidentifiedImageError:
            raise ValueError(f"Cannot identify image file: {image_path}")

        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            try:
                font = ImageFont.truetype("DejaVuSans.ttf", font_size)
            except IOError:
                font = ImageFont.load_default()

        text_anchor_point = (0,0)
        bbox = draw.textbbox(text_anchor_point, text_content, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x_pos, y_pos = 0, 0
        if position == "top":
            x_pos = (img.width - text_width) / 2
            y_pos = 10
        elif position == "center":
            x_pos = (img.width - text_width) / 2
            y_pos = (img.height - text_height) / 2
        elif position == "bottom":
            x_pos = (img.width - text_width) / 2
            y_pos = img.height - text_height - 10
        else:
            x_pos = (img.width - text_width) / 2
            y_pos = (img.height - text_height) / 2

        x_pos, y_pos = int(x_pos), int(y_pos)

        text_draw_xy = (x_pos, y_pos)

        if background_color and background_color.lower() not in ["transparent", "#00000000", "none"]:
            bg_x0 = x_pos - 5
            bg_y0 = y_pos - 5
            bg_x1 = x_pos + text_width + 5
            bg_y1 = y_pos + text_height + 5
            draw.rectangle([bg_x0, bg_y0, bg_x1, bg_y1], fill=background_color)

        draw.text(text_draw_xy, text_content, font=font, fill=font_color)

        return await self._save_processed_image(img, image_path, "text_overlay", execution_id, node_id, target_format="PNG")

    async def crop_resize_image(
        self, image_path: str, width: Optional[int],
        height: Optional[int], crop_type: str,
        execution_id: str, node_id: str
    ) -> str:
        try:
            img = Image.open(image_path)
        except UnidentifiedImageError:
            raise ValueError(f"Cannot identify image file: {image_path}")

        original_width, original_height = img.size

        target_width = width if width and width > 0 else original_width
        target_height = height if height and height > 0 else original_height

        if crop_type == "resize_only" or not width or not height:
            img_processed = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        elif crop_type == "center_crop":
            img_aspect = original_width / original_height
            target_aspect = target_width / target_height

            if img_aspect > target_aspect:
                new_height = target_height
                new_width = int(new_height * img_aspect)
            else:
                new_width = target_width
                new_height = int(new_width / img_aspect)

            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            left = (new_width - target_width) / 2
            top = (new_height - target_height) / 2
            right = (new_width + target_width) / 2
            bottom = (new_height + target_height) / 2
            img_processed = img_resized.crop((left, top, right, bottom))

        elif crop_type == "smart_crop":
            img_aspect = original_width / original_height
            target_aspect = target_width / target_height
            if img_aspect > target_aspect:
                new_height = target_height
                new_width = int(new_height * img_aspect)
            else:
                new_width = target_width
                new_height = int(new_width / img_aspect)
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            left = (new_width - target_width) / 2
            top = (new_height - target_height) / 2
            right = (new_width + target_width) / 2
            bottom = (new_height + target_height) / 2
            img_processed = img_resized.crop((left, top, right, bottom))
        else:
            img_processed = img.resize((target_width, target_height), Image.Resampling.LANCZOS)

        return await self._save_processed_image(img_processed, image_path, "crop_resize", execution_id, node_id)

    async def convert_image_format(
        self, image_path: str, target_format_str: str, quality: int,
        execution_id: str, node_id: str
    ) -> str:
        try:
            img = Image.open(image_path)
        except UnidentifiedImageError:
            raise ValueError(f"Cannot identify image file: {image_path}")

        pil_format = target_format_str.upper()
        if pil_format == "JPG": pil_format = "JPEG"
        if pil_format not in ["PNG", "JPEG", "WEBP", "GIF", "BMP", "TIFF"]:
            raise ValueError(f"Unsupported target format: {target_format_str}")

        save_kwargs = {}
        if pil_format == 'JPEG':
            if img.mode == 'RGBA' or img.mode == 'LA' or (img.mode == 'P' and 'transparency' in img.info):
                 img = img.convert('RGB')
            save_kwargs['quality'] = quality
            save_kwargs['optimize'] = True
        elif pil_format == 'PNG':
            save_kwargs['compress_level'] = max(0, min(9, int(9 - (quality -1) / 11)))
        elif pil_format == 'WEBP':
            save_kwargs['quality'] = quality
            if img.mode == 'RGBA' or img.mode == 'LA':
                save_kwargs['lossless'] = False

        return await self._save_processed_image(img, image_path, f"converted_{target_format_str.lower()}", execution_id, node_id, target_format=target_format_str)
