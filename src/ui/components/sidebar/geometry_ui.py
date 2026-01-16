import streamlit as st
from src.domain.constants import SUPPORTED_ASPECT_RATIOS
from src.features.geometry.models import CropMode
from src.ui.state.view_models import GeometryViewModel
from src.ui.components.sidebar.helpers import (
    render_control_slider,
    render_control_checkbox,
    render_control_selectbox,
)
from src.kernel.system.config import DEFAULT_WORKSPACE_CONFIG
from src.ui.state.state_manager import save_settings


def render_geometry_section() -> None:
    geo_vm = GeometryViewModel()
    geo_conf = geo_vm.to_config()

    with st.expander(":material/crop: Geometry", expanded=True):
        c_mode1, c_mode2 = st.columns(2)
        with c_mode1:
            crop_modes = list(CropMode)
            current_mode = geo_vm.crop_mode

            selected_label = st.selectbox(
                "Crop Mode",
                options=[m.value for m in crop_modes],
                index=crop_modes.index(current_mode),
                key="geometry_crop_mode_select",
                help="Select cropping method."
            )

            selected_mode = CropMode(selected_label)

            if selected_mode != current_mode:
                geo_vm.crop_mode = selected_mode
                save_settings()
                st.rerun()

        with c_mode2:
            render_control_checkbox(
                "Keep Borders",
                default_val=DEFAULT_WORKSPACE_CONFIG.geometry.keep_full_frame,
                key=geo_vm.get_key("keep_full_frame"),
                help_text="Keep entire image and film borders in final export.",
            )

        if geo_vm.crop_mode == CropMode.MANUAL:
            c_m1, c_m2 = st.columns(2)
            with c_m1:
                render_control_checkbox(
                    "Pick Crop",
                    default_val=False,
                    key=geo_vm.get_key("pick_manual_crop"),
                    is_toggle=True,
                    help_text="Click top-left and then bottom-right corner.",
                )
            with c_m2:
                if geo_conf.manual_crop_rect is not None:
                    if st.button("Reset Crop", use_container_width=True):
                        st.session_state[geo_vm.get_key("manual_crop_rect")] = None
                        save_settings()
                        st.rerun()
        else:
            c_main1, c_main2 = st.columns([1, 1])
            with c_main1:
                render_control_selectbox(
                    "Ratio",
                    SUPPORTED_ASPECT_RATIOS,
                    default_val=DEFAULT_WORKSPACE_CONFIG.geometry.autocrop_ratio,
                    key=geo_vm.get_key("autocrop_ratio"),
                    help_text="Aspect ratio to crop to.",
                )
            # Auto-Crop checkbox removed as it's now implied by mode
            with c_main2:
                # Placeholder to align layout or additional control if needed
                st.write("")

            c_a1, c_a2 = st.columns(2)
            with c_a1:
                render_control_checkbox(
                    "Pick Assist",
                    default_val=False,
                    key=geo_vm.get_key("pick_assist"),
                    is_toggle=True,
                    help_text="Click on the film border to assist detection.",
                )
            with c_a2:
                if geo_conf.autocrop_assist_luma is not None:
                    if st.button("Clear Assist", use_container_width=True):
                        st.session_state[geo_vm.get_key("autocrop_assist_point")] = None
                        st.session_state[geo_vm.get_key("autocrop_assist_luma")] = None
                        save_settings()
                        st.rerun()

        c_geo1, c_geo2 = st.columns(2)
        with c_geo1:
            render_control_slider(
                label="Crop Offset",
                min_val=-20.0,
                max_val=100.0,
                default_val=4.0,
                step=1.0,
                key=geo_vm.get_key("autocrop_offset"),
                format="%d",
                help_text="Buffer/offset (pixels) to crop beyond automatically detected border. "
                "Positive values crop IN, negative values expand OUT.",
            )
        with c_geo2:
            render_control_slider(
                label="Fine Rotation (°)",
                min_val=-5.0,
                max_val=5.0,
                default_val=0.0,
                step=0.05,
                key=geo_vm.get_key("fine_rotation"),
            )

        c_flip1, c_flip2 = st.columns(2)
        with c_flip1:
            render_control_checkbox(
                "Flip Horizontally",
                default_val=DEFAULT_WORKSPACE_CONFIG.geometry.flip_horizontal,
                key=geo_vm.get_key("flip_horizontal"),
            )
        with c_flip2:
            render_control_checkbox(
                "Flip Vertically",
                default_val=DEFAULT_WORKSPACE_CONFIG.geometry.flip_vertical,
                key=geo_vm.get_key("flip_vertical"),
            )
