import json


class Settings:
    def __init__(self, filepath="settings.json"):
        self.filepath = filepath
        self.data = self.default_settings()
        self.load()

    def default_settings(self):
        return {
            "settings": {
                "pict_tall_open_eye": "",
                "pict_tall_close_eye": "",
                "pict_silens_open_eye": "",
                "pict_silens_close_eye": "",
                "volume_threshold": 1000,
                "shaking": 0,
                "shaking_threshold": 750,
                "color_filling": "255, 0, 0",
                "color_filling_threshold": 750,
                "blinking": False,
                "blinking_rate": 2
            }
        }

    def load(self):
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                self.data["settings"].update(loaded.get("settings", {}))
        except:
            pass

    def save(self):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def get(self, key, default=None):
        return self.data["settings"].get(key, default)

    def set(self, key, value):
        self.data["settings"][key] = value

    def reset(self):
        self.data = self._default_settings()