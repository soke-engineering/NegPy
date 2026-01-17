import streamlit as st
from src.ui.components.main.actions_ui import change_file
from src.domain.session import WorkspaceSession
from src.ui.js_helpers import get_viewport_height
import logging

logger = logging.getLogger(__name__)


def render_film_strip() -> None:
    """
    Renders vertical film strip with thumbnails in 2 columns.
    """
    session: WorkspaceSession = st.session_state.session
    if not session.uploaded_files:
        return

    viewport_h = get_viewport_height()
    container_h = int(viewport_h * 0.9) if viewport_h else 1200
    with st.container(height=container_h):
        num_cols = 2
        uploaded_files = session.uploaded_files
        for i in range(0, len(uploaded_files), num_cols):
            cols = st.columns(num_cols)
            for j in range(num_cols):
                idx = i + j
                if idx < len(uploaded_files):
                    f_meta = uploaded_files[idx]
                    with cols[j]:
                        thumb = session.thumbnails.get(f_meta["name"])
                        is_selected = session.selected_file_idx == idx

                        if thumb:
                            st.image(thumb, width="stretch")
                            st.button(
                                "Select",
                                key=f"sel_{idx}",
                                width="stretch",
                                type="primary" if is_selected else "secondary",
                                on_click=change_file,
                                args=(idx,),
                            )
                        else:
                            st.write("...")
