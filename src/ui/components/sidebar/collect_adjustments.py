from src.ui.state.view_models import SidebarState
from src.ui.components.sidebar.local_adjustments_ui import (
    render_local_adjustments,
)
from src.ui.components.sidebar.exposure_ui import render_exposure_section
from src.ui.components.sidebar.paper_toning_ui import render_paper_section
from src.ui.components.sidebar.lab_scanner_ui import (
    render_lab_scanner_section,
)
from src.ui.components.sidebar.retouch_ui import render_retouch_section
from src.ui.components.sidebar.export_ui import render_export_section
from src.ui.components.sidebar.presets_ui import render_presets
from src.ui.components.sidebar.analysis_ui import render_analysis_section
from src.ui.components.sidebar.icc_ui import render_icc_section
from src.ui.components.sidebar.helpers import (
    render_control_selectbox,
    reset_wb_settings,
)
from src.kernel.system.config import DEFAULT_WORKSPACE_CONFIG


def render_adjustments() -> SidebarState:
    render_control_selectbox(
        "Processing Mode",
        ["C41", "B&W"],
        default_val=DEFAULT_WORKSPACE_CONFIG.process_mode,
        key="process_mode",
        on_change=reset_wb_settings,
        help_text="Choose processing mode between Color Negative (C41) and B&W Negative",
    )

    render_presets()
    render_analysis_section()
    render_exposure_section()
    render_lab_scanner_section()
    render_paper_section()
    render_local_adjustments()
    render_retouch_section()
    render_icc_section()

    export_data = render_export_section()

    return export_data
