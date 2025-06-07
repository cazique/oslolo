
# src/oslolo/utils/config_manager.py
# A simple placeholder for future configuration management.
# For now, we will use hardcoded defaults.

class ConfigManager:
    def __init__(self):
        self.settings = {
            "default_theme": "dark",
            "show_hidden_files": False,
        }

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value

config = ConfigManager()
