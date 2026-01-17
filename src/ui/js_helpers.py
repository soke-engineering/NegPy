import streamlit as st
from streamlit_javascript import st_javascript  # type: ignore


def get_viewport_height() -> int:
    """
    Returns the browser window inner height in pixels.
    Persists the value to session state to avoid flickering/resetting on re-runs.
    """
    val = st_javascript("window.parent.innerHeight", key="viewport_height_js")

    if val:
        st.session_state["last_viewport_height"] = int(val)
        return int(val)

    return int(st.session_state.get("last_viewport_height", 0))
