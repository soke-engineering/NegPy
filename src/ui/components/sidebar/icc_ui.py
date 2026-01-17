import streamlit as st
import os
from src.domain.session import WorkspaceSession
from src.domain.models import ICCMode
from src.ui.components.helpers import (
    render_control_selectbox,
    render_control_checkbox,
    render_control_radio,
)
from src.infrastructure.display.color_mgmt import ColorService


def render_icc_section() -> None:
    session: WorkspaceSession = st.session_state.session

    with st.expander(":material/palette: ICC Profiles", expanded=False):
        available_iccs = ColorService.get_available_profiles()
        all_icc_paths = ["None"] + available_iccs

        if "icc_profile_path" not in st.session_state:
            st.session_state.icc_profile_path = session.icc_profile_path or "None"
        if "icc_mode" not in st.session_state:
            st.session_state.icc_mode = (
                ICCMode.INPUT.value if session.icc_invert else ICCMode.OUTPUT.value
            )
        if "apply_icc_to_export" not in st.session_state:
            st.session_state.apply_icc_to_export = session.apply_icc_to_export

        selected_path = render_control_selectbox(
            "Profile",
            all_icc_paths,
            default_val=session.icc_profile_path or "None",
            key="icc_profile_path",
            format_func=lambda x: os.path.basename(x) if x != "None" else "None",
            help_text="Select ICC profile for simulation or correction.",
        )

        session.icc_profile_path = (
            str(selected_path) if selected_path != "None" else None
        )

        if session.icc_profile_path:
            c1, c2 = st.columns(2)
            with c1:
                mode_val = render_control_radio(
                    "Direction",
                    [m.value for m in ICCMode],
                    default_val=ICCMode.INPUT.value
                    if session.icc_invert
                    else ICCMode.OUTPUT.value,
                    key="icc_mode",
                    help_text="Input: Correction mode (profile as source). Output: Simulation mode (profile as destination).",
                )
                session.icc_invert = mode_val == ICCMode.INPUT.value

            with c2:
                apply_val = render_control_checkbox(
                    "Apply to Export",
                    default_val=session.apply_icc_to_export,
                    key="apply_icc_to_export",
                    help_text="If checked, profile is applied to exported files.",
                )
                session.apply_icc_to_export = apply_val
