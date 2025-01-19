import json
import os

class Configuration:
    def __init__(self) -> None:
        self._file_path = self._get_file_path()
        self.css_path = None
        self.font_path = None
        self.is_dark = False
        self.load_state = self._load_from_disk()

    def _get_file_path(self):
        config_dir = os.path.join(os.path.expanduser("~"), ".config", "gedit-markdown-preview")
        os.makedirs(config_dir, exist_ok=True)
        return os.path.join(config_dir, "settings.json")

    def _load_from_disk(self):
        if os.path.exists(self._file_path):
            with open(self._file_path, "r") as file:
                config_json = json.load(file)
                self.css_path = config_json.get("css")
                self.font_path = config_json.get("font")
                self.is_dark = config_json.get("is-dark")
                return True
        return False

    def save_to_disk(self):
        css = "default"
        font = "default"
        if self.css_path and self.css_path != "default":
            css = self.css_path
        if self.font_path and self.font_path != "default":
            font = self.font_path
        res = {
            "css": css,
            "font": font,
            "is-dark": self.is_dark,
        }
        with open(self._file_path, "w") as file:
            json.dump(res, file, indent=4)

