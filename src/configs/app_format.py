# Palette groups for the application.
# This file is part of NeveBit.


class app_geometry:
    """Default application geometry settings."""
    def __init__(self):
        # Fonts
        self.font_size = "12px"
        self.font_size_consoles = "13px"
        self.font_size_list = "13px"
        self.font_size_descriptor = "16px"

        # Buttons
        self.button_height = "30px"
        self.button_height_descriptor = "30px"

        # Text boxes
        self.line_edit_height = "15px"
        self.line_edit_stats_height = "15px"
        self.tooltips_height = "15px"

        # Loading bar
        self.progress_bar_height = "30px"

        # Graphs
        self.graph_font = "Ubuntu"
        self.graph_font_size_title = 12
        self.graph_font_size_axis = 10