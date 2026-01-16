from dataclasses import dataclass
from typing import Optional, Tuple
from enum import Enum


class CropMode(Enum):
    AUTO = "Auto-Crop"
    MANUAL = "Manual Crop"


@dataclass(frozen=True)
class GeometryConfig:
    rotation: int = 0
    fine_rotation: float = 0.0
    flip_horizontal: bool = False
    flip_vertical: bool = False

    autocrop: bool = True
    autocrop_offset: int = 2
    autocrop_ratio: str = "3:2"
    manual_crop: bool = False
    manual_crop_rect: Optional[Tuple[float, float, float, float]] = None
    keep_full_frame: bool = False
    autocrop_assist_point: Optional[Tuple[float, float]] = None
    autocrop_assist_luma: Optional[float] = None
