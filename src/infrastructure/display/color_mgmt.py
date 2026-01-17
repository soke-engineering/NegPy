import os
from typing import Any, Optional
from PIL import Image, ImageCms
from src.kernel.system.config import APP_CONFIG
from src.domain.models import ColorSpace


class ColorService:
    """
    ICC profile application & soft-proofing.
    """

    @staticmethod
    def apply_icc_profile(
        pil_img: Image.Image,
        src_color_space: str,
        dst_profile_path: Optional[str],
        inverse: bool = False,
    ) -> Image.Image:
        """
        Applies ICC for proofing or correction.
        If inverse=True, dst_profile_path is treated as the SOURCE profile,
        and src_color_space as the DESTINATION.
        """
        if not dst_profile_path or not os.path.exists(dst_profile_path):
            return pil_img

        try:
            profile_working: Any
            if src_color_space == ColorSpace.ADOBE_RGB.value and os.path.exists(
                APP_CONFIG.adobe_rgb_profile
            ):
                profile_working = ImageCms.getOpenProfile(APP_CONFIG.adobe_rgb_profile)
            else:
                profile_working = ImageCms.createProfile("sRGB")

            profile_selected: Any = ImageCms.getOpenProfile(dst_profile_path)

            if inverse:
                profile_src = profile_selected
                profile_dst = profile_working
            else:
                profile_src = profile_working
                profile_dst = profile_selected

            if pil_img.mode != "RGB":
                pil_img = pil_img.convert("RGB")

            result_icc = ImageCms.profileToProfile(
                pil_img,
                profile_src,
                profile_dst,
                renderingIntent=ImageCms.Intent.RELATIVE_COLORIMETRIC,
                outputMode="RGB",
                flags=ImageCms.Flags.BLACKPOINTCOMPENSATION,
            )
            return result_icc if result_icc is not None else pil_img
        except Exception:
            return pil_img

    @staticmethod
    def simulate_on_srgb(pil_img: Image.Image, src_color_space: str) -> Image.Image:
        """
        AdobeRGB -> sRGB (approximate look).
        """
        if src_color_space != ColorSpace.ADOBE_RGB.value:
            return pil_img

        try:
            if os.path.exists(APP_CONFIG.adobe_rgb_profile):
                adobe_prof = ImageCms.getOpenProfile(APP_CONFIG.adobe_rgb_profile)
                srgb_prof: Any = ImageCms.createProfile("sRGB")

                if pil_img.mode != "RGB":
                    pil_img = pil_img.convert("RGB")

                result_sim = ImageCms.profileToProfile(
                    pil_img,
                    adobe_prof,
                    srgb_prof,
                    renderingIntent=ImageCms.Intent.RELATIVE_COLORIMETRIC,
                    outputMode="RGB",
                )
                return result_sim if result_sim is not None else pil_img
        except Exception:
            pass
        return pil_img

    @staticmethod
    def get_available_profiles() -> list[str]:
        """
        Returns list of available ICC profile paths.
        """
        built_in_icc = [
            os.path.join("icc", f)
            for f in os.listdir("icc")
            if f.lower().endswith((".icc", ".icm"))
        ]
        user_icc = []
        if os.path.exists(APP_CONFIG.user_icc_dir):
            user_icc = [
                os.path.join(APP_CONFIG.user_icc_dir, f)
                for f in os.listdir(APP_CONFIG.user_icc_dir)
                if f.lower().endswith((".icc", ".icm"))
            ]
        return sorted(built_in_icc + user_icc)
