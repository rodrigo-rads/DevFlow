import json
from pathlib import Path

class ConfigManager:
    def __init__(self, config_file="config.json"):
        self.config_file = Path(config_file)
        self.config = {
            "last_output_dir": "",
            "path_by_type": {
                "controller": "",
                "service": "",
                "repository": "",
                "service_interface": "",
                "repository_interface": ""
            }
        }
        self.load()

    def load(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as file:
                    self.config.update(json.load(file))
            except Exception as e:
                print(f"Erro ao carregar arquivo de configuração: {e}")
    
    def save(self):
        try:
            with open(self.config_file, "w", encoding="utf-8") as file:
                json.dump(self.config, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Erro ao salvar config: {e}")

    def set(self, key, value):
        self.config[key] = value
    
    def get(self, key, default = None):
        return self.config.get(key, default)