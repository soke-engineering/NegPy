from PIL import Image
import cv2
import numpy as np
from typing import Tuple
from src.domain.models import ExportConfig


class PrintService:
    """
    Handles layout, scaling and padding for print exports and previews.
    """

    @staticmethod
    def apply_preview_layout_to_pil(
        pil_img: Image.Image,
        paper_aspect_ratio: str,
        border_size_cm: float,
        print_size_cm: float,
        border_color_hex: str,
    ) -> Image.Image:
        """
        Pads a PIL image to match a specific paper aspect ratio for UI preview.
        """
        img_np = np.array(pil_img).astype(np.float32) / 255.0

        config = ExportConfig(
            paper_aspect_ratio=paper_aspect_ratio,
            export_border_size=border_size_cm,
            export_print_size=print_size_cm,
            export_border_color=border_color_hex,
            export_dpi=300,
            use_original_res=True,
        )

        result_np = PrintService.apply_layout(img_np, config)
        result_uint8 = (np.clip(result_np, 0, 1) * 255).astype(np.uint8)
        return Image.fromarray(result_uint8)

    @staticmethod
    def calculate_paper_px(
        print_size_cm: float, dpi: int, aspect_ratio_str: str, img_w: int, img_h: int
    ) -> Tuple[int, int]:
        """
        Calculates target paper dimensions in pixels.
        """
        long_edge_px = int((print_size_cm / 2.54) * dpi)

        if aspect_ratio_str == "Original":
            if img_w >= img_h:
                return long_edge_px, int(long_edge_px * (img_h / img_w))
            else:
                return int(long_edge_px * (img_w / img_h)), long_edge_px

        try:
            w_r, h_r = map(float, aspect_ratio_str.split(":"))
            ratio = w_r / h_r
        except (ValueError, ZeroDivisionError):
            ratio = 1.0

        if ratio >= 1.0:
            paper_w = long_edge_px
            paper_h = int(paper_w / ratio)
        else:
            paper_h = long_edge_px
            paper_w = int(paper_h * ratio)

        return paper_w, paper_h

    @staticmethod
    def apply_layout(img: np.ndarray, export_settings: ExportConfig) -> np.ndarray:
        """
        Scales and pads image to fit paper aspect ratio and border requirements.
        """
        img_h, img_w = img.shape[:2]
        dpi = export_settings.export_dpi
        border_px = int((export_settings.export_border_size / 2.54) * dpi)

        paper_w, paper_h = PrintService.calculate_paper_px(
            export_settings.export_print_size,
            dpi,
            export_settings.paper_aspect_ratio,
            img_w,
            img_h,
        )

        max_content_w = max(10, paper_w - 2 * border_px)
        max_content_h = max(10, paper_h - 2 * border_px)

        img_aspect = img_w / img_h

        if img_aspect > (max_content_w / max_content_h):
            target_w = max_content_w
            target_h = int(target_w / img_aspect)
        else:
            target_h = max_content_h
            target_w = int(target_h * img_aspect)

        if not export_settings.use_original_res:
            img_scaled = cv2.resize(
                img, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4
            )
        else:
            img_scaled = img
            target_w, target_h = img_w, img_h

            if export_settings.paper_aspect_ratio == "Original":
                paper_w = target_w + 2 * border_px
                paper_h = target_h + 2 * border_px
            else:
                try:
                    w_r, h_r = map(float, export_settings.paper_aspect_ratio.split(":"))
                    paper_ratio = w_r / h_r
                except Exception:
                    paper_ratio = img_aspect

                min_paper_w = target_w + 2 * border_px
                min_paper_h = target_h + 2 * border_px

                if (min_paper_w / min_paper_h) > paper_ratio:
                    paper_w = min_paper_w
                    paper_h = int(paper_w / paper_ratio)
                else:
                    paper_h = min_paper_h
                    paper_w = int(paper_h * paper_ratio)

        color_hex = export_settings.export_border_color.lstrip("#")
        r, g, b = tuple(int(color_hex[i : i + 2], 16) / 255.0 for i in (0, 2, 4))

        paper = np.full(
            (paper_h, paper_w, img.shape[2]) if img.ndim == 3 else (paper_h, paper_w),
            (r, g, b) if img.ndim == 3 else (r,),
            dtype=img.dtype,
        )

        offset_x = (paper_w - target_w) // 2
        offset_y = (paper_h - target_h) // 2

        h_to_copy = min(target_h, paper_h)
        w_to_copy = min(target_w, paper_w)

        paper[offset_y : offset_y + h_to_copy, offset_x : offset_x + w_to_copy] = (
            img_scaled[:h_to_copy, :w_to_copy]
        )

        return paper
