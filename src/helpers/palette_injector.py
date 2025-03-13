# Simple helper class to apply a selected palette to a QSS template
# This file is part of NeveBit.


class PaletteHelper:
    def __init__(self, theme_path):
        self.theme_path = theme_path

    def apply_palette(self, selected_palette, base_qss=None):
        with open(self.theme_path, "r") as file:
            qss_template = file.read()

        if qss_template:
            styled_qss = qss_template
        else:
            styled_qss = base_qss

        for color_name, color_value in vars(selected_palette).items():
            if not color_name.startswith('__') and isinstance(color_value, str):
                placeholder = "{{" + color_name + "}}"
                styled_qss = styled_qss.replace(placeholder, color_value)

        return styled_qss

    def apply_geometry(self, selected_geometry, base_qss=None):
        styled_qss = base_qss
        for attr_name, attr_value in vars(selected_geometry).items():
            if not attr_name.startswith('__'):
                placeholder = "{{" + attr_name + "}}"
                styled_qss = styled_qss.replace(placeholder, str(attr_value))

        return styled_qss
